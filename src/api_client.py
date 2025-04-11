import os
import tradermade as tm
from config import API_KEY

tm.set_rest_api_key(API_KEY)

def get_real_time_data(symbols):
    data = tm.live(currency=symbols, fields=['bid', 'mid', 'ask'])
    print(f"Type of data: {type(data)}")
    print(f"Content of data: {data}")
    return [item for item in data]

def get_historical_data(symbol, date):
    return tm.historical(currency=symbol, date=date, interval='daily', fields=['open', 'high', 'low', 'close'])

def get_time_series_data(symbol, start_date, end_date, interval='hourly'):
    return tm.timeseries(currency=symbol, start=start_date, end=end_date, interval=interval, fields=['open', 'high', 'low', 'close'])