# TraderMade CFD APIを活用したデータ取得サンプルコード集

TraderMade CFD APIを使用して様々な金融商品のデータを取得するための包括的なサンプルコードを紹介します。このAPIは株式、指数、エネルギー、貴金属など40以上の金融商品に関するリアルタイムおよび履歴データへのアクセスを提供しており、REST API、WebSocket、各種アドインを通じてデータを取得できます[1]。

## TraderMade CFD APIの概要

TraderMadeのCFD（Contract for Difference）APIは、金融アプリケーションや取引ツールの開発に必要なデータを提供するサービスです。このAPIは4つの市場（株式、指数、エネルギー、貴金属）のデータを単一のインターフェースで提供し、開発者が革新的な取引ソリューションを構築することを可能にします[1]。

主な特徴として以下が挙げられます：
- 検証済みの正確なデータ（Tier 1機関からのクリーンで信頼性の高いデータ）[1]
- 開発者フレンドリーなAPI（柔軟なRESTfulおよびWebSocket API）[1]
- 総合的な履歴データ（バックテストや市場トレンド分析用）[1]
- 専門家によるサポート[1]

### データ配信方法

TraderMadeでは、以下の方法でCFDデータを取得できます：
1. REST API - リアルタイムおよび履歴CFDデータへのアクセス[1]
2. WebSocket - 4つの市場のリアルタイムCFDデータのストリーミング[1]
3. アドイン - Excel、Google Sheets、Chat GPTなどへの直接データ取得[1]

## Pythonを使用したCFDデータ取得

Pythonは多くの開発者に人気のある言語であり、TraderMadeもPython用のSDKを提供しています。以下は、TraderMadeのPython SDKを使ったCFDデータ取得の一連のサンプルコードです。

```python
import tradermade as tm
import pandas as pd
from datetime import datetime, timedelta

# APIキーを設定
API_KEY = "あなたのAPIキー"
tm.set_rest_api_key(API_KEY)

# 利用可能なCFDリストを取得
print("=== 利用可能なCFD一覧 ===")
cfd_list = tm.cfd_list()
print(cfd_list)

# 利用可能な通貨コードを取得
print("\n=== 利用可能な通貨コード一覧 ===")
currency_list = tm.currency_list()
print(currency_list)

# リアルタイムデータを取得（複数のCFD）
print("\n=== リアルタイムデータ（複数のCFD） ===")
live_data = tm.live(currency='USOIL,XAUUSD,US30', fields=['bid', 'mid', 'ask'])
print(live_data)

# 特定の日付の履歴データを取得
print("\n=== 特定日の履歴データ ===")
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
historical_data = tm.historical(currency='XAUUSD,US500', date=yesterday, interval='daily', fields=['open', 'high', 'low', 'close'])
print(historical_data)

# 時系列データを取得（過去1週間の時間単位データ）
print("\n=== 時系列データ（1週間） ===")
end_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d-%H:%M')
timeseries_data = tm.timeseries(
    currency='UKOIL', 
    start=start_date,
    end=end_date,
    interval='hourly',
    fields=['open', 'high', 'low', 'close']
)
print(timeseries_data)

# データをPandasデータフレームに変換して分析（例）
if 'quotes' in timeseries_data:
    df = pd.DataFrame(timeseries_data['quotes'])
    print("\n=== データフレーム統計情報 ===")
    print(df.describe())
    
    # 移動平均を計算（例）
    if 'close' in df.columns:
        df['MA5'] = df['close'].rolling(window=5).mean()
        print("\n=== 5期間移動平均付きデータ（末尾） ===")
        print(df.tail())
```

このPythonサンプルコードでは、TraderMade APIを使用して以下の操作を行っています：
- 利用可能なCFDと通貨コードのリスト取得
- リアルタイムデータの取得
- 特定の日付の履歴データの取得
- 時系列データの取得と簡単な分析[1]

## Goを使用したCFDデータ取得

Goはパフォーマンスとコンカレンシーに優れたプログラミング言語であり、特に高速な金融アプリケーションの開発に適しています。以下は、TraderMadeのGo SDKを使ったCFDデータ取得のサンプルコードです。

