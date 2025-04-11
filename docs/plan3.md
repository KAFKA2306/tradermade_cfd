# 計画

1.  `src`ディレクトリ以下に、`file_manager.py`というファイルを作成し、データの入出力処理を記述します。
2.  `config.py`で、`BASE_DIR`、`OUTPUT_DIR`、およびデータの種類ごとのディレクトリを定義します。
3.  `config.py`で、一連のディレクトリを生成する関数を定義します。
4.  `src/main.py`で、`file_manager.py`をインポートし、データの入出力処理を`file_manager.py`に委譲します。
5.  `src/main.py`で、`from .`のような相対インポートを修正します。
6.  データの入出力形式をParquet形式に変更します。
7.  時間の列を標準的なdatetime形式でindexに設定します。
8.  コメントを削除します。

## 変更内容

### src/file_manager.py (新規作成)

```python
import os
import pandas as pd

def save_data(data, filepath):
    """
    データをParquet形式で保存する。

    Args:
        data (pd.DataFrame): 保存するデータ。
        filepath (str): 保存先のファイルパス。
    """
    data.to_parquet(filepath)

def load_data(filepath):
    """
    Parquet形式のデータを読み込む。

    Args:
        filepath (str): 読み込むファイルのパス。

    Returns:
        pd.DataFrame: 読み込んだデータ。
    """
    return pd.read_parquet(filepath)
```

### config.py

```diff
--- a/src/config.py
+++ b/src/config.py
@@ -1,4 +1,20 @@
 import os
 
 API_KEY = os.environ.get('TRADERMADE_API_KEY')
+
+BASE_DIR = "m:/ML/Finance/tradermade_cfd"
+OUTPUT_DIR = os.path.join(BASE_DIR, "output")
+
+REAL_TIME_DIR = os.path.join(OUTPUT_DIR, "real_time_data")
+HISTORICAL_DIR = os.path.join(OUTPUT_DIR, "historical_data")
+TIME_SERIES_DIR = os.path.join(OUTPUT_DIR, "time_series_data")
+
+def create_directories():
+    """
+    必要なディレクトリを作成する。
+    """
+    os.makedirs(REAL_TIME_DIR, exist_ok=True)
+    os.makedirs(HISTORICAL_DIR, exist_ok=True)
+    os.makedirs(TIME_SERIES_DIR, exist_ok=True)
+
```

### src/main.py

```diff
--- a/src/main.py
+++ b/src/main.py
@@ -1,10 +1,10 @@
 import os
 from datetime import datetime, timedelta
-from api_client import get_real_time_data, get_historical_data, get_time_series_data
-from data_processor import save_real_time_data, save_historical_data, save_time_series_data
-from utils import create_directories, verify_directories, verify_api_key
+import api_client
+import data_processor
+import utils
+import config
+import file_manager
  
 if __name__ == "__main__":
  create_directories()
  verify_directories()
  if not verify_api_key():
  exit()
 
  # Real-time data
  real_time_symbols = 'USOIL,XAUUSD,US30'
  real_time_data = get_real_time_data(real_time_symbols)
  if real_time_data:
  real_time_filepath = save_real_time_data(real_time_data)
  print(f"Real-time data saved to {real_time_filepath}")
 
  # Historical data
  historical_symbol = 'XAUUSD'
  historical_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
  historical_data = get_historical_data(historical_symbol, historical_date)
  if not historical_data.empty:
  historical_filepath = save_historical_data(historical_data)
  print(f"Historical data saved to {historical_filepath}")
 
  # Time-series data
  time_series_symbol = 'UKOIL'
  time_series_end_date = datetime.utcnow().strftime('%Y-%m-%d-%H:%M')
  time_series_start_date = (datetime.utcnow() - timedelta(days=8)).strftime('%Y-%m-%d-%H:%M')
  time_series_data = get_time_series_data(time_series_symbol, time_series_start_date, time_series_end_date)
  print(f"Type of time_series_data: {type(time_series_data)}")
  print(f"Content of time_series_data: {time_series_data}")
  print(f"Keys of time_series_data: {time_series_data.keys()}")
  if not isinstance(time_series_data, dict):
  time_series_filepath = save_time_series_data(time_series_data)
  print(f"Time-series data saved to {time_series_filepath}")