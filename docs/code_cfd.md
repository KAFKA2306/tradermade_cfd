```python
# config.py
import os

# --- Base Configuration ---
BASE_DIR = r"E:/e/d" # Modify this path if necessary
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# --- API Key ---
# Set API Key via environment variables
# Temporary (current cmd session): set TRADERMADE_API_KEY=YOUR_API_KEY
# Permanent (system-wide, requires cmd restart): setx TRADERMADE_API_KEY "YOUR_API_KEY" /M
# Permanent (user-level, requires cmd restart): setx TRADERMADE_API_KEY "YOUR_API_KEY"
API_KEY = os.environ.get('TRADERMADE_API_KEY')

# --- Output Directories ---
REAL_TIME_DIR = os.path.join(OUTPUT_DIR, "real_time_data")
HISTORICAL_DIR = os.path.join(OUTPUT_DIR, "historical_data")
TIME_SERIES_DIR = os.path.join(OUTPUT_DIR, "time_series_data")
PROCESSED_METRICS_DIR = os.path.join(OUTPUT_DIR, "processed_metrics")

# List of directories to create
ALL_DIRS = [
    OUTPUT_DIR,
    REAL_TIME_DIR,
    HISTORICAL_DIR,
    TIME_SERIES_DIR,
    PROCESSED_METRICS_DIR
]

# --- Tickers for Processing ---
# Define which ticker represents spot and which represents futures (or CFD to proxy futures)
# This needs adjustment based on available data and desired analysis
SPOT_TICKER = 'XAUUSD' # Example: Gold Spot
FUTURES_TICKER = 'USOIL' # Example: WTI Crude Oil CFD as futures proxy

```

```python
# src/__init__.py
# This file can be empty, it marks the directory as a Python package.
```

```python
# src/utils.py
import os
import config

def create_directories():
    """Creates all necessary output directories defined in config."""
    print("Creating directories...")
    for directory in config.ALL_DIRS:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Directory created or already exists: {directory}")
        except OSError as e:
            print(f"Error creating directory {directory}: {e}")
            raise # Stop execution if directories cannot be created

def verify_api_key_environment():
    """Checks if the API key is set in environment variables."""
    if not config.API_KEY:
        print("ERROR: TRADERMADE_API_KEY environment variable is not set.")
        print("Please set the key using 'set' (temporary) or 'setx' (permanent) in cmd.")
        return False
    print("TRADERMADE_API_KEY found in environment variables.")
    return True

```

```python
# src/api_client.py
import os
import tradermade as tm
import pandas as pd
from datetime import datetime, timedelta, timezone
import config

_api_initialized = False

def initialize_api():
    """Initializes the Tradermade API with the key from config."""
    global _api_initialized
    if not config.API_KEY:
        print("API Key not configured. Cannot initialize API.")
        return False
    try:
        tm.set_rest_api_key(config.API_KEY)
        _api_initialized = True
        print("Tradermade API initialized successfully.")
        return True
    except Exception as e:
        print(f"Error initializing Tradermade API: {e}")
        _api_initialized = False
        return False

def get_live_data(symbols):
    """Fetches live data for given symbols."""
    if not _api_initialized:
        print("API not initialized.")
        return None
    try:
        print(f"Fetching live data for: {symbols}")
        data = tm.live(currency=symbols, fields=['bid', 'mid', 'ask'])
        if isinstance(data, pd.DataFrame):
            return data
        elif isinstance(data, list): # Handle cases where API returns list
             return pd.DataFrame(data)
        elif isinstance(data, str): # Handle error string
            print(f"API Error (live): {data}")
            return None
        else:
            print(f"Unexpected live data format: {type(data)}")
            return None # Or try pd.DataFrame(data) if appropriate
    except Exception as e:
        print(f"Exception fetching live data for {symbols}: {e}")
        return None

def get_historical_data(symbol, days_back=1):
    """Fetches daily historical data for a symbol."""
    if not _api_initialized:
        print("API not initialized.")
        return None
    try:
        target_date = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime('%Y-%m-%d')
        print(f"Fetching historical data for {symbol} on {target_date}")
        data = tm.historical(currency=symbol, date=target_date, interval='daily', fields=['open', 'high', 'low', 'close'])
        if isinstance(data, pd.DataFrame):
            return data
        elif isinstance(data, dict) and 'message' in data:
            print(f"API Error (historical) for {symbol}: {data['message']}")
            return None
        else:
            # Sometimes returns a list containing a dict
            if isinstance(data, list) and len(data) == 1 and isinstance(data[0], dict):
                 # Check if it's an error message within the list/dict structure
                 if 'message' in data[0]:
                      print(f"API Error (historical) for {symbol}: {data[0]['message']}")
                      return None
                 else:
                      return pd.DataFrame(data) # Attempt to create DataFrame
            print(f"Unexpected historical data format for {symbol}: {type(data)}")
            return None
    except Exception as e:
        print(f"Exception fetching historical data for {symbol}: {e}")
        return None

def get_time_series_data(symbol, days=7, interval='hourly'):
    """Fetches time series data for a symbol."""
    if not _api_initialized:
        print("API not initialized.")
        return None
    try:
        end_dt_utc = datetime.now(timezone.utc) - timedelta(minutes=5) # Avoid future date issue
        start_dt_utc = end_dt_utc - timedelta(days=days)
        start_date_str = start_dt_utc.strftime('%Y-%m-%d-%H:%M')
        end_date_str = end_dt_utc.strftime('%Y-%m-%d-%H:%M')
        print(f"Fetching {interval} time series for {symbol} from {start_date_str} to {end_date_str} UTC")
        data = tm.timeseries(currency=symbol, start=start_date_str, end=end_date_str, interval=interval, fields=['open', 'high', 'low', 'close'])
        if isinstance(data, dict) and 'quotes' in data:
            return pd.DataFrame(data['quotes'])
        elif isinstance(data, dict) and 'message' in data:
            print(f"API Error (timeseries) for {symbol}: {data['message']}")
            return None
        else:
            print(f"Unexpected timeseries data format for {symbol}: {type(data)}")
            return None
    except Exception as e:
        print(f"Exception fetching time series data for {symbol}: {e}")
        return None

```