```go
package main

import (
	"fmt"
	"log"
	"time"

	tradermade "github.com/tradermade/Go-SDK/rest"
)

func main() {
	// クライアントの初期化
	apiKey := "あなたのAPIキー"
	client := tradermade.NewRESTClient(apiKey)

	// 利用可能なCFDリストを取得
	fmt.Println("=== 利用可能なCFD一覧 ===")
	cfdList, err := client.GetCFDList()
	if err != nil {
		log.Fatalf("CFDリスト取得エラー: %v", err)
	}
	fmt.Printf("利用可能なCFD: %v\n", cfdList)

	// CFDのリアルタイムレートを取得
	fmt.Println("\n=== リアルタイムCFDレート ===")
	cfdSymbols := []string{"USOIL", "XAUUSD", "US30"}
	liveRates, err := client.GetLiveRates(cfdSymbols)
	if err != nil {
		log.Fatalf("リアルタイムレート取得エラー: %v", err)
	}

	// レート情報を出力
	for _, quote := range liveRates.Quotes {
		fmt.Printf("商品: %s, Bid: %.5f, Ask: %.5f, Mid: %.5f\n",
			quote.BaseCurrency, quote.Bid, quote.Ask, quote.Mid)
	}

	// 履歴データの取得
	fmt.Println("\n=== 履歴データ ===")
	yesterday := time.Now().AddDate(0, 0, -1).Format("2006-01-02")
	historicalData, err := client.GetHistoricalData("XAUUSD", yesterday, "daily")
	if err != nil {
		log.Fatalf("履歴データ取得エラー: %v", err)
	}
	fmt.Printf("日付: %s, Open: %.2f, High: %.2f, Low: %.2f, Close: %.2f\n",
		yesterday,
		historicalData.Open,
		historicalData.High,
		historicalData.Low,
		historicalData.Close)

	// 時系列データの取得
	fmt.Println("\n=== 時系列データ ===")
	endDate := time.Now().Format("2006-01-02")
	startDate := time.Now().AddDate(0, 0, -7).Format("2006-01-02")
	timeseriesData, err := client.GetTimeseriesData("US500", startDate, endDate, "daily", "1")
	if err != nil {
		log.Fatalf("時系列データ取得エラー: %v", err)
	}
	
	fmt.Printf("時系列データポイント数: %d\n", len(timeseriesData.Quotes))
	// 最新のデータポイントを表示
	if len(timeseriesData.Quotes) > 0 {
		latest := timeseriesData.Quotes[len(timeseriesData.Quotes)-1]
		fmt.Printf("最新データ - 日付: %s, Close: %.2f\n", latest.Date, latest.Close)
	}
}
```

このGoサンプルコードでは、TraderMade APIを使用して以下の操作を行っています：
- 利用可能なCFDリストの取得
- 複数のCFDシンボルのリアルタイムレートの取得と表示
- 特定のCFDの履歴データの取得
- 時系列データの取得と最新データの表示[1]

## Java/Kotlinを使用したCFDデータ取得

Java/Kotlinは企業システムやクロスプラットフォームアプリケーションの開発によく使用されます。以下は、TraderMadeのJava/Kotlin SDKを使ったCFDデータ取得の包括的なサンプルコードです。

