import os
import config
 
def create_directories():
    os.makedirs(config.BASE_DIR, exist_ok=True)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    os.makedirs(config.REAL_TIME_DIR, exist_ok=True)
    os.makedirs(config.HISTORICAL_DIR, exist_ok=True)
    os.makedirs(config.TIME_SERIES_DIR, exist_ok=True)
 
def verify_directories():
    print(f"BASE_DIR: {config.BASE_DIR}")
    print(f"OUTPUT_DIR: {config.OUTPUT_DIR}")
    print(f"REAL_TIME_DIR: {config.REAL_TIME_DIR}")
    print(f"HISTORICAL_DIR: {config.HISTORICAL_DIR}")
    print(f"TIME_SERIES_DIR: {config.TIME_SERIES_DIR}")
 
def verify_api_key():
    api_key = os.environ.get("TRADERMADE_API_KEY")
    if not api_key:
        print("TRADERMADE_API_KEY is not set. Please set the environment variable.")
        return False
    return True