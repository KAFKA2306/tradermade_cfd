import pandas as pd
import os
from datetime import datetime
import config
 
def save_real_time_data(data, filename="real_time_data", data_dir=config.REAL_TIME_DIR):
    df = pd.DataFrame(data)
    filepath = os.path.join(data_dir, f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet")
    df.to_parquet(filepath)
    return filepath
 
def save_historical_data(data, filename="historical_data", data_dir=config.HISTORICAL_DIR):
    df = pd.DataFrame(data)
    filepath = os.path.join(data_dir, f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet")
    df.to_parquet(filepath)
    return filepath
 
def save_time_series_data(data, filename="time_series_data", data_dir=config.TIME_SERIES_DIR):
    df = pd.DataFrame(data) # APIからのレスポンス形式に合わせて修正
    filepath = os.path.join(data_dir, f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet")
    df.to_parquet(filepath)
    return filepath