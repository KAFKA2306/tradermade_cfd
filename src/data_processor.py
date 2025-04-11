import pandas as pd
import os
import glob # glob をインポート
from datetime import datetime
import config
import file_manager # file_manager をインポート (保存に使う場合)

# --- Parquet保存の共通ヘルパー関数 ---
# Note: file_manager.py に同様の機能があるため、統合を検討。
#       ここでは既存の構造を維持し、必要な修正のみ行う。
#       file_manager.save_data を使うように変更
def _save_data_parquet(data, filename_prefix, data_dir):
    """データをDataFrameに変換し、Parquet形式で指定ディレクトリに保存する (内部用)"""
    # file_manager.save_data を使う方が一貫性がある
    filepath = file_manager.save_data(data, data_dir, filename_prefix)
    if filepath:
        print(f"(processor using file_manager) Data saved to {filepath}")
    else:
        print(f"(processor using file_manager) Failed to save data for prefix '{filename_prefix}'.")
    return filepath

# --- データタイプ別保存関数 ---
def save_real_time_data(real_time_data):
    """リアルタイムデータを保存"""
    return _save_data_parquet(real_time_data, "real_time_data", config.REAL_TIME_DIR)

def save_historical_data(historical_data):
    """過去データを保存"""
    return _save_data_parquet(historical_data, "historical_data", config.HISTORICAL_DIR)

def save_time_series_data(time_series_data):
    """時系列データを保存"""
    return _save_data_parquet(time_series_data, "time_series_data", config.TIME_SERIES_DIR)

# --- データ読み込み関数 ---
def read_latest_parquet(data_type, filename_pattern=None):
    """指定されたタイプの最新のParquetファイルを読み込む"""
    dir_path = None
    default_pattern = "*.parquet" # デフォルトパターン

    if data_type == 'real_time':
        dir_path = config.REAL_TIME_DIR
        default_pattern = "real_time_data_*.parquet"
    elif data_type == 'historical':
        dir_path = config.HISTORICAL_DIR
        default_pattern = "historical_data_*.parquet"
    elif data_type == 'time_series':
        dir_path = config.TIME_SERIES_DIR
        default_pattern = "time_series_data_*.parquet"
    elif data_type == 'processed':
        dir_path = config.PROCESSED_METRICS_DIR
        default_pattern = "calculated_metrics_*.parquet"
    elif data_type == 'indicator':
        dir_path = config.INDICATOR_DIR
        default_pattern = "indicator_data_*.parquet"
    else:
        print(f"Unknown data_type for reading: {data_type}")
        return None

    if not os.path.isdir(dir_path):
         print(f"Directory not found for reading: {dir_path}")
         return None

    # filename_pattern が指定されていない場合は、そのタイプのデフォルトパターンを使用
    if filename_pattern is None:
        filename_pattern = default_pattern

    search_pattern = os.path.join(dir_path, filename_pattern)
    print(f"Searching for files: {search_pattern}")
    # glob をインポート済み
    data_files = glob.glob(search_pattern)

    if not data_files:
        print(f"No files found matching pattern: {search_pattern}")
        return None

    latest_file = None # 初期化
    try:
        latest_file = max(data_files, key=os.path.getctime)
        print(f"Reading latest file: {latest_file}")
        # file_manager.load_data を使う
        return file_manager.load_data(latest_file)
    except Exception as e:
        print(f"Error reading latest Parquet file ({latest_file}): {e}")
        return None

