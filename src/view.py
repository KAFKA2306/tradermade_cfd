import os
import glob
import pandas as pd
import config
from IPython.display import display

def display_parquet_files():
    output_dir = config.OUTPUT_DIR
    data_type_dirs = [os.path.join(output_dir, d) for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]
    print(fr"data_type_dirs : {data_type_dirs}")
    parquet_files = []
    for data_type_dir in data_type_dirs:
        parquet_files.extend(glob.glob(os.path.join(data_type_dir, "*.parquet")))
        parquet_files = glob.glob(os.path.join(data_type_dir, "*.parquet"))
        parquet_files.sort()  # ファイルを順番に表示するためにソート
        print(fr"parquet_files : {parquet_files}")
    
        for file_path in parquet_files:
            print(f"{file_path}")
            df = pd.read_parquet(file_path)
            display(df)

if __name__ == "__main__":
    display_parquet_files()