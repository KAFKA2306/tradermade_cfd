# 主要なCFD（差金決済取引）銘柄とForex（外国為替）通貨ペアのリアルタイムデータ取得

このドキュメントでは、主要なCFD（差金決済取引）銘柄とForex（外国為替）通貨ペアのリアルタイムデータを取得する方法について説明します。

## CFDとは？

CFD（差金決済取引）は、原資産を実際に所有せずに、価格変動から利益を得るための金融商品です。CFD取引では、買いポジション（ロング）または売りポジション（ショート）を持つことができ、価格が予想通りに変動すれば利益が得られます。

## Forexとは？

Forex（外国為替）は、異なる国の通貨を交換する市場です。Forex市場は世界最大規模の金融市場であり、24時間取引が可能です。

## 必要なもの

*   Python 3.6+
*   TraderMade APIキー（`.env`ファイルに`TRADERMADE_API_KEY`として設定）
*   ライブラリ：pandas、tradermade、python-dotenv

## セットアップ

1.  リポジトリをクローンします。
2.  必要なライブラリをインストールします：`pip install -r requirements.txt`
3.  `.env`ファイルを作成し、環境変数`TRADERMADE_API_KEY`を設定します。

    *   APIキーを取得するには、TraderMadeにサインアップする必要があります。
    *   `.env`ファイルの設定方法は、[python-dotenv](https://pypi.org/project/python-dotenv/)を参照してください。

## 使い方

`src/main.py`を実行して、リアルタイムデータ、ヒストリカルデータ、およびタイムシリーズデータを取得し、保存します。

## コード例

以下のコードは、主要なCFD銘柄とForex通貨ペアのリアルタイムデータを取得する例です。

```python
import os
import pandas as pd
import tradermade as tm
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TRADERMADE_API_KEY")

tm.set_rest_api_key(API_KEY)

symbols = 'USOIL,XAUUSD,EURUSD,GBPUSD'  # 例：原油、金、ユーロ/米ドル、英ポンド/米ドル
data = tm.live(currency=symbols, fields=['bid', 'mid', 'ask'])

df = pd.DataFrame(data)
print(df)
```

## コード

このプロジェクトのコードは、以下のファイルに分割されています。

*   `src/main.py`: メインスクリプト
*   `src/api_client.py`: TraderMade APIとの通信を処理する関数
*   `src/data_processor.py`: データの保存を処理する関数
*   `src/config.py`: 設定
*   `src/utils.py`: ユーティリティ関数
*   `src/view.py`: データの表示

詳細については、上記のファイルを参照してください。