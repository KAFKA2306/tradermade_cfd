import os

API_KEY = os.environ.get('TRADERMADE_API_KEY')

BASE_DIR = "m:/ML/Finance/tradermade_cfd"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

REAL_TIME_DIR = os.path.join(OUTPUT_DIR, "real_time_data")
HISTORICAL_DIR = os.path.join(OUTPUT_DIR, "historical_data")
TIME_SERIES_DIR = os.path.join(OUTPUT_DIR, "time_series_data")

def create_directories():
    """
    必要なディレクトリを作成する。
    """
    os.makedirs(REAL_TIME_DIR, exist_ok=True)
    os.makedirs(HISTORICAL_DIR, exist_ok=True)
    os.makedirs(TIME_SERIES_DIR, exist_ok=True)

DATA_TYPES = ["real_time_data", "historical_data", "time_series_data", "combined_data"]
