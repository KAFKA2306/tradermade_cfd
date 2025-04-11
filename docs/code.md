提供されたログとコードを分析した結果、いくつかのエラーが発生している原因を特定しました。特にAPIからの応答形式の処理と、環境変数の読み込みに関する問題が見られます。

以下に、これらの問題を修正した完全なコードを再度提示します。

**1. 環境変数の設定 (再確認)**

コマンドプロンプト (管理者権限**なし**) で以下を実行し、**コマンドプロンプトを再起動**してください。

```bash
setx TRADERMADE_API_KEY "あなたのAPIキー"
```

再起動後、`echo %TRADERMADE_API_KEY%` を実行してAPIキーが表示されるか確認してください。

**2. 修正後のPythonコード**

以下の内容で各 `.py` ファイルを**上書き**してください。

**`config.py`**
```python
# config.py
import os

# !!! ご自身の環境に合わせて BASE_DIR を設定してください !!!
BASE_DIR = r"m:/ML/Finance/tradermade_cfd" # 例: Windows
# BASE_DIR = "/path/to/your/project/tradermade_cfd" # 例: Linux/macOS

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REAL_TIME_DIR = os.path.join(OUTPUT_DIR, "real_time_data")
HISTORICAL_DIR = os.path.join(OUTPUT_DIR, "historical_data")
TIME_SERIES_DIR = os.path.join(OUTPUT_DIR, "time_series_data")

DATA_DIRS = {
    "real_time": REAL_TIME_DIR,
    "historical": HISTORICAL_DIR,
    "time_series": TIME_SERIES_DIR,
}

API_KEY = os.environ.get("TRADERMADE_API_KEY")
```

**`src/utils.py`**
```python
# src/utils.py
import os
from config import BASE_DIR, OUTPUT_DIR, DATA_DIRS, API_KEY

def create_directories():
    """必要なディレクトリを作成する"""
    try:
        os.makedirs(BASE_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        for data_dir in DATA_DIRS.values():
            os.makedirs(data_dir, exist_ok=True)
        print("Directories created/verified.")
    except OSError as e:
        print(f"Error creating directories: {e}")
        raise # ディレクトリ作成失敗は致命的なので例外を再送

def verify_directories():
    """設定されたディレクトリパスを表示する"""
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"OUTPUT_DIR: {OUTPUT_DIR}")
    for data_type, data_dir in DATA_DIRS.items():
        print(f"{data_type.replace('_', ' ').title()} Directory: {data_dir}")

def verify_api_key():
    """環境変数からAPIキーが読み込めているか確認する"""
    if not API_KEY:
        print("ERROR: TRADERMADE_API_KEY environment variable is not set.")
        print("Please set the environment variable and restart your terminal/IDE.")
        return False
    print("TRADERMADE_API_KEY found.")
    return True
```

**`src/api_client.py`**
```python
# src/api_client.py
import os
import tradermade as tm
import pandas as pd
from config import API_KEY

# --- API 初期化 ---
_api_initialized = False

def initialize_api():
    """Tradermade APIキーを設定する"""
    global _api_initialized
    if not API_KEY:
        print("API Key not found in environment variables. Cannot initialize API.")
        return False
    try:
        tm.set_rest_api_key(API_KEY)
        _api_initialized = True
        print("Tradermade API Key set successfully.")
        return True
    except Exception as e:
        print(f"Error initializing Tradermade API: {e}")
        return False

# --- データ取得関数 ---
def get_real_time_data(symbols):
    """リアルタイムデータを取得する"""
    if not _api_initialized:
        print("API not initialized. Call initialize_api() first.")
        return None
    try:
        # tm.live は成功時に DataFrame を返すことが多い
        data = tm.live(currency=symbols, fields=['bid', 'mid', 'ask'])
        print(f"Type of real-time data received: {type(data)}")
        # APIエラーの場合、DataFrameでない可能性もあるのでログ出力で確認
        if not isinstance(data, pd.DataFrame):
             print(f"Unexpected data format for real-time data: {data}")
        return data
    except Exception as e:
        print(f"Error getting real-time data for {symbols}: {e}")
        return None

def get_historical_data(symbol, date):
    """特定日の過去データを取得する"""
    if not _api_initialized:
        print("API not initialized. Call initialize_api() first.")
        return None
    try:
        # tm.historical は成功時に DataFrame、エラー時に dict を返すことがある
        data = tm.historical(currency=symbol, date=date, interval='daily', fields=['open', 'high', 'low', 'close'])
        print(f"Type of historical data received: {type(data)}")
        if isinstance(data, dict) and 'message' in data:
            print(f"API Error for historical data {symbol} on {date}: {data['message']}")
        elif not isinstance(data, pd.DataFrame):
             print(f"Unexpected data format for historical data: {data}")
        return data
    except Exception as e:
        print(f"Error getting historical data for {symbol} on {date}: {e}")
        return None

def get_time_series_data(symbol, start_date, end_date, interval='hourly'):
    """時系列データを取得する"""
    if not _api_initialized:
        print("API not initialized. Call initialize_api() first.")
        return None
    try:
        # tm.timeseries は成功時に dict {'quotes': [...]}, エラー時に dict {'message': '...'} を返す
        data = tm.timeseries(currency=symbol, start=start_date, end=end_date, interval=interval, fields=['open', 'high', 'low', 'close'])
        print(f"Type of time-series data received: {type(data)}")
        if isinstance(data, dict) and 'message' in data:
            print(f"API Error for time-series {symbol}: {data['message']}")
        elif not (isinstance(data, dict) and 'quotes' in data):
             print(f"Unexpected data format for time-series data: {data}")
        return data
    except Exception as e:
        print(f"Error getting time-series data for {symbol}: {e}")
        return None
```

