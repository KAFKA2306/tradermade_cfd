import os
import tradermade as tm
import pandas as pd
from datetime import datetime, timedelta # datetime と timedelta をインポート
from config import API_KEY

# --- APIキー設定 (モジュール読み込み時に実行) ---
_api_initialized = False
if API_KEY:
    try:
        tm.set_rest_api_key(API_KEY)
        _api_initialized = True
        print("Tradermade API Key set successfully from api_client.py")
    except Exception as e:
        print(f"Error setting API key in api_client.py: {e}")
else:
    print("API Key not found in config or .env file for api_client.py")

def initialize_api():
    """APIの初期化状態を確認"""
    if not _api_initialized:
        print("API Key was not initialized. Please check config.py and your .env file.")
    return _api_initialized

# --- 共通のデータ取得ラッパー ---
def _get_data(api_function, **kwargs):
    """API関数を呼び出し、エラーハンドリングを行う"""
    if not _api_initialized:
        print("API is not initialized (key missing or failed to set). Cannot fetch data.")
        return None
    try:
        # APIライブラリの呼び出し部分をデバッグしやすくする
        print(f"Calling API function: {api_function.__name__} with args: {kwargs}")
        data = api_function(**kwargs)
        print(f"API Response type for {api_function.__name__}: {type(data)}")
        # レスポンスが辞書型でエラーメッセージを含むかチェック
        if isinstance(data, dict) and data.get('error'):
             print(f"API Error reported by Tradermade for {api_function.__name__}: {data.get('message', 'No error message provided.')}")
             return None # エラー時はNoneを返す
        if isinstance(data, dict) and 'message' in data and 'error' in data.get('message', '').lower():
             print(f"API Error Message detected for {api_function.__name__}: {data['message']}")
             return None # エラーメッセージを含む場合もNoneを返す
        return data
    except Exception as e:
        print(f"Exception during API call {api_function.__name__}: {e}")
        return None

# --- データ取得関数 ---
def get_real_time_data(cfd_symbols):
    """リアルタイムデータを取得"""
    print(f"Fetching real-time data for: {cfd_symbols}")
    # 'instrument' フィールドも取得してどのシンボルのデータか明確にする
    data = _get_data(tm.live, currency=cfd_symbols, fields=['bid', 'mid', 'ask', 'instrument'])
    if data is None:
        print("Real-time API call failed or returned error.")
        return None

    # Tradermadeのliveはリストを返すことが多い
    if isinstance(data, list):
        try:
            df = pd.DataFrame(data)
            print(f"Converted real-time list data to DataFrame. Shape: {df.shape}")
            if 'instrument' not in df.columns:
                 print("Warning: 'instrument' column missing in real-time data.")
                 # シンボルが単一の場合、手動で追加することも検討できる
                 if len(cfd_symbols.split(',')) == 1:
                     df['instrument'] = cfd_symbols
            return df
        except Exception as convert_error:
            print(f"Error converting real-time list data to DataFrame: {convert_error}")
            return None
    elif isinstance(data, dict): # 単一シンボルだと辞書の場合もある？ドキュメント確認要
         try:
            # 'instrument'がない場合、リクエストしたシンボル名を追加
            if 'instrument' not in data and len(cfd_symbols.split(',')) == 1:
                data['instrument'] = cfd_symbols
            df = pd.DataFrame([data]) # リストでラップしてDataFrame化
            print(f"Converted real-time dict data to DataFrame. Shape: {df.shape}")
            return df
         except Exception as convert_error:
             print(f"Error converting real-time dict data to DataFrame: {convert_error}")
             return None
    else:
        print(f"Unexpected data type received from real-time API: {type(data)}")
        return None


# エイリアスとして get_live_data を定義
get_live_data = get_real_time_data

