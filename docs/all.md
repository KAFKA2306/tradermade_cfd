```markdown
# TraderMade API データ取得・保存システム

## 1. プロジェクト構成

```
tradermade_cfd/
│
├── .venv/                  # Python仮想環境
├── output/                 # データ出力先ベースディレクトリ
│   ├── real_time_data/     # リアルタイムデータ保存先 (Parquet)
│   ├── historical_data/    # 履歴データ保存先 (Parquet)
│   └── time_series_data/   # 時系列データ保存先 (Parquet)
│
├── src/                    # ソースコードディレクトリ
│   ├── __init__.py
│   ├── api_client.py       # TraderMade APIとの通信
│   ├── config.py           # 設定ファイル (ディレクトリパス、APIキー)
│   ├── data_processor.py   # データ処理・保存 (Parquet)
│   ├── main.py             # メイン実行スクリプト
│   ├── utils.py            # ユーティリティ関数 (ディレクトリ作成、検証)
│   └── view.py             # 保存されたParquetデータの表示 (オプション)
│
└── requirements.txt        # 依存ライブラリリスト
```

## 2. APIキー設定 (Windows環境変数)

TraderMade APIキーをWindowsの環境変数 `TRADERMADE_API_KEY` に設定します。

### 一時的な設定 (現在のコマンドプロンプトセッションのみ有効)

```
set TRADERMADE_API_KEY=YOUR_API_KEY
```

### 恒久的な設定

1.  コマンドプロンプトを**管理者として実行**します。
2.  以下のコマンドを実行します (`YOUR_API_KEY` を実際のキーに置き換えてください)。

    ```
    setx TRADERMADE_API_KEY "YOUR_API_KEY" /M
    ```
3.  コマンドプロンプトを再起動するか、システムを再起動すると設定が反映されます。

## 3. `requirements.txt`

```
pandas
pyarrow
tradermade
ipython
```

## 4. ソースコード (`src` ディレクトリ)

### `src/config.py`

```
import os

# 注意: このパスはユーザーの環境に合わせて変更してください
# 例: BASE_DIR = r"C:/Users/YourUser/Projects/tradermade_cfd"
# 例: BASE_DIR = r"E:/e/d"
BASE_DIR = r"M:/ML/Finance/tradermade_cfd" #  bool:
    if not config.API_KEY:
        print("Error: TRADERMADE_API_KEY environment variable is not set.")
        print("Please set the environment variable 'TRADERMADE_API_KEY' with your API key.")
        print("Temporary: set TRADERMADE_API_KEY=YOUR_KEY")
        print("Permanent (Admin CMD): setx TRADERMADE_API_KEY \"YOUR_KEY\" /M")
        return False
    else:
        print(f"TRADERMADE_API_KEY found (starts with: {config.API_KEY[:4]}...).")
        return True

```

### `src/api_client.py`

```
import os
import pandas as pd
import tradermade as tm
import src.config as config # config をインポート

if config.API_KEY:
    tm.set_rest_api_key(config.API_KEY)
else:
    print("Warning: TRADERMADE_API_KEY environment variable not set. API calls will likely fail.")

