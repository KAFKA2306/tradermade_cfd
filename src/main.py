import os
from datetime import datetime, timedelta
import api_client
import data_processor # data_processor をインポート
import utils
import config
import file_manager # file_manager をインポート
# import indicator_calculator # 必要に応じてインポート
# import view # 必要に応じてインポート

# main_fetch.py と main_process.py (仮) に分ける方が管理しやすいが、
# ここでは main.py に統合されていると仮定して修正する。

def run_fetch_cycle():
    """データ取得サイクルを実行"""
    print("--- Starting Data Fetch Cycle ---")

    # APIキーとディレクトリの確認
    if not utils.verify_api_key(): return
    utils.create_directories()
    if not api_client.initialize_api(): return

    # --- Fetch Real-time Data ---
    # SPOT_TICKER と FUTURES_TICKER に加えて、他のシンボルも取得する場合
    live_symbols_list = list(set([config.SPOT_TICKER, config.FUTURES_TICKER, 'US30', 'DE40'])) # 例: 重複削除
    live_symbols_str = ','.join(live_symbols_list)
    print(f"Fetching real-time data for: {live_symbols_str}")
    live_data_df = api_client.get_live_data(live_symbols_str)
    if live_data_df is not None:
        # file_manager を使って保存 (プレフィックスは汎用的に)
        filepath = file_manager.save_data(live_data_df, config.REAL_TIME_DIR, "real_time_data")
        if filepath: print(f"Real-time data saved to {filepath}")
    else:
        print("Failed to fetch or save real-time data.")

    # --- Fetch Historical Data (Yesterday's close for context) ---
    for ticker in [config.SPOT_TICKER, config.FUTURES_TICKER]:
        print(f"Fetching historical data for: {ticker}")
        hist_df = api_client.get_historical_data(ticker, days_back=1) # デフォルトで昨日
        if hist_df is not None:
            # ファイル名にティッカーを含める
            filepath = file_manager.save_data(hist_df, config.HISTORICAL_DIR, f"historical_data_{ticker}")
            if filepath: print(f"Historical data for {ticker} saved to {filepath}")
        else:
            print(f"Failed to fetch or save historical data for {ticker}.")


    # --- Fetch Time Series Data (e.g., hourly for past 7 days) ---
    for ticker in [config.SPOT_TICKER, config.FUTURES_TICKER]:
        print(f"Fetching time series data for: {ticker}")
        ts_df = api_client.get_time_series_data(ticker, days=7, interval='hourly') # 過去7日間の時間足
        if ts_df is not None:
             # ファイル名にティッカーを含める
            filepath = file_manager.save_data(ts_df, config.TIME_SERIES_DIR, f"time_series_data_{ticker}")
            if filepath: print(f"Time series data for {ticker} saved to {filepath}")
        else:
            print(f"Failed to fetch or save time series data for {ticker}.")


    print("--- Data Fetch Cycle Complete ---")


def run_processing_cycle():
    """データ処理サイクルを実行 (メトリクス計算など)"""
    print("--- Starting Data Processing Cycle ---")

    # ディレクトリ存在確認 (念のため)
    utils.create_directories()

    # 最新のリアルタイムデータを読み込む (全シンボル含む汎用ファイル)
    # data_processor.read_latest_parquet は最新のファイルを読む
    latest_live_generic_df = data_processor.read_latest_parquet("real_time", filename_pattern="real_time_data_*.parquet")

    if latest_live_generic_df is None or latest_live_generic_df.empty:
        print("Could not read the latest generic real-time data file. Cannot process metrics.")
        return # return に変更

    # 'instrument' 列が存在するか確認
    if 'instrument' not in latest_live_generic_df.columns:
        print("Error: 'instrument' column missing in latest real-time data. Cannot filter tickers.")
        # もし 'instrument' がなくても SPOT/FUTURES が1行ずつしかないと仮定できるなら別の処理も可能だが、推奨しない
        return # return に変更

    # SPOT と FUTURES のデータをフィルタリング
    spot_live_df = latest_live_generic_df[latest_live_generic_df['instrument'] == config.SPOT_TICKER]
    futures_live_df = latest_live_generic_df[latest_live_generic_df['instrument'] == config.FUTURES_TICKER]

    # 必要なデータがあるか確認
    if spot_live_df.empty:
        print(f"Could not find latest live data for SPOT ticker: {config.SPOT_TICKER} in the file. Cannot process metrics.")
        return # return に変更
    if futures_live_df.empty:
        print(f"Could not find latest live data for FUTURES ticker: {config.FUTURES_TICKER} in the file. Cannot process metrics.")
        return # return に変更

    # メトリクスの計算
    print(f"Calculating metrics between {config.SPOT_TICKER} and {config.FUTURES_TICKER}...")
    # data_processor の関数を使用
    metrics_df = data_processor.calculate_metrics(spot_live_df, futures_live_df)

    if metrics_df is not None and not metrics_df.empty:
        # メトリクスを PROCESSED_METRICS_DIR に保存
        # data_processor.save_dataframe_to_parquet を使う
        filepath = data_processor.save_dataframe_to_parquet(metrics_df, "processed", "calculated_metrics")
        if filepath:
             print(f"Calculated metrics saved to {filepath}")
        else:
             print("Failed to save calculated metrics.")
    else:
         print("Metrics calculation failed or returned None/Empty.")

    print("--- Data Processing Cycle Complete ---")


def main():
    """メイン実行関数"""
    # 1. データ取得を実行
    run_fetch_cycle()

    # 2. データ処理を実行 (メトリクス計算)
    run_processing_cycle()

    # 3. 指標計算を実行 (オプション)
    # print("\n--- Running Indicator Calculation ---")
    # try:
    #     import indicator_calculator
    #     indicator_calculator.calculate_indicators()
    # except ImportError:
    #     print("indicator_calculator module not found, skipping indicator calculation.")
    # except Exception as e:
    #     print(f"Error during indicator calculation: {e}")

    # 4. 結果表示を実行 (オプション、Jupyter/IPython環境向け)
    # print("\n--- Displaying Latest Metrics (if in suitable environment) ---")
    # try:
    #     # Check if running in an IPython environment
    #     from IPython import get_ipython
    #     if get_ipython() is not None:
    #         import view
    #         view.display_latest_metrics()
    #     else:
    #         print("Not in an IPython/Jupyter environment. Skipping display.")
    # except ImportError:
    #     print("IPython or view module not found, skipping display.")
    # except Exception as e:
    #     print(f"Error during display: {e}")

if __name__ == "__main__":
    main()