```java
package com.example.tradermade;

import io.tradermade.kotlin.sdk.TraderMadeAPI;
import io.tradermade.kotlin.sdk.models.*;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Map;

public class TraderMadeCFDSample {
    public static void main(String[] args) {
        // APIクライアントの初期化
        String apiKey = "あなたのAPIキー";
        TraderMadeAPI api = new TraderMadeAPI(apiKey);
        
        try {
            // CFDリストの取得
            System.out.println("=== 利用可能なCFD一覧 ===");
            CFDListResponse cfdList = api.getCFDList();
            System.out.println("利用可能なCFD: " + cfdList.getAvailable());
            
            // リアルタイムデータの取得
            System.out.println("\n=== リアルタイムCFDデータ ===");
            LiveDataResponse liveData = api.getLiveData("USOIL,XAUUSD,US30");
            
            for (Quote quote : liveData.getQuotes()) {
                System.out.printf("商品: %s, Bid: %.5f, Ask: %.5f, Mid: %.5f%n",
                        quote.getBaseCurrency(), quote.getBid(), quote.getAsk(), quote.getMid());
            }
            
            // 履歴データの取得
            System.out.println("\n=== 履歴データ ===");
            LocalDate yesterday = LocalDate.now().minusDays(1);
            String yesterdayStr = yesterday.format(DateTimeFormatter.ISO_DATE);
            
            HistoricalDataResponse historicalData = api.getHistoricalData("XAUUSD", yesterdayStr);
            System.out.printf("日付: %s, Open: %.2f, High: %.2f, Low: %.2f, Close: %.2f%n",
                    historicalData.getDate(),
                    historicalData.getOpen(),
                    historicalData.getHigh(),
                    historicalData.getLow(),
                    historicalData.getClose());
            
            // 時系列データの取得
            System.out.println("\n=== 時系列データ ===");
            LocalDate startDate = LocalDate.now().minusDays(7);
            LocalDate endDate = LocalDate.now();
            String startDateStr = startDate.format(DateTimeFormatter.ISO_DATE);
            String endDateStr = endDate.format(DateTimeFormatter.ISO_DATE);
            
            TimeSeriesResponse timeSeriesData = api.getTimeSeriesData(
                    "US500", 
                    startDateStr, 
                    endDateStr, 
                    "daily", 
                    "1"
            );
            
            System.out.printf("時系列データポイント数: %d%n", timeSeriesData.getQuotes().size());
            
            if (!timeSeriesData.getQuotes().isEmpty()) {
                TimeSeriesQuote latestQuote = timeSeriesData.getQuotes().get(timeSeriesData.getQuotes().size() - 1);
                System.out.printf("最新データ - 日付: %s, Close: %.2f%n", 
                        latestQuote.getDate(), 
                        latestQuote.getClose());
            }
            
            // 通貨換算の例
            System.out.println("\n=== 通貨換算 ===");
            CurrencyConversionResponse conversion = api.convertCurrency("XAU", "USD", 1.0);
            System.out.printf("1 XAU = %.2f USD%n", conversion.getTotal());
            
        } catch (Exception e) {
            System.err.println("エラーが発生しました: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

Kotlinでの同等のコード例：

```kotlin
import io.tradermade.kotlin.sdk.TraderMadeAPI
import java.time.LocalDate
import java.time.format.DateTimeFormatter

fun main() {
    // APIクライアントの初期化
    val apiKey = "あなたのAPIキー"
    val api = TraderMadeAPI(apiKey)
    
    try {
        // CFDリストの取得
        println("=== 利用可能なCFD一覧 ===")
        val cfdList = api.getCFDList()
        println("利用可能なCFD: ${cfdList.available}")
        
        // リアルタイムデータの取得
        println("\n=== リアルタイムCFDデータ ===")
        val liveData = api.getLiveData("USOIL,XAUUSD,US30")
        
        liveData.quotes.forEach { quote ->
            println("商品: ${quote.baseCurrency}, Bid: ${quote.bid}, Ask: ${quote.ask}, Mid: ${quote.mid}")
        }
        
        // 履歴データの取得
        println("\n=== 履歴データ ===")
        val yesterday = LocalDate.now().minusDays(1)
        val yesterdayStr = yesterday.format(DateTimeFormatter.ISO_DATE)
        
        val historicalData = api.getHistoricalData("XAUUSD", yesterdayStr)
        println("日付: ${historicalData.date}, Open: ${historicalData.open}, High: ${historicalData.high}, " +
                "Low: ${historicalData.low}, Close: ${historicalData.close}")
        
        // 時系列データの取得
        println("\n=== 時系列データ ===")
        val startDate = LocalDate.now().minusDays(7)
        val endDate = LocalDate.now()
        val startDateStr = startDate.format(DateTimeFormatter.ISO_DATE)
        val endDateStr = endDate.format(DateTimeFormatter.ISO_DATE)
        
        val timeSeriesData = api.getTimeSeriesData(
            "US500", 
            startDateStr, 
            endDateStr, 
            "daily", 
            "1"
        )
        
        println("時系列データポイント数: ${timeSeriesData.quotes.size}")
        
        timeSeriesData.quotes.lastOrNull()?.let { latestQuote ->
            println("最新データ - 日付: ${latestQuote.date}, Close: ${latestQuote.close}")
        }
        
        // 通貨換算の例
        println("\n=== 通貨換算 ===")
        val conversion = api.convertCurrency("XAU", "USD", 1.0)
        println("1 XAU = ${conversion.total} USD")
        
    } catch (e: Exception) {
        println("エラーが発生しました: ${e.message}")
        e.printStackTrace()
    }
}
```

Java/Kotlinのサンプルコードでは、TraderMade APIを使用して以下の操作を行っています：
- CFDリストの取得と表示
- 複数の商品のリアルタイムデータの取得と表示
- 履歴データの取得
- 時系列データの取得と最新データの表示
- 通貨換算機能の活用[1]

## WebSocketを使用したリアルタイムデータのストリーミング

WebSocketを使用すると、継続的にリアルタイムデータを受信できます。以下は、Pythonを使用したWebSocketストリーミングの例です。

```python
import websocket
import json
import time
import threading

