import os
import glob
import pandas as pd
import datetime
import config

def integrate_data():
    """
    複数の parquet ファイルを読み込み、統合する。
    """
    all_data = []
    
    # リアルタイムデータ
    real_time_files = glob.glob(os.path.join(config.REAL_TIME_DIR, "*.parquet"))
    for file in real_time_files:
        try:
            df = pd.read_parquet(file)
            df['data_type'] = 'real_time'
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    # ヒストリカルデータ
    historical_files = glob.glob(os.path.join(config.HISTORICAL_DIR, "*.parquet"))
    for file in historical_files:
        try:
            df = pd.read_parquet(file)
            df['data_type'] = 'historical'
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    # タイムシリーズデータ
    time_series_files = glob.glob(os.path.join(config.TIME_SERIES_DIR, "*.parquet"))
    for file in time_series_files:
        try:
            df = pd.read_parquet(file)
            df['data_type'] = 'time_series'
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if all_data:
        integrated_df = pd.concat(all_data, ignore_index=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # ディレクトリが存在することを確認
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        
        file_path = os.path.join(config.OUTPUT_DIR, f"integrated_data_{timestamp}.parquet")
        integrated_df.to_parquet(file_path)
        print(f"Integrated data saved to {file_path}")
    else:
        print("No data to integrate.")

if __name__ == "__main__":
    integrate_data()