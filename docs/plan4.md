# 計画

1.  `src/utils.py`から`DATA_DIRS`のインポートを削除し、`create_directories`関数と`verify_directories`関数を修正して、`config`から個別のディレクトリ変数を直接インポートするように変更します。

## 変更内容

### src/utils.py

```diff
--- a/src/utils.py
+++ b/src/utils.py
@@ -1,23 +1,23 @@
 import os
-from config import BASE_DIR, OUTPUT_DIR, DATA_DIRS
+import config
  
 def create_directories():
- os.makedirs(BASE_DIR, exist_ok=True)
- os.makedirs(OUTPUT_DIR, exist_ok=True)
- for data_dir in DATA_DIRS.values():
- os.makedirs(data_dir, exist_ok=True)
+    os.makedirs(config.BASE_DIR, exist_ok=True)
+    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
+    os.makedirs(config.REAL_TIME_DIR, exist_ok=True)
+    os.makedirs(config.HISTORICAL_DIR, exist_ok=True)
+    os.makedirs(config.TIME_SERIES_DIR, exist_ok=True)
  
 def verify_directories():
- print(f"BASE_DIR: {BASE_DIR}")
- print(f"OUTPUT_DIR: {OUTPUT_DIR}")
- for data_type, data_dir in DATA_DIRS.items():
- print(f"{data_type} directory: {data_dir}")
+    print(f"BASE_DIR: {config.BASE_DIR}")
+    print(f"OUTPUT_DIR: {config.OUTPUT_DIR}")
+    print(f"REAL_TIME_DIR: {config.REAL_TIME_DIR}")
+    print(f"HISTORICAL_DIR: {config.HISTORICAL_DIR}")
+    print(f"TIME_SERIES_DIR: {config.TIME_SERIES_DIR}")
  
 def verify_api_key():
- api_key = os.environ.get("TRADERMADE_API_KEY")
- if not api_key:
- print("TRADERMADE_API_KEY is not set. Please set the environment variable.")
- return False
- return True
+    api_key = os.environ.get("TRADERMADE_API_KEY")
+    if not api_key:
+        print("TRADERMADE_API_KEY is not set. Please set the environment variable.")
+        return False
+    return True