# WebSocketイベントハンドラー
def on_message(ws, message):
    data = json.loads(message)
    print(f"リアルタイムデータ受信: {data}")

def on_error(ws, error):
    print(f"エラー発生: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket接続終了: {close_status_code} - {close_msg}")

def on_open(ws):
    print("WebSocket接続確立")
    
    # サブスクリプションリクエスト
    subscribe_message = {
        "userKey": "あなたのAPIキー",
        "symbol": "XAUUSD,USOIL,US30"
    }
    ws.send(json.dumps(subscribe_message))

def start_websocket():
    # WebSocketへの接続
    websocket_url = "wss://marketdata.tradermade.com/feedadv"
    ws = websocket.WebSocketApp(websocket_url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    
    # WebSocket接続の開始（ノンブロッキング）
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    
    return ws

if __name__ == "__main__":
    print("TraderMade WebSocketデータストリーミングを開始します...")
    ws = start_websocket()
    
    try:
        # メインスレッドを60秒間実行し続ける
        for i in range(60):
            time.sleep(1)
            print(f"データ受信中... {i+1}秒経過")
    except KeyboardInterrupt:
        print("プログラムを終了します")
    finally:
        ws.close()
        print("WebSocket接続を閉じました")
```

このWebSocketサンプルコードでは、TraderMadeのWebSocketエンドポイントに接続し、選択したCFD商品のリアルタイムデータストリームを受信します[1]。

## APIの利用方法と料金プラン

TraderMade APIの利用には以下の点に注意が必要です：

1. **APIキーの取得**: サインアップしてログインすると、ダッシュボードからAPIキーを入手できます。登録は無料です[1]。

2. **使用量の追跡**: APIキーを使用することで、簡単に使用量を追跡できます[1]。

3. **WebSocketストリーミング**: WebSocket経由でのストリーミングデータにアクセスするには、14日間の無料トライアルが利用可能です[1]。

4. **料金プラン**:
   - 月額1,000リクエストまで永久無料
   - 月単位の柔軟な課金プラン（アップグレード、ダウングレード、キャンセルが可能）
   - 一回限りのデータ販売も利用可能[1]

5. **支払い方法**: 支払いパートナーはStripeで、Visa、MasterCard、Discover、American Express、Diner's Clubなど様々なデビットカードやクレジットカードが利用可能[1]。

## まとめ

TraderMade CFD APIは、株式、指数、エネルギー、貴金属など多様な金融商品のデータに簡単にアクセスできる強力なツールです。本記事では、Python、Go、Java/Kotlin、WebSocketを使用して一通りのデータを取得する方法を紹介しました。

これらのサンプルコードを活用することで、以下のことが可能になります：
- リアルタイムおよび履歴CFDデータの取得
- 時系列データの分析と可視化
- リアルタイムデータストリームの受信と処理
- 金融アプリケーションやウェブサイトへのデータ統合

TraderMadeのAPIは開発者フレンドリーで、ドキュメントが充実しており、専門家によるサポートも提供されています。これにより、データに関する懸念を減らし、アプリケーション開発に集中することができます[1]。

金融データを活用したアプリケーション開発を検討している場合は、TraderMade CFD APIは信頼性の高いデータソースとして検討する価値があるでしょう。

Citations:
[1] https://tradermade.com/cfds

---
Perplexity の Eliot より: pplx.ai/share