import os
import pandas as pd
import datetime # datetime モジュール全体をインポート

def save_data(data, directory, prefix):
    """
    データをParquet形式で保存する。

    Args:
        data (pd.DataFrame or dict or list): 保存するデータ。
        directory (str): 保存先のディレクトリパス。
        prefix (str): ファイル名のプレフィックス。

    Returns:
        str: 保存されたファイルの完全パス。失敗時はNone。
    """
    if data is None:
        print(f"No data provided for prefix '{prefix}'. Skipping save.")
        return None

    df = None
    try:
        if isinstance(data, pd.DataFrame):
            df = data.copy() # 念のためコピー
        elif isinstance(data, list):
             if not data:
                  print(f"Received empty list for prefix '{prefix}'. Skipping save.")
                  return None
             df = pd.DataFrame(data)
        elif isinstance(data, dict):
             # 辞書が空、または'quotes'キーがあってその値が空リストの場合もスキップ
             if not data or ('quotes' in data and not data['quotes']):
                  print(f"Received empty dictionary or empty 'quotes' for prefix '{prefix}'. Skipping save.")
                  return None
             # timeseriesの'quotes'形式か、単一レコード形式か
             if 'quotes' in data:
                 df = pd.DataFrame(data['quotes'])
             else:
                 df = pd.DataFrame([data]) # 単一レコード辞書をリストでラップ
        else:
             print(f"Unsupported data type '{type(data)}' for prefix '{prefix}'. Cannot save.")
             return None

        if df.empty:
            print(f"DataFrame created for prefix '{prefix}' is empty. Skipping save.")
            return None

    except Exception as e:
        print(f"Error converting data to DataFrame for prefix '{prefix}': {e}")
        return None

    try:
        os.makedirs(directory, exist_ok=True)
        # datetime.datetime を使用
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(directory, f"{prefix}_{timestamp}.parquet")

        df.to_parquet(filepath, engine='pyarrow') # engine指定を推奨
        # print(f"Data successfully saved to {filepath}") # 成功メッセージは呼び出し元に任せるか、ここで出すか選択
        return filepath
    except Exception as e:
        print(f"Error saving data to {filepath}: {e}")
        return None

def load_data(filepath):
    """
    Parquet形式のデータを読み込む。

    Args:
        filepath (str): 読み込むファイルのパス。

    Returns:
        pd.DataFrame: 読み込んだデータ。失敗した場合はNone。
    """
    try:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return None
        return pd.read_parquet(filepath)
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
        return None