```python
# src/data_saver.py
import os
import pandas as pd
from datetime import datetime
import config

def save_dataframe_to_parquet(df, data_type_key, filename_prefix):
    """Saves a DataFrame to the appropriate directory as a Parquet file."""
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        print(f"No valid DataFrame provided for {filename_prefix}. Skipping save.")
        return None

    # Determine target directory from config based on key
    directory_map = {
        "real_time": config.REAL_TIME_DIR,
        "historical": config.HISTORICAL_DIR,
        "time_series": config.TIME_SERIES_DIR,
        "processed": config.PROCESSED_METRICS_DIR,
    }
    target_dir = directory_map.get(data_type_key)

    if not target_dir:
        print(f"Invalid data_type_key '{data_type_key}'. Cannot determine save directory.")
        return None

    # Ensure the directory exists (should have been created by utils)
    os.makedirs(target_dir, exist_ok=True)

    # Identify potential datetime columns and set index
    datetime_col = None
    if 'timestamp' in df.columns:
        datetime_col = 'timestamp'
    elif 'date' in df.columns:
        datetime_col = 'date'

    if datetime_col:
        try:
            # Convert to datetime, handling potential errors
            df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
            # Drop rows where conversion failed
            df.dropna(subset=[datetime_col], inplace=True)
            if not df.empty:
                 df = df.set_index(datetime_col)
            else:
                 print(f"DataFrame became empty after datetime conversion/dropna for {filename_prefix}. Skipping save.")
                 return None
        except Exception as e:
            print(f"Error processing datetime column '{datetime_col}' for {filename_prefix}: {e}. Proceeding without setting index.")
            # Continue without setting index if conversion fails critically

    # Generate filename and save
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = os.path.join(target_dir, f"{filename_prefix}_{timestamp_str}.parquet")

    try:
        print(f"Saving data to: {filepath}")
        df.to_parquet(filepath, engine='pyarrow') # or 'fastparquet' if installed
        return filepath
    except Exception as e:
        print(f"Error saving DataFrame to Parquet file {filepath}: {e}")
        return None

```