def get_real_time_data(symbols: str) -> pd.DataFrame:
    """
    指定されたシンボルのリアルタイムデータを取得し、DataFrameで返す。
    """
    try:
        # tm.liveはリスト形式で返すことが多い
        data = tm.live(currency=symbols, fields=['bid', 'mid', 'ask'])
        print(f"Type of real-time data received: {type(data)}")
        print(f"Content of real-time data: {data}")

        if isinstance(data, list) and data:
            df = pd.DataFrame(data)
            # 'instrument' 列がない場合、リクエストしたシンボルから補完を試みる
            if 'instrument' not in df.columns:
                symbol_list = [s.strip() for s in symbols.split(',')]
                if len(df) == len(symbol_list):
                    df['instrument'] = symbol_list
                else:
                    # データ数とシンボル数が一致しない場合は警告
                    print(f"Warning: Row count ({len(df)}) doesn't match symbol count ({len(symbol_list)}). Cannot reliably assign instruments.")
                    df['instrument'] = 'Unknown' # または None など
            return df
        elif isinstance(data, dict) and 'quotes' in data: # まれに辞書形式で返る可能性も考慮
             df = pd.DataFrame(data['quotes'])
             if 'instrument' not in df.columns:
                 symbol_list = [s.strip() for s in symbols.split(',')]
                 if len(df) == len(symbol_list):
                     df['instrument'] = symbol_list
                 else:
                     print(f"Warning: Row count ({len(df)}) doesn't match symbol count ({len(symbol_list)}). Cannot reliably assign instruments.")
                     df['instrument'] = 'Unknown'
             return df
        elif isinstance(data, dict) and 'message' in data: # エラーメッセージの場合
            print(f"API returned message for real-time data ({symbols}): {data['message']}")
            return pd.DataFrame()
        else:
             print(f"Unexpected format or empty data received for real-time data: {data}")
             return pd.DataFrame()

    except Exception as e:
        print(f"Error fetching real-time data for {symbols}: {e}")
        return pd.DataFrame()

def get_historical_data(symbol: str, date: str) -> pd.DataFrame:
    """
    指定されたシンボルと日付の履歴データ(日次OHLC)を取得し、DataFrameで返す。
    """
    try:
        # tm.historical は通常 DataFrame を返す (単一シンボル、単一日付の場合)
        # ただし、ドキュメントや過去の挙動からリストや辞書で返る可能性も考慮
        data = tm.historical(currency=symbol, date=date, interval='daily', fields=['open', 'high', 'low', 'close'])
        print(f"Type of historical data received: {type(data)}")
        print(f"Content of historical data: {data}")

        if isinstance(data, pd.DataFrame):
            # 日付列 'date' がインデックスになっていない場合があるため列として追加
            if 'date' not in data.columns and data.index.name == 'date':
                 data.reset_index(inplace=True)
            elif 'date' not in data.columns:
                 # date列もインデックスもない場合、引数の日付を追加
                 data['date'] = date
            return data
        elif isinstance(data, list) and data: # 複数シンボル指定した場合など
            df = pd.DataFrame(data)
            if 'date' not in df.columns: df['date'] = date # date列がない場合補完
            return df
        elif isinstance(data, dict) and data.get('date'): # 単一データが辞書で返るケース
             # 'date' キーがない場合は引数のdateを使用
            if 'date' not in data: data['date'] = date
            return pd.DataFrame([data])
        elif isinstance(data, dict) and 'message' in data: # エラーメッセージの場合
            print(f"API returned message for historical data ({symbol}, {date}): {data['message']}")
            return pd.DataFrame()
        else:
            print(f"Unexpected format or empty data received for historical data: {data}")
            return pd.DataFrame()

    except Exception as e:
        print(f"Error fetching historical data for {symbol} on {date}: {e}")
        return pd.DataFrame()


def get_time_series_data(symbol: str, start_date: str, end_date: str, interval: str = 'hourly') -> pd.DataFrame:
    """
    指定されたシンボル、期間、間隔の時系列データ(OHLC)を取得し、DataFrameで返す。
    """
    try:
        # tm.timeseries は DataFrame または エラーメッセージを含む辞書を返すことが多い
        data = tm.timeseries(currency=symbol, start=start_date, end=end_date, interval=interval, fields=['open', 'high', 'low', 'close'])
        print(f"Type of time-series data received: {type(data)}")
        # print(f"Content of time-series data: {data}") # 大量データの場合があるのでHeadのみ表示推奨

        if isinstance(data, pd.DataFrame):
            # 'date' 列がインデックスになっている場合があるので、列に戻す
            if 'date' not in data.columns and data.index.name == 'date':
                data.reset_index(inplace=True)
            print(f"Time-series DataFrame shape: {data.shape}")
            print(data.head())
            return data
        elif isinstance(data, dict) and 'quotes' in data: # APIが辞書形式('quotes'キー)でデータを返す場合
            df = pd.DataFrame(data['quotes'])
            print(f"Time-series DataFrame shape (from dict): {df.shape}")
            print(df.head())
            return df
        elif isinstance(data, dict) and 'message' in data: # APIがエラーメッセージを返す場合
            print(f"API returned message for time-series data ({symbol}): {data['message']}")
            return pd.DataFrame() # 空のDataFrameを返す
        else:
            print(f"Unexpected format or empty data received for time-series data: {data}")
            return pd.DataFrame()

    except Exception as e:
        print(f"Error fetching time-series data for {symbol} from {start_date} to {end_date}: {e}")
        return pd.DataFrame()