**`src/data_processor.py`**
```python
# src/data_processor.py
import pandas as pd
import os
from config import DATA_DIRS
from datetime import datetime

def _save_dataframe_to_csv(df, filename_prefix, data_dir):
    """DataFrameを指定ディレクトリにCSVとして保存するヘルパー関数"""
    if not isinstance(df, pd.DataFrame) or df.empty:
        print(f"No data (or not a DataFrame) to save for {filename_prefix}.")
        return None
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(data_dir, f"{filename_prefix}_{timestamp}.csv")
        df.to_csv(filepath, index=False) # インデックスは保存しない場合が多い
        return filepath
    except Exception as e:
        print(f"Error saving data to {filepath}: {e}")
        return None

def save_real_time_data(data, filename="real_time_data", data_dir=DATA_DIRS["real_time"]):
    """リアルタイムデータ (DataFrame想定) をCSVに保存する"""
    if isinstance(data, pd.DataFrame):
        return _save_dataframe_to_csv(data, filename, data_dir)
    else:
        print(f"Skipping save: Real-time data is not a DataFrame (type: {type(data)}).")
        return None

def save_historical_data(data, filename="historical_data", data_dir=DATA_DIRS["historical"]):
    """過去データ (DataFrame想定) をCSVに保存する"""
    if isinstance(data, pd.DataFrame):
        return _save_dataframe_to_csv(data, filename, data_dir)
    else:
        # APIエラーでdictが返る場合などを考慮
        print(f"Skipping save: Historical data is not a DataFrame (type: {type(data)}).")
        return None

def save_time_series_data(data, filename="time_series_data", data_dir=DATA_DIRS["time_series"]):
    """時系列データ (dict={'quotes': [...]} 想定) をCSVに保存する"""
    if isinstance(data, dict) and 'quotes' in data:
        quotes_list = data['quotes']
        if not quotes_list: # quotesリストが空の場合
             print(f"Time-series data for {filename} contains an empty 'quotes' list. Skipping save.")
             return None
        try:
             df = pd.DataFrame(quotes_list)
             return _save_dataframe_to_csv(df, filename, data_dir)
        except Exception as e: # DataFrame変換エラーなど
            print(f"Error converting time-series 'quotes' to DataFrame: {e}")
            return None
    elif isinstance(data, dict) and 'message' in data:
        # APIエラーメッセージが表示されているはずなので、ここではスキップのみ通知
        print(f"Skipping save: Time-series data contains an API error message.")
        return None
    else:
        print(f"Skipping save: Time-series data is not in the expected format (dict with 'quotes' key) (type: {type(data)}).")
        return None
```

