import os
import pandas as pd
import datetime
import config
import data_processor # data_processor をインポート

def calculate_basis_z_score(df, window=20, min_periods=1):
    """
    ローリングウィンドウを使用してベーシスZスコアを計算する。

    Args:
        df (pd.DataFrame): 'basis' 列を含むDataFrame。インデックスは時系列推奨。
        window (int): ローリング計算のウィンドウサイズ。
        min_periods (int): 計算に必要な最小期間数。

    Returns:
        pd.DataFrame: 'basis_z_score' 列が追加されたDataFrame。
    """
    if 'basis' not in df.columns:
        print("Error: 'basis' column not found. Cannot calculate Z-score.")
        df['basis_z_score'] = pd.NA # またはエラーを発生させる
        return df

    # ローリング平均と標準偏差を計算
    rolling_mean = df['basis'].rolling(window=window, min_periods=min_periods).mean()
    rolling_std = df['basis'].rolling(window=window, min_periods=min_periods).std()

    # 標準偏差が0またはNaNの場合のZスコアを処理
    # Zスコア = (現在の値 - ローリング平均) / ローリング標準偏差
    # rolling_std が 0 や NaN の場合は Z スコアも NaN になるようにする
    df['basis_z_score'] = (df['basis'] - rolling_mean) / rolling_std
    # オプション: 標準偏差が非常に小さい場合にZスコアが発散するのを防ぐ
    # df['basis_z_score'] = df['basis_z_score'].fillna(0) # 例: NaNを0で埋める

    print(f"Calculated rolling basis Z-score with window={window}, min_periods={min_periods}.")
    return df

def calculate_indicators(input_data_type='processed', window_size=20):
    """
    指定されたタイプの最新データから指標を計算し、Parquet形式で保存する。

    Args:
        input_data_type (str): 読み込むデータのタイプ ('processed' など)。
        window_size (int): Zスコア計算のローリングウィンドウサイズ。
    """
    print(f"--- Starting Indicator Calculation (Input: {input_data_type}, Window: {window_size}) ---")

    # data_processor を使って最新の処理済みメトリクスデータを読み込む
    # 注意: calculate_metrics は通常1行のDFを生成するため、
    #       時系列分析を行うには、過去のメトリクスを結合したファイルが必要になる。
    #       ここでは、仮に最新ファイルに複数行データがあると仮定して進める。
    #       もし1行しかない場合は、ローリング計算は意味をなさない。
    input_df = data_processor.read_latest_parquet(input_data_type)

    if input_df is None or input_df.empty:
        print(f"No data found for type '{input_data_type}'. Cannot calculate indicators.")
        return

    # 必要な列が存在するか確認 (data_processor.calculate_metrics の出力に合わせる)
    required_cols = ['futures_price', 'spot_price']
    if not all(col in input_df.columns for col in required_cols):
        print(f"Required columns ({required_cols}) not found in the input data.")
        # basis 列が直接存在する場合もあるかもしれないのでチェック
        if 'basis' not in input_df.columns:
             print("And 'basis' column is also missing. Cannot proceed.")
             return
        else:
             print("Found 'basis' column, will proceed with Z-score calculation.")

    # basis 列がない場合は計算する
    if 'basis' not in input_df.columns:
         try:
            input_df['basis'] = input_df['futures_price'] - input_df['spot_price']
         except Exception as e:
             print(f"Error calculating 'basis' column: {e}")
             return

    # --- Zスコア計算 ---
    # データがウィンドウサイズ以上あるか確認
    if len(input_df) >= window_size:
         print(f"Calculating Basis Z-Score with window {window_size}...")
         indicator_df = calculate_basis_z_score(input_df.copy(), window=window_size, min_periods=max(1, window_size // 2)) # min_periods調整
    elif len(input_df) > 1:
         print(f"Input data has {len(input_df)} rows, less than window size {window_size}. Calculating Z-score with available data.")
         indicator_df = calculate_basis_z_score(input_df.copy(), window=len(input_df), min_periods=1) # 可能な範囲で計算
    else:
         print("Input data has only one row. Skipping rolling Z-score calculation.")
         # Zスコア列をNaNで追加しておく
         input_df['basis_z_score'] = pd.NA
         indicator_df = input_df.copy()


    # --- 他の指標の計算 (例) ---
    # if 'spot_price' in indicator_df.columns:
    #     print("Calculating Spot Price SMA...")
    #     indicator_df['spot_sma'] = indicator_df['spot_price'].rolling(window=window_size, min_periods=1).mean()


    # --- 結果を保存 ---
    if indicator_df is not None and not indicator_df.empty:
        # 保存には data_processor.save_dataframe_to_parquet を使う
        filepath = data_processor.save_dataframe_to_parquet(
            indicator_df,
            "indicator", # 保存先のタイプ
            f"indicator_data_w{window_size}" # ファイル名にウィンドウサイズを含める
        )
        if filepath:
             print(f"Indicator data saved to {filepath}")
        else:
             print("Failed to save indicator data.")
    else:
         print("No indicator data generated to save.")

    print("--- Indicator Calculation Complete ---")


if __name__ == "__main__":
    # 例: 最新の処理済みメトリクスファイルに対して指標計算する場合
    # 注意: このファイルが時系列データを含んでいる必要がある
    calculate_indicators(input_data_type='processed', window_size=20)

    # もし過去のメトリクスを結合したファイルがあるなら、それを指定する
    # integrated_metrics_df = data_processor.read_latest_parquet('processed', filename_pattern='all_metrics_*.parquet') # 仮のパターン
    # if integrated_metrics_df is not None:
    #     calculate_indicators(input_df=integrated_metrics_df, window_size=20) # 関数に入力DFを渡すように変更が必要