```

### `src/data_processor.py`

```
import pandas as pd
import os
import src.config as config # config をインポート
from datetime import datetime

def save_data_to_parquet(df: pd.DataFrame, data_type: str, filename_prefix: str) -> str | None:
    """
    DataFrameを指定されたデータタイプのディレクトリにParquet形式で保存する。
    時間列をdatetimeに変換し、インデックスに設定する。
    """
    if df is None or df.empty:
        print(f"Skipping save for {data_type}: DataFrame is None or empty.")
        return None

    data_dir = config.DATA_DIRS.get(data_type)
    if not data_dir:
        print(f"Error: Directory for data type '{data_type}' not found in config.")
        return None

    # ディレクトリが存在しない場合は作成
    os.makedirs(data_dir, exist_ok=True)

    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(data_dir, f"{filename_prefix}_{timestamp_str}.parquet")

    try:
        # 元のDataFrameを変更しないようにコピーを作成
        df_processed = df.copy()

        # 時間関連の列を特定 ('timestamp' または 'date')
        time_col = None
        if 'timestamp' in df_processed.columns:
            time_col = 'timestamp'
        elif 'date' in df_processed.columns:
            time_col = 'date'

        if time_col:
            # datetime型に変換 (エラーはNaTにする)
            df_processed[time_col] = pd.to_datetime(df_processed[time_col], errors='coerce')

            # NaTを含む行を除外するかどうかは要件による
            # ここではNaTがあってもインデックス設定を試みる
            # df_processed = df_processed.dropna(subset=[time_col])

            # NaTでない有効な時間データがある場合のみインデックスに設定
            if not df_processed[time_col].isnull().all():
                 # インデックスに設定する前にソートする（推奨）
                 df_processed = df_processed.sort_values(by=time_col)
                 df_processed = df_processed.set_index(time_col)
            else:
                 print(f"Warning: No valid datetime values found in column '{time_col}' for {filepath}. Not setting index.")

        # Parquetで保存
        df_processed.to_parquet(filepath, index=True) # インデックスも保存
        return filepath
    except Exception as e:
        print(f"Error saving data to {filepath}: {e}")
        return None

def save_real_time_data(data: pd.DataFrame, filename: str = "real_time_data") -> str | None:
    """リアルタイムデータをParquetで保存"""
    return save_data_to_parquet(data, "real_time", filename)

def save_historical_data(data: pd.DataFrame, filename: str = "historical_data") -> str | None:
    """履歴データをParquetで保存"""
    return save_data_to_parquet(data, "historical", filename)

def save_time_series_data(data: pd.DataFrame, filename: str = "time_series_data") -> str | None:
    """時系列データをParquetで保存"""
    return save_data_to_parquet(data, "time_series", filename)

```

### `src/main.py`

```
import os
from datetime import datetime, timedelta, timezone
import src.api_client as api_client # 修正: import  形式
import src.data_processor as data_processor # 修正: import  形式
import src.utils as utils # 修正: import  形式