**`src/main.py`**
```python
# src/main.py
import os
import pandas as pd
from datetime import datetime, timedelta, timezone
from api_client import (
    initialize_api,
    get_real_time_data,
    get_historical_data,
    get_time_series_data
)
from data_processor import (
    save_real_time_data,
    save_historical_data,
    save_time_series_data
)
from utils import create_directories, verify_directories, verify_api_key

if __name__ == "__main__":
    try:
        create_directories()
        verify_directories()

        if not verify_api_key():
            exit(1) # APIキーがない場合は終了

        if not initialize_api():
            exit(1) # API初期化失敗時も終了

        # --- Real-time data ---
        print("\n--- Getting Real-time Data ---")
        real_time_symbols = 'USOIL,XAUUSD,US30'
        real_time_data = get_real_time_data(real_time_symbols)

        # 取得データがDataFrameか確認してから保存
        if isinstance(real_time_data, pd.DataFrame):
            real_time_filepath = save_real_time_data(real_time_data)
            if real_time_filepath:
                print(f"Real-time data saved to: {real_time_filepath}")
        else:
            print("Failed to get valid real-time data.")

        # --- Historical data ---
        print("\n--- Getting Historical Data ---")
        historical_symbol = 'XAUUSD'
        # APIはUTC基準のため、昨日の日付もUTC基準で取得
        historical_date_obj = datetime.now(timezone.utc) - timedelta(days=1)
        historical_date_str = historical_date_obj.strftime('%Y-%m-%d')
        print(f"Requesting historical data for {historical_symbol} on {historical_date_str} UTC")

        historical_data = get_historical_data(historical_symbol, historical_date_str)

        # 取得データがDataFrameか確認してから保存
        if isinstance(historical_data, pd.DataFrame):
            historical_filepath = save_historical_data(historical_data)
            if historical_filepath:
                print(f"Historical data saved to: {historical_filepath}")
        else:
             print("Failed to get valid historical data.") # エラーメッセージはapi_clientで出力済みの想定

        # --- Time-series data ---
        print("\n--- Getting Time-series Data ---")
        time_series_symbol = 'UKOIL'
        # APIはUTC基準。未来の日付を避けるためutcnow()を使用し、終了時刻を少し前にする
        now_utc = datetime.now(timezone.utc)
        # APIのデータ反映ラグを考慮し、5分前の時刻を終了時刻とする
        time_series_end_utc = now_utc - timedelta(minutes=5)
        # 7日前の時刻を開始時刻とする
        time_series_start_utc = time_series_end_utc - timedelta(days=7) # endから7日前

        time_series_end_str = time_series_end_utc.strftime('%Y-%m-%d-%H:%M')
        time_series_start_str = time_series_start_utc.strftime('%Y-%m-%d-%H:%M')

        print(f"Requesting time-series for {time_series_symbol} from {time_series_start_str} to {time_series_end_str} UTC (hourly)")
        time_series_data = get_time_series_data(
            time_series_symbol,
            time_series_start_str,
            time_series_end_str,
            interval='hourly'
        )

        # 取得データがdictで'quotes'キーを持つか確認してから保存
        if isinstance(time_series_data, dict) and 'quotes' in time_series_data:
             time_series_filepath = save_time_series_data(time_series_data)
             if time_series_filepath:
                print(f"Time-series data saved to: {time_series_filepath}")
        else:
            print("Failed to get valid time-series data.") # エラーメッセージはapi_clientで出力済みの想定

        print("\nScript finished successfully.")

    except Exception as e:
        # 予期せぬエラーをキャッチ
        import traceback
        print("\n--- An unexpected error occurred ---")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        print("Traceback:")
        traceback.print_exc()
        print("Script finished with errors.")
        exit(1)

```

**修正のポイント:**

1.  **API初期化**: `api_client.py` に `initialize_api()` を追加し、`main.py` の最初で呼び出すようにしました。これにより、APIキーが設定されてから各取得関数が実行されます。
2.  **データ型チェックの強化**:
    *   `main.py`: 各API取得関数 (`get_...`) の結果が期待される型 (DataFrame または `dict` で `'quotes'` キーを持つ) であるかを `isinstance` で確認してから、保存関数 (`save_...`) を呼び出すように修正しました。これにより、`ValueError` や `KeyError` を防ぎます。
    *   `data_processor.py`: 保存関数内でも再度 `isinstance` で型を確認し、予期しないデータ型が渡された場合にエラーを出さずにスキップするようにしました。
3.  **エラーメッセージ**: API呼び出し時にエラーが発生した場合 (`None` やエラー `dict` が返る場合)、`api_client.py` 内でエラー内容を出力するようにし、`main.py` では「有効なデータが取得できなかった」旨のメッセージを表示するように整理しました。
4.  **Time Seriesの日付**: `main.py` で `timeseries` の終了日時 (`end_date`) を現在時刻 (UTC) より少し前 (`timedelta(minutes=5)`) に設定し、`end_date in the future` エラーを回避するようにしました。開始日時は終了日時から計算するように変更しました。
5.  **環境変数チェック**: `utils.py` の `verify_api_key` で、キーが見つからない場合にエラーメッセージを表示し、`main.py` で `exit(1)` するようにしました。
6.  **全体のエラーハンドリング**: `main.py` の `if __name__ == "__main__":` ブロック全体を `try...except` で囲み、予期しないエラーが発生した場合にトレースバックを出力して終了するようにしました。

**実行手順:**

1.  上記のコードで各 `.py` ファイルを更新します。
2.  環境変数 `TRADERMADE_API_KEY` が正しく設定されていることを確認します (コマンドプロンプト再起動後に `echo %TRADERMADE_API_KEY%` で確認)。
3.  仮想環境がアクティブな状態で、コマンドプロンプトから `python src/main.py` を実行します。

これで、以前発生していたエラーが解消され、データが正しく取得・保存されるはずです。

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/b3e843fc-a540-449a-b70f-6773ea63ce8b/paste.txt
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/f1efdcda-2300-4e3a-b889-ca900ba653eb/api_client.py
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/dce859c7-0b9d-4a41-8078-fd9f9658d128/data_processor.py
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/caac0b25-0c0a-41ed-b15d-f4a47b42cb85/view.py
[5] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/b4e26f9d-3c9a-480a-9d8a-31a37bed8d94/main.py
[6] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/a2aa930e-22c1-4044-a205-0e9e78b6cb4c/utils.py
[7] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/7a9df052-e509-4c9e-969c-1821153d91dd/config.py
[8] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/482945dc-3516-46d5-9b41-620866f25c62/tradermade_documentation.md

---
Perplexity の Eliot より: pplx.ai/share