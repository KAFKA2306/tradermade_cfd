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
├── .env                    # 環境変数ファイル
└── requirements.txt        # 依存ライブラリリスト
```

## 2. APIキー設定

TraderMade APIキーを `.env` ファイルに設定します。

1.  プロジェクトルートに `.env` ファイルを作成します。
2.  `.env` ファイルに以下の行を追加し、`YOUR_API_KEY` を実際のキーに置き換えます。

    ```
    TRADERMADE_API_KEY=YOUR_API_KEY
    ```

`src/config.py` で `.env` ファイルを読み込むように設定します。

## 3. `requirements.txt`

```
pandas==1.5.3
pyarrow==10.0.1
tradermade==0.2.0
ipython==8.5.0
python-dotenv==0.21.0
```

## 4. ソースコード (`src` ディレクトリ)

### `src/config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

# 注意: このパスはユーザーの環境に合わせて変更してください
# 例: BASE_DIR = r"C:/Users/YourUser/Projects/tradermade_cfd"
BASE_DIR = r"M:/ML/Finance/tradermade_cfd"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

DATA_DIRS = {
    "real_time": os.path.join(OUTPUT_DIR, "real_time_data"),
    "historical": os.path.join(OUTPUT_DIR, "historical_data"),
    "time_series": os.path.join(OUTPUT_DIR, "time_series_data"),
}

API_KEY = os.getenv("TRADERMADE_API_KEY")

def verify_api_key():
    if not API_KEY:
        print("Error: TRADERMADE_API_KEY environment variable is not set.")
        print("Please set the environment variable 'TRADERMADE_API_KEY' in .env file.")
        return False
    else:
        print(f"TRADERMADE_API_KEY found (starts with: {API_KEY[:4]}...).")
        return True
```

### `src/api_client.py`

```python
import os
import pandas as pd
import tradermade as tm
import src.config as config

if config.API_KEY:
    tm.set_rest_api_key(config.API_KEY)
else:
    print("Warning: TRADERMADE_API_KEY environment variable not set. API calls will likely fail.")

def get_real_time_data(symbols: str) -> pd.DataFrame:
    """
    指定されたシンボルのリアルタイムデータを取得し、DataFrameで返す。
    """
    try:
        data = tm.live(currency=symbols, fields=['bid', 'mid', 'ask'])
        print(f"Type of real-time data received: {type(data)}")
        print(f"Content of real-time data: {data}")

        if isinstance(data, list) and data:
            df = pd.DataFrame(data)
            if 'instrument' not in df.columns:
                symbol_list = [s.strip() for s in symbols.split(',')]
                if len(df) == len(symbol_list):
                    df['instrument'] = symbol_list
                else:
                    print(f"Warning: Row count ({len(df)}) doesn't match symbol count ({len(symbol_list)}). Cannot reliably assign instruments.")
                    df['instrument'] = 'Unknown'
            return df
        elif isinstance(data, dict) and 'quotes' in data:
             df = pd.DataFrame(data['quotes'])
             if 'instrument' not in df.columns:
                 symbol_list = [s.strip() for s in symbols.split(',')]
                 if len(df) == len(symbol_list):
                     df['instrument'] = symbol_list
                 else:
                     print(f"Warning: Row count ({len(df)}) doesn't match symbol count ({len(symbol_list)}). Cannot reliably assign instruments.")
                     df['instrument'] = 'Unknown'
             return df
        elif isinstance(data, dict) and 'message' in data:
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
        data = tm.historical(currency=symbol, date=date, interval='daily', fields=['open', 'high', 'low', 'close'])
        print(f"Type of historical data received: {type(data)}")
        print(f"Content of historical data: {data}")

        if isinstance(data, pd.DataFrame):
            if 'date' not in data.columns and data.index.name == 'date':
                 data.reset_index(inplace=True)
            elif 'date' not in data.columns:
                 data['date'] = date
            return data
        elif isinstance(data, list) and data:
            df = pd.DataFrame(data)
            if 'date' not in df.columns: df['date'] = date
            return df
        elif isinstance(data, dict) and data.get('date'):
             if 'date' not in data: data['date'] = date
             return pd.DataFrame([data])
        elif isinstance(data, dict) and 'message' in data:
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
        data = tm.timeseries(currency=symbol, start=start_date, end=end_date, interval=interval, fields=['open', 'high', 'low', 'close'])
        print(f"Type of time-series data received: {type(data)}")
        # print(f"Content of time-series data: {data}") # 大量データの場合があるのでHeadのみ表示推奨

        if isinstance(data, pd.DataFrame):
            if 'date' not in data.columns and data.index.name == 'date':
                data.reset_index(inplace=True)
            print(f"Time-series DataFrame shape: {data.shape}")
            print(data.head())
            return data
        elif isinstance(data, dict) and 'quotes' in data:
            df = pd.DataFrame(data['quotes'])
            print(f"Time-series DataFrame shape (from dict): {df.shape}")
            print(df.head())
            return df
        elif isinstance(data, dict) and 'message' in data:
            print(f"API returned message for time-series data ({symbol}): {data['message']}")
            return pd.DataFrame()
        else:
            print(f"Unexpected format or empty data received for time-series data: {data}")
            return pd.DataFrame()

    except Exception as e:
        print(f"Error fetching time-series data for {symbol} from {start_date} to {end_date}: {e}")
        return pd.DataFrame()
```

### `src/data_processor.py`

```python
import pandas as pd
import os
import src.config as config
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

    os.makedirs(data_dir, exist_ok=True)

    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(data_dir, f"{filename_prefix}_{timestamp_str}.parquet")

    try:
        df_processed = df.copy()

        time_col = None
        if 'timestamp' in df_processed.columns:
            time_col = 'timestamp'
        elif 'date' in df_processed.columns:
            time_col = 'date'

        if time_col:
            df_processed[time_col] = pd.to_datetime(df_processed[time_col], errors='coerce')

            if not df_processed[time_col].isnull().all():
                 df_processed = df_processed.sort_values(by=time_col)
                 df_processed = df_processed.set_index(time_col)
            else:
                 print(f"Warning: No valid datetime values found in column '{time_col}' for {filepath}. Not setting index.")

        df_processed.to_parquet(filepath, index=True)
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

```python
import os
from datetime import datetime, timedelta, timezone
import src.api_client as api_client
import src.data_processor as data_processor
import src.utils as utils

if __name__ == "__main__":
    print("Starting script...")
    utils.create_directories()
    utils.verify_directories()

    if not utils.verify_api_key():
        exit(1)

    real_time_symbols = 'USOIL,XAUUSD,US30'
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

    historical_symbol = 'XAUUSD'
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

    time_series_symbol = 'UKOIL'
    now_utc = datetime.now(timezone.utc)
    time_series_end_dt = now_utc - timedelta(minutes=5)
    time_series_end_dt_str = time_series_end_dt.strftime('%Y-%m-%d-%H:%M')
    time_series_start_dt = time_series_end_dt - timedelta(days=8)
    time_series_start_dt_str = time_series_start_dt.strftime('%Y-%m-%d-%H:%M')
    time_series_interval = 'hourly'

    print(f"\nFetching time-series data for: {time_series_symbol}")
    print(f"Interval: {time_series_interval}")
    print(f"Start (UTC): {time_series_start_dt_str}")
    print(f"End (UTC): {time_series_end_dt_str}")
    time_series_df = api_client.get_time_series_data(
        time_series_symbol,