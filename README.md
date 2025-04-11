# TraderMade CFD Data Processing

This project fetches, processes, and displays CFD data from the TraderMade API.

## Requirements

*   Python 3.6+
*   TraderMade API key (set as environment variable `TRADERMADE_API_KEY`)
*   Libraries: pandas, ipython, tradermade

## Setup

1.  Clone the repository.
2.  Install the requirements: `pip install -r requirements.txt`
3.  Set the `TRADERMADE_API_KEY` environment variable.

## Usage

1.  **`src/main_fetch.py`**: TraderMade API からデータを取得し、保存します。
    *   設定ファイル (`config.py`) に基づき、リアルタイムデータ、ヒストリカルデータ（過去1日分）、および時系列データ（過去7日間の時間足）を取得します。
    *   取得したデータは、それぞれ `data/real_time`, `data/historical`, `data/time_series` ディレクトリに Parquet 形式で保存されます。
    *   実行前に `TRADERMADE_API_KEY` 環境変数が設定されている必要があります。

2.  **`src/data_integrator.py`**: `main_fetch.py` で保存された複数のデータファイルを統合します。
    *   `data/real_time`, `data/historical`, `data/time_series` ディレクトリ内の Parquet ファイルをすべて読み込みます。
    *   各データに `data_type` カラムを追加し、一つのデータフレームに結合します。
    *   統合されたデータは、タイムスタンプ付きのファイル名 (`integrated_data_YYYYMMDD_HHMMSS.parquet`) で `data/output` ディレクトリに保存されます。

3.  **`src/indicator_calculator.py`**: 処理済みデータからテクニカル指標を計算します。
    *   `data_processor.py` によって生成された最新の処理済みメトリクスデータ (`data/processed_metrics/calculated_metrics_*.parquet`) を読み込みます。
    *   ベーシス（先物価格 - 現物価格）を計算（または確認）します。
    *   ベーシスのローリング Z スコア (`basis_z_score`) を計算します（デフォルトのウィンドウサイズは20）。
    *   計算結果は `data/indicator` ディレクトリに `indicator_data_w[window_size]_YYYYMMDD_HHMMSS.parquet` のようなファイル名で保存されます。

4.  **`src/view.py`**: 最新の計算済みメトリクスを表示します。
    *   `data/processed_metrics` ディレクトリから最新の `calculated_metrics_*.parquet` ファイルを読み込みます。
    *   現物価格、先物価格、ベーシス、ベーシス率、年率換算ベーシス、市場レジームなどの主要なメトリクスを抽出・整形します。
    *   IPython/Jupyter 環境で、これらのメトリクスを HTML グリッド形式で見やすく表示します。
    *   (注意: このスクリプトは主に Jupyter Notebook (`src/view.ipynb`) や IPython コンソールでの使用を想定しています。)