# --- メトリクス計算関数 ---
def calculate_metrics(spot_df, futures_df):
    """スポットと先物の最新データからメトリクスを計算"""
    try:
        # データが空でないか、必要なカラムがあるか確認
        if spot_df is None or spot_df.empty:
             print("Spot DataFrame is empty or None. Cannot calculate metrics.")
             return None
        if futures_df is None or futures_df.empty:
             print("Futures DataFrame is empty or None. Cannot calculate metrics.")
             return None

        # .iloc[-1] を使うのは、DataFrameがタイムスタンプ等でソートされている前提
        # もしソートされていない場合や、特定のタイムスタンプのデータが必要な場合はロジック変更
        spot_row = spot_df.iloc[-1] # 最新行を取得
        futures_row = futures_df.iloc[-1] # 最新行を取得

        # 価格の抽出 (midが優先、なければclose, ask, bid の順で試す)
        spot_price = spot_row.get('mid', spot_row.get('close', spot_row.get('ask', spot_row.get('bid'))))
        future_price = futures_row.get('mid', futures_row.get('close', futures_row.get('ask', futures_row.get('bid'))))

        if spot_price is None:
            print(f"Could not find price ('mid', 'close', 'ask', 'bid') in spot data row: {spot_row}")
            return None
        if future_price is None:
            print(f"Could not find price ('mid', 'close', 'ask', 'bid') in futures data row: {futures_row}")
            return None

        # 数値型に変換 (エラー時 None)
        try:
            spot_price = float(spot_price)
            future_price = float(future_price)
        except (ValueError, TypeError):
            print(f"Could not convert prices to float. Spot: '{spot_price}', Future: '{future_price}'")
            return None


        # 基本指標の計算
        basis = future_price - spot_price
        # ゼロ除算を回避
        basis_rate_percent = (basis / spot_price) * 100 if spot_price != 0 else 0.0

        # 30日を想定した年率換算ベーシス (日数は要件に応じて変更)
        days_to_expiry = 30 # 仮定
        # ゼロ除算を回避
        annualized_basis_percent = (basis_rate_percent * 365) / days_to_expiry if days_to_expiry != 0 else 0.0

        # 結果をデータフレームに格納
        metrics = {
            'spot_ticker': spot_row.get('instrument', config.SPOT_TICKER), # instrument列があれば使う
            'futures_ticker': futures_row.get('instrument', config.FUTURES_TICKER),
            'spot_price': spot_price,
            'futures_price': future_price,
            'basis': basis,
            'basis_rate_percent': basis_rate_percent,
            'annualized_basis_percent_30d': annualized_basis_percent,
            'timestamp': datetime.now(), # 計算実行時のタイムスタンプ
            'spot_data_timestamp': spot_row.name if isinstance(spot_row.name, pd.Timestamp) else pd.NaT, # 元データのタイムスタンプ(index)
            'futures_data_timestamp': futures_row.name if isinstance(futures_row.name, pd.Timestamp) else pd.NaT,
            'market_regime': 'contango' if basis > 0 else ('backwardation' if basis < 0 else 'flat') # 閉じ括弧修正
        } # 閉じ括弧を追加

        metrics_df = pd.DataFrame([metrics])
        # タイムスタンプをインデックスに設定する場合
        # metrics_df['timestamp'] = pd.to_datetime(metrics_df['timestamp'])
        # metrics_df = metrics_df.set_index('timestamp')

        print(f"Metrics calculated: Basis={basis:.4f}, Basis Rate={basis_rate_percent:.4f}%")
        return metrics_df

    except IndexError:
         print("Error accessing data row (IndexError). Check if DataFrames are empty or index is valid.")
         return None
    except KeyError as e:
         print(f"Error accessing column (KeyError): {e}. Check column names in DataFrames.")
         return None
    except Exception as e:
        print(f"An unexpected error occurred during metrics calculation: {e}")
        return None

# --- DataFrame保存関数 (file_managerと重複するが、タイプ指定を追加) ---
def save_dataframe_to_parquet(df, data_type, filename_prefix):
    """DataFrameを指定されたタイプのディレクトリにParquet形式で保存する"""
    dir_path = None
    if data_type == 'processed':
        dir_path = config.PROCESSED_METRICS_DIR
    elif data_type == 'indicator':
        dir_path = config.INDICATOR_DIR
    # 他のタイプも必要なら追加
    else:
        print(f"Unknown data_type for saving DataFrame: {data_type}")
        return None

    if df is None or df.empty:
        print(f"DataFrame for '{filename_prefix}' is empty or None. Skipping save.")
        return None

    # file_manager.save_data を使用
    return file_manager.save_data(df, dir_path, filename_prefix)