```python
# src/data_reader.py
import os
import glob
import pandas as pd
import config

def read_latest_parquet(data_type_key, filename_pattern="*.parquet"):
    """Reads the most recent Parquet file from the specified directory."""
    directory_map = {
        "real_time": config.REAL_TIME_DIR,
        "historical": config.HISTORICAL_DIR,
        "time_series": config.TIME_SERIES_DIR,
        "processed": config.PROCESSED_METRICS_DIR,
    }
    target_dir = directory_map.get(data_type_key)

    if not target_dir or not os.path.isdir(target_dir):
        print(f"Directory for data type '{data_type_key}' not found or invalid: {target_dir}")
        return None

    try:
        list_of_files = glob.glob(os.path.join(target_dir, filename_pattern))
        if not list_of_files:
            print(f"No Parquet files found in {target_dir} matching '{filename_pattern}'.")
            return None

        latest_file = max(list_of_files, key=os.path.getctime)
        print(f"Reading latest file: {latest_file}")
        df = pd.read_parquet(latest_file)
        return df
    except Exception as e:
        print(f"Error reading latest Parquet file from {target_dir}: {e}")
        return None

def read_all_parquet(data_type_key, filename_pattern="*.parquet"):
     """Reads all Parquet files from the specified directory and concatenates them."""
     directory_map = {
        "real_time": config.REAL_TIME_DIR,
        "historical": config.HISTORICAL_DIR,
        "time_series": config.TIME_SERIES_DIR,
        "processed": config.PROCESSED_METRICS_DIR,
     }
     target_dir = directory_map.get(data_type_key)

     if not target_dir or not os.path.isdir(target_dir):
        print(f"Directory for data type '{data_type_key}' not found or invalid: {target_dir}")
        return None

     all_files = glob.glob(os.path.join(target_dir, filename_pattern))
     if not all_files:
        print(f"No Parquet files found in {target_dir} matching '{filename_pattern}'.")
        return None

     df_list = []
     for f in all_files:
        try:
            df = pd.read_parquet(f)
            df_list.append(df)
        except Exception as e:
            print(f"Error reading file {f}: {e}. Skipping.")

     if not df_list:
         print("No dataframes could be read.")
         return None

     combined_df = pd.concat(df_list).sort_index() # Sort by datetime index
     print(f"Read and combined {len(df_list)} files from {target_dir}.")
     return combined_df
```

```python
# src/data_processor.py
import pandas as pd
import numpy as np
import config

def calculate_metrics(spot_df, futures_df, historical_basis_df=None):
    """
    Calculates specified metrics using spot, futures, and historical basis data.
    Assumes spot_df and futures_df contain the latest 'mid' prices for the respective tickers,
    indexed by datetime.
    """
    metrics = {}

    if spot_df is None or futures_df is None or spot_df.empty or futures_df.empty:
        print("Spot or Futures data is missing or empty. Cannot calculate metrics.")
        return None

    try:
        # Ensure dataframes are sorted by index (time)
        spot_df = spot_df.sort_index()
        futures_df = futures_df.sort_index()

        # Get the latest available price for each
        # We might need to align timestamps or use the absolute latest regardless of small time diffs
        latest_spot_time = spot_df.index.max()
        latest_futures_time = futures_df.index.max()

        # Use data closest to the most recent timestamp between the two
        latest_time = max(latest_spot_time, latest_futures_time)

        # Find rows closest to the latest time (using tolerance if needed, e.g., '1min')
        spot_price_row = spot_df.iloc[spot_df.index.get_indexer([latest_time], method='nearest')]
        futures_price_row = futures_df.iloc[futures_df.index.get_indexer([latest_time], method='nearest')]

        # Extract 'mid' price, handling potential missing values
        spot_price = spot_price_row['mid'].iloc[0] if not spot_price_row.empty and 'mid' in spot_price_row else np.nan
        futures_price = futures_price_row['mid'].iloc[0] if not futures_price_row.empty and 'mid' in futures_price_row else np.nan

        if pd.isna(spot_price) or pd.isna(futures_price):
             print("Could not extract valid spot or futures price. Aborting metrics calculation.")
             return None

        metrics['spot_price'] = spot_price
        metrics['futures_price'] = futures_price

        # --- Basis Calculations ---
        basis = futures_price - spot_price
        metrics['basis'] = basis

        if spot_price != 0:
            basis_rate = (basis / spot_price) * 100
            metrics['basis_rate_percent'] = basis_rate
        else:
            metrics['basis_rate_percent'] = np.nan

        # --- Placeholder/Simplified Calculations (Require More Data/Logic) ---
        # Annualized Basis: Needs futures expiry info, using a fixed 30-day placeholder
        metrics['annualized_basis_percent_30d'] = metrics.get('basis_rate_percent', np.nan) * (365.0 / 30.0)

        # Basis Z-Score: Needs historical basis data
        if historical_basis_df is not None and not historical_basis_df.empty and 'basis' in historical_basis_df.columns:
            try:
                basis_mean = historical_basis_df['basis'].mean()
                basis_std = historical_basis_df['basis'].std()
                if basis_std is not None and basis_std != 0:
                    metrics['basis_z_score'] = (basis - basis_mean) / basis_std
                else:
                    metrics['basis_z_score'] = np.nan # Avoid division by zero
            except Exception as e:
                print(f"Error calculating Z-score: {e}")
                metrics['basis_z_score'] = np.nan
        else:
            metrics['basis_z_score'] = np.nan # Not enough data

        # Market Regime: Placeholder logic based on basis sign
        if basis > 0:
            metrics['market_regime'] = 'Contango (Futures > Spot)'
        elif basis < 0:
            metrics['market_regime'] = 'Backwardation (Futures < Spot)'
        else:
            metrics['market_regime'] = 'Flat (Futures = Spot)'

        # Volatility-Adjusted Basis: Needs volatility calculation (historical prices)
        # Placeholder - requires historical spot/futures price series
        metrics['volatility_adjusted_basis'] = np.nan # Placeholder

        print("Calculated metrics:", metrics)
        # Convert metrics dict to DataFrame for saving
        metrics_df = pd.DataFrame([metrics])
        metrics_df['calculation_time'] = pd.Timestamp.now(tz='UTC')
        metrics_df = metrics_df.set_index('calculation_time')
        return metrics_df

    except Exception as e:
        print(f"An error occurred during metric calculation: {e}")
        import traceback
        traceback.print_exc()
        return None

def calculate_historical_basis(spot_hist_df, futures_hist_df):
    """Calculates historical basis from historical spot and futures DataFrames."""
    if spot_hist_df is None or futures_hist_df is None or spot_hist_df.empty or futures_hist_df.empty:
        print("Historical spot or futures data missing for basis calculation.")
        return None

    try:
        # Ensure datetime index
        spot_hist_df.index = pd.to_datetime(spot_hist_df.index)
        futures_hist_df.index = pd.to_datetime(futures_hist_df.index)

        # Use 'close' price for daily historical data, or 'mid' if available and more frequent
        spot_col = 'close' if 'close' in spot_hist_df.columns else 'mid'
        futures_col = 'close' if 'close' in futures_hist_df.columns else 'mid'

        # Align dataframes on index (time)
        aligned_df = pd.merge(spot_hist_df[[spot_col]], futures_hist_df[[futures_col]],
                              left_index=True, right_index=True, how='inner',
                              suffixes=('_spot', '_futures'))

        if aligned_df.empty:
            print("No overlapping timestamps found between historical spot and futures data.")
            return None

        aligned_df['basis'] = aligned_df[f'{futures_col}_futures'] - aligned_df[f'{spot_col}_spot']
        print(f"Calculated historical basis for {len(aligned_df)} points.")
        return aligned_df[['basis']] # Return only the basis column with datetime index

    except Exception as e:
        print(f"Error calculating historical basis: {e}")
        return None

```

