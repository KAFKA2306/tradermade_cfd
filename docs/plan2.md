# 計画

1.  `src/main.py`で、`time_series_data`の内容とキーを出力するように変更します。
2.  `src/data_processor.py`で、APIからのレスポンス形式に合わせて、`save_time_series_data`関数を修正します。

## 変更内容

```diff
--- a/src/main.py
+++ b/src/main.py
@@ -31,6 +31,7 @@
  time_series_data = get_time_series_data(time_series_symbol, time_series_start_date, time_series_end_date)
  print(f"Type of time_series_data: {type(time_series_data)}")
  print(f"Content of time_series_data: {time_series_data}")
+ print(f"Keys of time_series_data: {time_series_data.keys()}")
  if not isinstance(time_series_data, dict):
  time_series_filepath = save_time_series_data(time_series_data)
  print(f"Time-series data saved to {time_series_filepath}")
```

```diff
--- a/src/data_processor.py
+++ b/src/data_processor.py
@@ -16,5 +16,5 @@
 def save_time_series_data(data):
  output_dir = os.path.join(OUTPUT_DIR, 'time_series_data')
  filename = f"time_series_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
- df = pd.DataFrame(data['quotes'])
+ df = pd.DataFrame(data) # APIからのレスポンス形式に合わせて修正
  filepath = os.path.join(output_dir, filename)
  df.to_csv(filepath, index=False)
  return filepath