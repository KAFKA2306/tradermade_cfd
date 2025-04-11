import time
import config
import utils as utils
import api_client as api_client
import data_processor as data_processor

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
        data_processor.save_real_time_data(live_data_df)

    # --- Fetch Historical Data (e.g., for Z-score context) ---
    # Fetch for spot and futures tickers separately
    hist_spot_df = api_client.get_historical_data(config.SPOT_TICKER, days_back=1) # Yesterday's data
    if hist_spot_df is not None:
        data_processor.save_historical_data(hist_spot_df)

    hist_futures_df = api_client.get_historical_data(config.FUTURES_TICKER, days_back=1)
    if hist_futures_df is not None:
        data_processor.save_historical_data(hist_futures_df)

    # --- Fetch Time Series Data (e.g., for volatility or finer basis history) ---
    # Fetch for spot and futures tickers separately (e.g., hourly for past week)
    ts_spot_df = api_client.get_time_series_data(config.SPOT_TICKER, days=7, interval='hourly')
    if ts_spot_df is not None:
        data_processor.save_time_series_data(ts_spot_df)

    ts_futures_df = api_client.get_time_series_data(config.FUTURES_TICKER, days=7, interval='hourly')
    if ts_futures_df is not None:
        data_processor.save_time_series_data(ts_futures_df)

    print("--- Data Fetch Cycle Complete ---")

if __name__ == "__main__":
    run_fetch()