```python
# src/main_fetch.py
import time
import config
import src.utils as utils
import src.api_client as api_client
import src.data_saver as data_saver

def run_fetch():
    """Main function to fetch and save data."""
    print("--- Starting Data Fetch ---")

    if not utils.verify_api_key_environment():
        return

    utils.create_directories() # Ensure directories exist

    if not api_client.initialize_api():
        return

    # --- Fetch Real-time Data ---
    # Define symbols needed for spot and futures (and potentially others)
    live_symbols_list = [config.SPOT_TICKER, config.FUTURES_TICKER, 'US30', 'DE40'] # Add more as needed
    live_symbols_str = ','.join(live_symbols_list)
    live_data_df = api_client.get_live_data(live_symbols_str)
    if live_data_df is not None:
        # Add a general filename prefix, specific ticker handling might be needed if saving separately
        data_saver.save_dataframe_to_parquet(live_data_df, "real_time", "live_prices")

    # --- Fetch Historical Data (e.g., for Z-score context) ---
    # Fetch for spot and futures tickers separately
    hist_spot_df = api_client.get_historical_data(config.SPOT_TICKER, days_back=1) # Yesterday's data
    if hist_spot_df is not None:
        data_saver.save_dataframe_to_parquet(hist_spot_df, "historical", f"{config.SPOT_TICKER}_daily")

    hist_futures_df = api_client.get_historical_data(config.FUTURES_TICKER, days_back=1)
    if hist_futures_df is not None:
        data_saver.save_dataframe_to_parquet(hist_futures_df, "historical", f"{config.FUTURES_TICKER}_daily")

    # --- Fetch Time Series Data (e.g., for volatility or finer basis history) ---
    # Fetch for spot and futures tickers separately (e.g., hourly for past week)
    ts_spot_df = api_client.get_time_series_data(config.SPOT_TICKER, days=7, interval='hourly')
    if ts_spot_df is not None:
        data_saver.save_dataframe_to_parquet(ts_spot_df, "time_series", f"{config.SPOT_TICKER}_hourly")

    ts_futures_df = api_client.get_time_series_data(config.FUTURES_TICKER, days=7, interval='hourly')
    if ts_futures_df is not None:
        data_saver.save_dataframe_to_parquet(ts_futures_df, "time_series", f"{config.FUTURES_TICKER}_hourly")

    print("--- Data Fetch Cycle Complete ---")

if __name__ == "__main__":
    run_fetch()
```

