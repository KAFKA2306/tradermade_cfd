import os
from datetime import datetime, timedelta
import api_client
import data_processor
import utils
import config

 
if __name__ == "__main__":
    config.create_directories()
    utils.verify_directories()
    if not utils.verify_api_key():
        exit()
 
    # Real-time data
    real_time_symbols = 'USOIL,XAUUSD,US30'
    real_time_data = api_client.get_real_time_data(real_time_symbols)
    if real_time_data:
        real_time_filepath = data_processor.save_real_time_data(real_time_data)
        print(f"Real-time data saved to {real_time_filepath}")
 
    # Historical data
    historical_symbol = 'XAUUSD'
    historical_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    historical_data = api_client.get_historical_data(historical_symbol, historical_date)
    if not historical_data.empty:
        historical_filepath = data_processor.save_historical_data(historical_data)
        print(f"Historical data saved to {historical_filepath}")
 
    # Time-series data
    time_series_symbol = 'UKOIL'
    time_series_end_date = datetime.utcnow().strftime('%Y-%m-%d-%H:%M')
    time_series_start_date = (datetime.utcnow() - timedelta(days=8)).strftime('%Y-%m-%d-%H:%M')
    time_series_data = api_client.get_time_series_data(time_series_symbol, time_series_start_date, time_series_end_date)
    print(f"Type of time_series_data: {type(time_series_data)}")
    print(f"Content of time_series_data: {time_series_data}")
    print(f"Keys of time_series_data: {time_series_data.keys()}")
    if not isinstance(time_series_data, dict):
        time_series_filepath = data_processor.save_time_series_data(time_series_data)
        print(f"Time-series data saved to {time_series_filepath}")