def get_historical_data(cfd_symbol, historical_date=None, days_back=None):
    """過去データを取得"""
    target_date_str = historical_date
    if historical_date is None and days_back is not None:
        # datetime と timedelta がインポートされていることを確認
        try:
            target_date = datetime.now() - timedelta(days=days_back)
            target_date_str = target_date.strftime('%Y-%m-%d')
        except NameError:
            print("Error: datetime or timedelta not imported correctly.")
            return None
    elif historical_date is None:
         # デフォルトとして昨日の日付を使用
         target_date = datetime.now() - timedelta(days=1)
         target_date_str = target_date.strftime('%Y-%m-%d')

    print(f"Fetching historical data for {cfd_symbol} on {target_date_str}")
    # 'instrument' フィールドも取得
    data = _get_data(tm.historical, currency=cfd_symbol, date=target_date_str, interval='daily', fields=['open', 'high', 'low', 'close', 'instrument'])

    if data is None:
        print(f"Historical API call failed or returned error for {cfd_symbol} on {target_date_str}.")
        return None

    # historical は通常、単一の辞書を返す
    if isinstance(data, dict):
        # 'instrument' がない場合、リクエストしたシンボル名を追加
        if 'instrument' not in data:
            data['instrument'] = cfd_symbol
        try:
            df = pd.DataFrame([data]) # リストでラップしてDataFrame化
            print(f"Converted historical dict data to DataFrame. Shape: {df.shape}")
            return df
        except Exception as convert_error:
            print(f"Warning: Could not convert historical data dict to DataFrame: {convert_error}")
            return None
    else:
         print(f"Unexpected data type received from historical API: {type(data)}")
         return None


def get_time_series_data(cfd_symbol, start=None, end=None, days=None, interval='hourly'):
    """時系列データを取得"""
    start_str = start
    end_str = end

    # days パラメータをサポート (start/end が指定されていない場合)
    if start is None and end is None and days is not None:
        try:
            end_dt = datetime.utcnow() # APIはUTCを期待することが多い
            start_dt = end_dt - timedelta(days=days)
            # APIが期待するフォーマットに合わせる (例: '%Y-%m-%d-%H:%M')
            end_str = end_dt.strftime('%Y-%m-%d-%H:%M')
            start_str = start_dt.strftime('%Y-%m-%d-%H:%M')
        except NameError:
            print("Error: datetime or timedelta not imported correctly.")
            return None
    elif start is None or end is None:
        print("Error: Either provide both 'start' and 'end' dates, or 'days' parameter for time series.")
        return None

    print(f"Fetching {interval} time series for {cfd_symbol} from {start_str} to {end_str}")
    # 'instrument' フィールドも取得
    data = _get_data(tm.timeseries,
                    currency=cfd_symbol,
                    start=start_str,
                    end=end_str,
                    interval=interval,
                    fields=['open', 'high', 'low', 'close', 'instrument']) # instrument を追加

    if data is None:
        print(f"Time series API call failed or returned error for {cfd_symbol}.")
        return None

    # timeseries は 'quotes' キーを持つ辞書を返すことが多い
    if isinstance(data, dict) and 'quotes' in data:
        if data['quotes']: # quotes リストが空でないか確認
            try:
                df = pd.DataFrame(data['quotes'])
                # 'instrument' が quotes 内にない場合があるため、手動で追加
                if 'instrument' not in df.columns:
                    df['instrument'] = cfd_symbol
                print(f"Converted time series 'quotes' data to DataFrame. Shape: {df.shape}")
                return df
            except Exception as convert_error:
                print(f"Error converting time series 'quotes' to DataFrame: {convert_error}")
                return None
        else:
            print(f"Time series data for {cfd_symbol} returned an empty 'quotes' list.")
            return None # 空のリストでもNoneを返すか、空のDataFrameを返すかは要件次第
    else:
        print(f"Unexpected data type or structure received from time series API: {type(data)}")
        if isinstance(data, dict):
            print(f"Keys in received dict: {data.keys()}")
        return None