```python
# src/main_process.py
import config
import src.utils as utils
import src.data_reader as data_reader
import src.data_processor as data_processor
import src.data_saver as data_saver

def run_processing():
    """Main function to read data, calculate metrics, and save results."""
    print("--- Starting Data Processing ---")

    # Verify directories exist (optional, as fetch should create them)
    utils.create_directories()

    # --- Read Latest Live Data ---
    # Assumes live data for multiple symbols is saved in one file from main_fetch
    latest_live_df = data_reader.read_latest_parquet("real_time", filename_pattern="live_prices_*.parquet")

    if latest_live_df is None or latest_live_df.empty:
        print("Could not read latest live data. Cannot process metrics.")
        return

    # Filter data for specific spot and futures tickers
    # Note: 'instrument' column is expected from tm.live()
    if 'instrument' not in latest_live_df.columns:
         # If live data was saved differently (e.g., separate files per ticker),
         # need to adjust reading logic here.
         # For now, assume 'instrument' column exists.
         print("ERROR: 'instrument' column not found in live data. Cannot filter tickers.")
         # Fallback: try reading latest individual files if fetch saves them separately
         spot_live_df = data_reader.read_latest_parquet("real_time", filename_pattern=f"{config.SPOT_TICKER}_*.parquet") # Adjust pattern if needed
         futures_live_df = data_reader.read_latest_parquet("real_time", filename_pattern=f"{config.FUTURES_TICKER}_*.parquet") # Adjust pattern if needed
         if spot_live_df is None or futures_live_df is None:
              print("Could not read separate live data files for spot/futures.")
              return
    else:
         spot_live_df = latest_live_df[latest_live_df['instrument'] == config.SPOT_TICKER]
         futures_live_df = latest_live_df[latest_live_df['instrument'] == config.FUTURES_TICKER]


    if spot_live_df.empty or futures_live_df.empty:
         print(f"Live data for {config.SPOT_TICKER} or {config.FUTURES_TICKER} not found in the latest file.")
         return

    # --- Read Historical/Time Series Data for Context (e.g., Z-Score) ---
    # Read combined historical/timeseries data for spot and futures to calculate historical basis
    # Example: using hourly time series data for the last 7 days
    spot_ts_df = data_reader.read_latest_parquet("time_series", f"{config.SPOT_TICKER}_hourly_*.parquet")
    futures_ts_df = data_reader.read_latest_parquet("time_series", f"{config.FUTURES_TICKER}_hourly_*.parquet")

    historical_basis_df = None
    if spot_ts_df is not None and futures_ts_df is not None:
        historical_basis_df = data_processor.calculate_historical_basis(spot_ts_df, futures_ts_df)
        if historical_basis_df is not None:
             print("Successfully calculated historical basis for context.")
             # Optionally save this historical basis series
             # data_saver.save_dataframe_to_parquet(historical_basis_df, "processed", "historical_basis_series")
        else:
             print("Could not calculate historical basis.")
    else:
        print("Could not read sufficient time series data for historical basis calculation.")


    # --- Calculate Metrics ---
    metrics_df = data_processor.calculate_metrics(spot_live_df, futures_live_df, historical_basis_df)

    # --- Save Metrics ---
    if metrics_df is not None:
        data_saver.save_dataframe_to_parquet(metrics_df, "processed", "calculated_metrics")

    print("--- Data Processing Cycle Complete ---")


if __name__ == "__main__":
    run_processing()
```

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/d15a311f-f282-425f-a626-2bc7c3e5c769/utils.py
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/170bec48-4593-4de2-b8c2-e67492a691ee/data_processor.py
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/809eaaa6-0451-492e-bdef-8091aa46c243/main.py
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/77e34a2f-fffc-4e3c-a236-765d0e72a609/api_client.py
[5] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/2d20ad25-42bb-4aed-8b14-147218fa7b94/view.py
[6] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/52522745/5e1d4495-6acd-4409-a618-d425f197eb8d/config.py

---
Perplexity の Eliot より: pplx.ai/share