if __name__ == "__main__":
    print("Starting script...")
    utils.create_directories()
    utils.verify_directories()

    if not utils.verify_api_key():
        exit(1) # APIキーがない場合は終了コード1で終了

    # --- Real-time data ---
    real_time_symbols = 'USOIL,XAUUSD,US30' # 取得したいシンボルをカンマ区切りで指定
    print(f"\nFetching real-time data for: {real_time_symbols}")
    real_time_df = api_client.get_real_time_data(real_time_symbols)

    if real_time_df is not None and not real_time_df.empty:
        print("Real-time data fetched successfully.")
        real_time_filepath = data_processor.save_real_time_data(real_time_df)
        if real_time_filepath:
            print(f"Real-time data saved to {real_time_filepath}")
        else:
            print("Failed to save real-time data.")
    else:
        print("No real-time data fetched or an error occurred.")

    # --- Historical data ---
    historical_symbol = 'XAUUSD' # 取得したいシンボルを指定
    # TraderMadeの履歴データはUTC基準の可能性があるため、UTCの昨日を取得
    # APIによってはローカルタイムゾーンの場合もあるため要確認
    yesterday_utc = datetime.now(timezone.utc).date() - timedelta(days=1)
    historical_date_str = yesterday_utc.strftime('%Y-%m-%d')
    print(f"\nFetching historical data for: {historical_symbol} on {historical_date_str}")
    historical_df = api_client.get_historical_data(historical_symbol, historical_date_str)

    if historical_df is not None and not historical_df.empty:
        print("Historical data fetched successfully.")
        historical_filepath = data_processor.save_historical_data(historical_df)
        if historical_filepath:
            print(f"Historical data saved to {historical_filepath}")
        else:
            print("Failed to save historical data.")
    else:
        print("No historical data fetched or an error occurred.")

    # --- Time-series data ---
    time_series_symbol = 'UKOIL' # 取得したいシンボルを指定
    # APIの仕様に合わせてUTCで日時を指定 (TraderMadeはGMT/UTC基準)
    now_utc = datetime.now(timezone.utc)
    # TraderMade timeseries APIは未来の日付を指定できないため、現在時刻以前をendとする
    # 少しマージンを持たせる（例：5分前）
    time_series_end_dt = now_utc - timedelta(minutes=5)
    time_series_end_dt_str = time_series_end_dt.strftime('%Y-%m-%d-%H:%M')
    # 8日前のデータを取得 (期間は必要に応じて調整)
    time_series_start_dt = time_series_end_dt - timedelta(days=8)
    time_series_start_dt_str = time_series_start_dt.strftime('%Y-%m-%d-%H:%M')
    time_series_interval = 'hourly' # 間隔を指定 (daily, hourly, minute)

    print(f"\nFetching time-series data for: {time_series_symbol}")
    print(f"Interval: {time_series_interval}")
    print(f"Start (UTC): {time_series_start_dt_str}")
    print(f"End (UTC): {time_series_end_dt_str}")
    time_series_df = api_client.get_time_series_data(
        time_series_symbol,
        time_series_start_dt_str,
        time_series_end_dt_str,
        interval=time_series_interval
    )

    # time_series_df が DataFrame であることを確認してから保存
    if time_series_df is not None and not time_series_df.empty:
        print("Time-series data fetched successfully.")
        time_series_filepath = data_processor.save_time_series_data(time_series_df)
        if time_series_filepath:
            print(f"Time-series data saved to {time_series_filepath}")
        else:
            print("Failed to save time-series data.")
    else:
        # APIからメッセージが返された場合などはapi_client内でprintされる
        print("No time-series data fetched or an error occurred (check API messages/limits).")

    print("\nScript finished.")

```

### `src/view.py` (オプション)

```
import os
import glob
import pandas as pd
import src.config as config # config をインポート
from IPython.display import display # IPython環境での表示用

