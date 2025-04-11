# 計画

1.  `src/main.py`で、`time_series_end_date`を現在の日付に変更します。
2.  `time_series_start_date`と`time_series_end_date`の形式が、APIの要件を満たしていることを確認します。
3.  APIが正常なレスポンスを返すかどうかを確認します。

## 変更内容

```diff
--- a/src/main.py
+++ b/src/main.py
@@ -27,7 +27,7 @@
 
  # Time-series data
  time_series_symbol = 'UKOIL'
- time_series_end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d-%H:%M')
+ time_series_end_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
  time_series_start_date = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d-%H:%M')
  time_series_data = get_time_series_data(time_series_symbol, time_series_start_date, time_series_end_date)
  print(f"Type of time_series_data: {type(time_series_data)}")