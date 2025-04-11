# src/view.py
import os
import glob
import pandas as pd
import config
import data_processor # データ読み込みに使用
from IPython.display import display, HTML

def display_latest_metrics():
    """
    Reads the latest calculated metrics file and displays the key indicators using HTML.
    Designed for use in IPython/Jupyter environments.
    """
    # data_processor を使って最新の処理済みメトリクスデータを読み込む
    # data_processor のデフォルトパターンに合わせる
    metrics_df = data_processor.read_latest_parquet('processed', filename_pattern="calculated_metrics_*.parquet")

    if metrics_df is None or metrics_df.empty:
        print(f"No calculated metric files found or the latest file is empty in '{config.PROCESSED_METRICS_DIR}'.")
        print("Please run the data fetching and processing scripts (e.g., main.py) first.")
        return

    # --- Display Metrics ---
    # 通常、calculate_metrics は1行のDataFrameを返す想定
    if len(metrics_df) > 1:
        print(f"Warning: Metrics file contains {len(metrics_df)} rows. Displaying the last row.")
        latest_metrics = metrics_df.iloc[-1] # 最新行を選択
    else:
        latest_metrics = metrics_df.iloc[0]

    # Define columns to display and map to DataFrame columns
    # data_processor.calculate_metrics で計算される列名に合わせる
    display_columns_map = {
        '現物ティッカー': 'spot_ticker',
        '先物ティッカー': 'futures_ticker',
        '現物価格': 'spot_price',
        '先物価格': 'futures_price',
        'ベーシス': 'basis',
        'ベーシス率 (%)': 'basis_rate_percent',
        '年率換算ベーシス (30d, %)': 'annualized_basis_percent_30d',
        # 'ベーシスZスコア': 'basis_z_score', # indicator_calculatorで計算/追加される場合
        '市場レジーム': 'market_regime',
        '計算タイムスタンプ': 'timestamp', # metrics計算時のタイムスタンプ
        '現物データ日時': 'spot_data_timestamp', # 元データのタイムスタンプ
        '先物データ日時': 'futures_data_timestamp',
    } # 閉じ括弧を追加

    # Prepare data for HTML display
    html_output = '<div class="latest-data-grid">' # 開始タグ

    for display_name, col_name in display_columns_map.items():
        html_output += '<div class="latest-data-item">' # 各項目の開始タグ
        html_output += f'<strong>{display_name}:</strong> ' # ラベルを太字に

        if col_name in latest_metrics and pd.notna(latest_metrics[col_name]):
            value = latest_metrics[col_name]

            # Format values nicely
            try:
                if isinstance(value, (int, float)):
                    if 'percent' in col_name or 'rate' in col_name:
                        formatted_value = f"{value:.4f}%"
                    elif col_name == 'basis_z_score': # Zスコアのフォーマット
                        formatted_value = f"{value:.2f}"
                    elif col_name in ['spot_price', 'futures_price', 'basis']:
                        formatted_value = f"{value:,.4f}" # 小数点以下4桁、カンマ区切り
                    else:
                        formatted_value = f"{value}" # Default formatting for other numbers
                elif isinstance(value, pd.Timestamp):
                     # タイムゾーン情報があれば表示、なければそのまま
                     try:
                          # ローカルタイムゾーンに変換して表示する場合 (環境依存に注意)
                          # formatted_value = value.tz_localize(None).strftime('%Y-%m-%d %H:%M:%S') # Naiveに変換
                          # UTCのまま表示する場合
                          formatted_value = value.strftime('%Y-%m-%d %H:%M:%S %Z') # タイムゾーン含む
                          if not formatted_value.strip().endswith("Z") and "UTC" not in formatted_value : # タイムゾーン情報がない場合
                               formatted_value = value.strftime('%Y-%m-%d %H:%M:%S') + " (UTC?)" # 推測を追加
                     except Exception: # タイムゾーン関連エラーのフォールバック
                          formatted_value = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    formatted_value = str(value) # Ensure strings
            except Exception as format_error:
                 print(f"Error formatting value for {col_name}: {value} ({type(value)}) - {format_error}")
                 formatted_value = f"Error ({value})"


            html_output += f'{formatted_value}'
        elif col_name in latest_metrics and pd.isna(latest_metrics[col_name]):
             html_output += 'N/A' # NaN値の場合
        else:
            # print(f"Warning: Column '{col_name}' not found in the metrics data.")
            html_output += 'Not Found'
        html_output += '</div>' # 各項目の終了タグ

    html_output += '</div>' # 終了タグ

    # Add some basic CSS for grid layout
    # CSSの閉じ括弧と <style> タグを追加
    style = """
<style>
.latest-data-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* 幅を少し広げる */
    gap: 12px; /* 少し間隔を広げる */
    font-family: sans-serif;
    border: 1px solid #ccc;
    padding: 15px;
    border-radius: 5px;
    background-color: #f9f9f9;
    margin-bottom: 15px; /* 下にマージン追加 */
}

.latest-data-item {
    background-color: #fff;
    padding: 12px; /* 少しパディングを増やす */
    border: 1px solid #eee;
    border-radius: 4px; /* 少し角を丸める */
    word-wrap: break-word; /* 長い文字列を折り返す */
}

.latest-data-item strong {
    /* display: inline-block; ラベルと値を横並びにする場合 */
    display: block; /* ラベルを上に表示する場合 */
    margin-bottom: 4px; /* ラベルと値の間隔 */
    color: #333;
    /* min-width: 150px; 横並びの場合に有効 */
}
</style>
""" # <style> タグを追加

    # Display using IPython.display.HTML
    print(f"Displaying data from the latest metrics file used: (Source DF shape: {metrics_df.shape})")
    display(HTML(style + html_output))

def main():
    """メイン関数 (スクリプトとして実行時)"""
    print("Attempting to display latest metrics...")
    display_latest_metrics()

if __name__ == "__main__":
    # このスクリプトを直接実行しても、通常はIPython環境ではないため、
    # display(HTML(...)) は期待通りに動作しない可能性があります。
    # Jupyter Notebook や IPython コンソールでの使用を想定しています。
    main()
