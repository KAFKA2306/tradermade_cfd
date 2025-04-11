# src/utils.py
import os
import config # configモジュールをインポート

def create_directories():
    """config.pyで定義された全ディレクトリを作成"""
    for directory in config.ALL_DIRS:
        os.makedirs(directory, exist_ok=True)
    print(f"Ensured directories exist: {config.ALL_DIRS}")

def verify_api_key():
    """環境変数からAPIキーを確認"""
    if not config.API_KEY:
        print("ERROR: TRADERMADE_API_KEY 環境変数が設定されていません。")
        print(".envファイルに TRADERMADE_API_KEY=YOUR_API_KEY の形式で設定してください。")
        return False
    print("TRADERMADE_API_KEY が環境変数に見つかりました。")
    return True

# 他のコードとの互換性のためのエイリアス
verify_api_key_environment = verify_api_key