def display_parquet_files(num_rows: int = 5):
    """
    config.pyで定義された各データディレクトリ内の最新Parquetファイルを表示する。
    Args:
        num_rows (int): 各DataFrameの先頭から表示する行数。
    """
    print("Displaying latest Parquet files...")
    for data_type, data_type_dir in config.DATA_DIRS.items():
        print(f"\n--- {data_type.upper()} Data ---")
        print(f"Directory: {data_type_dir}")

        # ディレクトリ内のParquetファイルを検索
        parquet_files = glob.glob(os.path.join(data_type_dir, "*.parquet"))

        if not parquet_files:
            print("No Parquet files found in this directory.")
            continue

        # 更新日時が最新のファイルを取得
        try:
            latest_file = max(parquet_files, key=os.path.getmtime)
            print(f"Latest File: {os.path.basename(latest_file)}")

            df = pd.read_parquet(latest_file)
            print(f"Shape: {df.shape}")
            # インデックスが存在するか確認してから表示
            if df.index is not None:
                 print(f"Index Name: {df.index.name}, Index Type: {type(df.index)}")
            else:
                 print("Index: Not set or default RangeIndex")
            print(f"Columns: {df.columns.tolist()}")
            print(f"Head ({num_rows} rows):")
            display(df.head(num_rows)) # IPython環境できれいに表示

        except ValueError: # ファイルが見つからない場合 (globが空リストを返す)
            print("No Parquet files found to determine the latest.")
        except Exception as e:
            print(f"Error reading or displaying {latest_file}: {e}")


if __name__ == "__main__":
    # Jupyter NotebookやIPython環境で実行することを推奨
    # コマンドラインから python src/view.py で実行しても良いが、
    # display() の出力が最適化されない場合がある
    display_parquet_files(num_rows=5) # 表示行数を指定可能
```

## 5. 実行方法

1.  **仮想環境の作成とアクティベート:**
    ```
    # プロジェクトルート (tradermade_cfd ディレクトリ) に移動
    cd path/to/tradermade_cfd

    # 仮想環境を作成
    python -m venv .venv

    # 仮想環境をアクティベート (Windows)
    .\.venv\Scripts\activate
    # (macOS/Linux)
    # source .venv/bin/activate
    ```

2.  **依存ライブラリのインストール:**
    ```
    pip install -r requirements.txt
    ```

3.  **APIキーの設定:** 上記「2. APIキー設定 (Windows環境変数)」を参照して `TRADERMADE_API_KEY` を設定してください。

4.  **メインスクリプトの実行:**
    ```
    # 仮想環境がアクティブな状態で実行
    python src/main.py
    ```
    実行すると、APIからデータが取得され、`output` ディレクトリ以下の各サブディレクトリに Parquet ファイルとして保存されます。コンソールに出力されるログで処理状況を確認できます。

5.  **保存されたデータの確認 (オプション):**
    IPythonコンソールやJupyter Notebookで以下のように実行すると、各データディレクトリの最新のParquetファイルの内容が表示されます。
    ```
    # IPython や Jupyter Notebook で
    import sys
    # src ディレクトリをパスに追加 (プロジェクトルートから実行する場合)
    sys.path.append('src')
    import src.view as view # import  形式
    view.display_parquet_files()
    ```
    または、コマンドラインから（表示形式は最適化されない可能性があります）:
    ```
    python src/view.py
    ```

```

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/d950b078-29c1-4b09-bcbe-059e1201e7a1/absolute_rules.md
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/5ba4f6c7-03c3-4292-88b9-460575f8e4d7/get_data_docs.md
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/f151da75-b071-4a4b-91b7-25f7494d3577/tradermade_documentation.md
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/b7a3b02c-d689-45d4-8cff-3a4e5339be22/data_processor.py
[5] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/5a308400-4204-4717-81c1-d0ce6cebf968/utils.py
[6] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/2073704d-4d0d-43b0-9946-7e6e78fdb065/view.py
[7] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/a3faf86b-05a4-4bf4-a569-c16f8072954d/main.py
[8] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/bc1fa7c8-39a2-49ab-9d95-3e94ea268560/config.py
[9] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/8500a3a7-ca6a-4dd4-a560-b1f96977dcd0/api_client.py

---
Perplexity の Eliot より: pplx.ai/share