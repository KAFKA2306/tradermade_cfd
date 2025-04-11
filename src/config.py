import os
from dotenv import load_dotenvpi

# Load environment variables from .env file
load_dotenv()

# --- Base Configuration ---
BASE_DIR = r"M:\ML\Finance\tradermade_cfd" # Modify this path if necessary
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# --- API Key ---
# Set API Key in .env file
# TRADERMADE_API_KEY=YOUR_API_KEY
API_KEY = os.getenv("TRADERMADE_API_KEY")

# --- Output Directories ---
REAL_TIME_DIR = os.path.join(OUTPUT_DIR, "real_time_data")
HISTORICAL_DIR = os.path.join(OUTPUT_DIR, "historical_data")
TIME_SERIES_DIR = os.path.join(OUTPUT_DIR, "time_series_data")
PROCESSED_METRICS_DIR = os.path.join(OUTPUT_DIR, "processed_metrics")
INDICATOR_DIR = os.path.join(OUTPUT_DIR, "indicators") # indicator_calculator.py で使用

# List of directories to create
ALL_DIRS = [
    OUTPUT_DIR,
    REAL_TIME_DIR,
    HISTORICAL_DIR,
    TIME_SERIES_DIR,
    PROCESSED_METRICS_DIR,
    INDICATOR_DIR # リストに追加
] # 閉じ括弧を追加

# --- Tickers for Processing ---
# Define which ticker represents spot and which represents futures (or CFD to proxy futures)
# This needs adjustment based on available data and desired analysis
SPOT_TICKER = 'XAUUSD' # Example: Gold Spot
FUTURES_TICKER = 'USOIL' # Example: WTI Crude Oil CFD as futures proxy
