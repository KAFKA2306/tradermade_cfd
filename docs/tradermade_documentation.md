TraderMadetradermade logo
Product
Resources
Company
Pricing


Dashboard
Documentation
Restful API WebSockets FIX
RESTful API
Getting Started
Quick Start Guide
Authentication
Query Generator
Supported Currencies
Available SDK’s
Python
Kotlin
Error Codes
API Endpoints
Currency Data Endpoints
Live Rates
Historical Rates
Tick Historical Rates
Minute Historical Rates
Hour Historical Rates
Time-Series
Pandas
Convert
Examples
Getting Started
Welcome to TraderMade. We provide clean forex and CFD data via easy to use delivery methods. We use HTTPS and RESTful structures that make it easier to request data. Authentication is over a secure HTTPS protocol and responses are in JSON Format.

Following are a few simple steps to start getting data:

1. Sign up for API : Sign Up ↗
2. Get your API Key : API Key ↗.
3. Start getting data : API Endpoints ↗
Quick Start Guide
We have created a number of tutorials to help you get started with our REST API. Our tutorials cover topics such as Excel, Python, C#.

See our quick start tutorials : Visit Tutorials ↗
Also check our interactive API Definition : Technical Documentation ↗
Authentication
You need to include your API Key with each request to get data. You can find your API Key in your Dashboard once you signin. We will prepopulate your API Key for you to run sample API queries once you Sign In .

You can also learn more on how to use our forex data API on the tutorials page ↗

copied to clipboard!Error
Query Generator
1. Request URLCopy
https://marketdata.tradermade.com/api/v1/?api_key=PXC--8DtI3s4Gbfptfd7
Choose API Endpoint *

Select Endpoint
Insert your API key *
PXC--8DtI3s4Gbfptfd7
2. Select Parameters
Parameter 1

Select
Parameter 2

Select
Parameter 3

Select
Parameter 4

Select
Parameter 5

Select
Parameter 6

Select
Start and end date time must be GMT and not at a future period. Please check each endpoint docs to find out the data history available.

Run Query
                        

                    Copy
COPY
RESET QUERY
Supported Currencies
We support over 8000+ currency pairs on our API endpoints. It includes 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. We also have CFDs, Visit the CFD list page for codes.

Available SDKs
Python SDK
                        
pip install tradermade

                    Copy
Python users can install our SDK to start using our API in seconds. We recommend going through our python SDK documentation. Alternatively, you can read our tutorial on how to use our Python-SDK for Forex Data

                        
import tradermade as tm
# set api key
tm.set_rest_api_key("api_key")

#get data
tm.live(currency='EURUSD,GBPUSD',fields=["bid", "mid", "ask"]) # returns live data - fields is optional
    
tm.historical(currency='EURUSD,GBPUSD', date="2021-04-22",interval="daily", fields=["open", "high", "low","close"]) # returns historical data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.timeseries(currency='EURUSD', start="2025-04-10-00:00",end="2025-04-11-10:29",interval="hourly",fields=["open", "high", "low","close"]) # returns timeseries data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.cfd_list() # gets list of all cfds available
    
tm.currency_list() # gets list of all currency codes available add two codes to get code for currencypair ex EUR + USD gets EURUSD

                    Copy
Kotlin client JVM
                    
package io.tradermade.test_client_jvm

                Copy
Java and android users can setup our SDK in seconds. We recommend going through our Kotlin JVM Client.

                    

# set api key
val api = TraderMadeAPI("YOUR_API_KEY")

#get data
val liveData = api.getLiveData("EURUSD,GBPUSD") // returns live data 

val historicalData = api.getHistoricalData("EURUSD", "2023-08-01") // returns historical data for the currency requested.

val timeSeriesData = api.getTimeSeriesData("EURUSD", "2023-08-01", "2023-08-10", "daily", "1") // returns timeseries data for the currency requested interval is daily, hourly, minute.

val convertedAmount = api.convertCurrency("EUR", "USD", 1000.0) // returns live currency conversion rates 


                Copy
Error Codes
Below are the error codes and responses for all the API endpoints.

Codes
HTTP Status
Message
401
200 - OK
API Key is invalid | Your plan doesn't allow access to this dataset
204
200 - OK
Data for the date requested not available | Currency pair currently not available
400
400 - BAD REQUEST
Input payload validation failed (often due to a missing parameter or wrong input) Reasons may be an incorrect currency code, date format, or end date before the start date.
403
403 - Forbidden
No data for weekend | Data outside max historical data we provide
                        
// 400 will return error which includes the details of the error   
    {
        "errors": {
            "date": "YYYY-MM-DD time data '2019-10-' does not match format '%Y-%m-%d'"
        },
        "message": "Input payload validation failed"
    }

                    Copy
Data Endpoints
Live Currencies List
You can request the live_currencies_list endpoint to access a list of the available currencies for the /live and the /convert endpoint.endpoint. Add the currency codes to form a currency pair to request currency data. For example EURUSD can be requested by adding EUR and USD together. Reverse the quote to USDEUR to get the inverse of the same pair. To access the JSON object containing all available currency codes verus USD, append your api_key to the TraderMade exchange rates API apicurrencies endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Live Crypto List
We offer data for 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. A list of the available cryptocurrencies for the /live endpoint, can be accessed through requesting the live_cypto_list endpoint. In order to request currency data, add the currencies codes together to form a currency pair. For example DOGEUSD can be requested by adding DOGE and USD together. In order to get the inverse of the same pair, simply reverse the quote to USDDOGE. To access JSON object containing all available crypto codes verus USD, Simply append your api_key to the TraderMade live crypto API endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_crypto_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Currencies List
We support over 1600 currency pairs on our historical data endpoints. Request the historical_currencies_list endpoint or visit the list of historical exchange rates page to access a list of the available currencies for historical, pandasDF, timeseries, and the minute_historical endpoints. The below example is an abbreviated version.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Exchange rates API
The TraderMade exchange rates API has nine endpoints serving different sets of data. Below has one example for each of the endpoints.

Request URL

    // live endpoint 
    https://marketdata.tradermade.com/api/v1/live?currency=EURGBP,GBPJPY&api_key=PXC--8DtI3s4Gbfptfd7
    
    // historical  
    https://marketdata.tradermade.com/api/v1/historical?date=2019-10-10&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical  
    https://marketdata.tradermade.com//api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical_sample  
    https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // minute_historical 
    https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2019-10-09-13:24&api_key=PXC--8DtI3s4Gbfptfd7
    
    // hour_historical  
    https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&date_time=2019-10-10-13:00&api_key=PXC--8DtI3s4Gbfptfd7
    
    // convert  
    https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
    
    // timeseries  
    https://marketdata.tradermade.com/api/v1/timeseries?start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
    
    // pandasDF  
    https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
                                
Copy
Live Rates
The live rates endpoint provides live sub-second data for over 4200+ currency pairs and 20+ CFDs. For the complete list, visit the live currencies list page or check the live currencies list endpoint section Node Providers, BlockChain and Smart Contract companies are allowed to request only one currency per request. Requesting multiple currencies will lead to several API call charges. For example, seeking five pairs in a single request will cost 5 API calls (only applicable to Blockchain Companies). Max currency pairs per call is limited to 10 unless otherwise agreed.

Params	Description
currency	EURUSD,GBPUSD,UK100
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live?currency=EURUSD,GBPUSD,UK100&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Rates
The historical endpoint provides daily exchange rate data for the available currency pairs. Our daily bars are 22/22 as is the norm in financial markets. The daily bar finishes at and starts from 22:00 GMT. Our API lets you query any trading day over the past 20+ years (for some exotic currency pairs history may be less). The trading week starts at 22:00 hours on a Sunday, and for a date requested for Saturday or Sunday, it returns the Friday date.

Params	Description
currency	EURUSD,GBPUSD
date	2019-10-09
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical?currency=EURUSD,GBPUSD&date=2019-10-09&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Tick Historical Rates
The Tick historical endpoint provides tick FX rate data for 50+ currency pairs. You can visit the historical currencies list page for a complete list of codes. Historical Tick provides one month of data with each chunk not exceeding 60 minutes. This feature is only available on Advanced plan and uses 5 API requests each time.You can request only one currency pair every time

You can't access tick historical data without an advanced plan. But you can request a sample tick (shown below), which will get you to tick data going back four working days, not including today. A maximum chunk of tick data in one request is 30 minutes and will take 5 requests away. You can only request one currency pair per request.

Params

Description

URL

/tick_historical/symbol/startdate/enddate

symbol

GBPUSD

startdate

YYYY-mm-dd HH:MM - (2025-04-10 08:30)

enddate

YYYY-mm-dd HH:MM - (2025-04-10 09:00)

format

json or csv - default is json

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?api_key=PXC--8DtI3s4Gbfptfd7&format=json
Copy



https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Minute Historical Rates
The API lets you query historical data for any minute for the past 30 years. You can only request one currency pair and one minute of data in one single request.

Params	Description
currency	EURUSD
date_time	YYYY-mm-dd-HH:MM
(2019-10-10-13:24)
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2025-04-11-10:29&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Hour Historical Rates
The API provides historical rates (OHLC) for the given hour over the past two years

Params	Description
currency	EURUSD
date_time	2019-10-10-13:00
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&date_time=2025-04-11-10:29 
Copy
Timeseries
Time series API provides historical currency rates (OHLC) for daily, hourly and granular endpoints. Daily timeseries data is available for up to 15 years (for some exotic currency pairs, history may be less). But the max request is one-year per request. You can get hourly data for up to 12 months (max one-month data per request) and minute interval data for up to one month (max 2-days data per call). For example, if you request 15-minute data on Friday, you can only request a start date from Thursday 00:00 GMT (in one call). You can seek one currency pair per call.

History - daily - fifteen years | hourly - 12 months | minute - 1 Month

You can also use our timeseries endpoint to plot data in highcharts - replace apikey with your API key. You can read the chart tutorial here

Params

Description

currency

EURUSD

start_date

daily - 2019-10-01 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

end_date

daily - 2019-10-10 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

interval

daily (other choices are - hourly or minute)

period

Daily Interval equals 1 | Hourly interval, choices are - 1, 2, 4, 6, 8, 24 | Minute interval, choices are - 1, 5, 10, 15, 30

format

records (other choices are - csv, index, columns, split)

api_key

Your API key

Request URL
Daily
Hourly
Minute
Response JSON
https://marketdata.tradermade.com/api/v1/timeseries?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records
Copy
Pandas Data Frame
PandasDF API endpoint provides daily OHLC data for the currency requested in a pandas Data Frame that makes it easy for python developers to use historical currency data. Request single currency when field parameter is "OHLC". You can request multiple currency when the field is "close". Data is available for upto 15 years (for some exotic currency pairs history may be less) but the max request is one-year per request.

Params

Description

currency

EURUSD

start_date

2019-10-01

end_date

2019-10-10

format

records (other choices are - index, columns, split)

fields

ohlc (another choice is - close)

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records&fields=ohlc
Copy
Convert
The API provides conversion from one currency to another in real time.

Params	Description
from	EUR
to	GBP
amount	1000
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
Copy
Examples
Below is an example showing the convert exchange rates data

PHP (CURL)
Python
R
Go
C#
JavaScript (axios)
JavaScript (fetch)
JavaScript (jQuery)
$curl = curl_init();
    
    curl_setopt_array( $curl, array(
        CURLOPT_PORT => "443",
        CURLOPT_URL => "https://marketdata.tradermade.com/api/v1/convert?from=EUR&to=USD&amount=1000&api_key=PXC--8DtI3s4Gbfptfd7",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => "",
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "GET",
    ));
    
    $response = curl_exec($curl);
    $err = curl_error($curl);
    
    curl_close($curl);
    
    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        echo $response;
    }
                                    
Copy
Products
Forex Data
CFD Data
Crypto Data
Live Streaming Data API
Download Historical Data
Resources
Data Documentation
Live Forex Rates
Currency Converter
Knowledge Base
Tutorials
Blog
Company
About Us
Contact Us
Affiliate Program
Startup Program
Pricing
View Pricing
Instagram
X
YouTube
LinkedIn
© 2024 Tradermade, All rights reserved

Terms of Service
Privacy Policy
We use cookies on this website. To learn more about cookies and how to manage your preferences, visit our cookies policy page.

ALLOW All
Accept only essential cookies

TraderMadetradermade logo
Product
Resources
Company
Pricing


Dashboard
Documentation
Restful API WebSockets FIX
RESTful API
Getting Started
Quick Start Guide
Authentication
Query Generator
Supported Currencies
Available SDK’s
Python
Kotlin
Error Codes
API Endpoints
Currency Data Endpoints
Live Rates
Historical Rates
Tick Historical Rates
Minute Historical Rates
Hour Historical Rates
Time-Series
Pandas
Convert
Examples
Getting Started
Welcome to TraderMade. We provide clean forex and CFD data via easy to use delivery methods. We use HTTPS and RESTful structures that make it easier to request data. Authentication is over a secure HTTPS protocol and responses are in JSON Format.

Following are a few simple steps to start getting data:

1. Sign up for API : Sign Up ↗
2. Get your API Key : API Key ↗.
3. Start getting data : API Endpoints ↗
Quick Start Guide
We have created a number of tutorials to help you get started with our REST API. Our tutorials cover topics such as Excel, Python, C#.

See our quick start tutorials : Visit Tutorials ↗
Also check our interactive API Definition : Technical Documentation ↗
Authentication
You need to include your API Key with each request to get data. You can find your API Key in your Dashboard once you signin. We will prepopulate your API Key for you to run sample API queries once you Sign In .

You can also learn more on how to use our forex data API on the tutorials page ↗

copied to clipboard!Error
Query Generator
1. Request URLCopy
https://marketdata.tradermade.com/api/v1/?api_key=PXC--8DtI3s4Gbfptfd7
Choose API Endpoint *

Select Endpoint
Insert your API key *
PXC--8DtI3s4Gbfptfd7
2. Select Parameters
Parameter 1

Select
Parameter 2

Select
Parameter 3

Select
Parameter 4

Select
Parameter 5

Select
Parameter 6

Select
Start and end date time must be GMT and not at a future period. Please check each endpoint docs to find out the data history available.

Run Query
                        

                    Copy
COPY
RESET QUERY
Supported Currencies
We support over 8000+ currency pairs on our API endpoints. It includes 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. We also have CFDs, Visit the CFD list page for codes.

Available SDKs
Python SDK
                        
pip install tradermade

                    Copy
Python users can install our SDK to start using our API in seconds. We recommend going through our python SDK documentation. Alternatively, you can read our tutorial on how to use our Python-SDK for Forex Data

                        
import tradermade as tm
# set api key
tm.set_rest_api_key("api_key")

#get data
tm.live(currency='EURUSD,GBPUSD',fields=["bid", "mid", "ask"]) # returns live data - fields is optional
    
tm.historical(currency='EURUSD,GBPUSD', date="2021-04-22",interval="daily", fields=["open", "high", "low","close"]) # returns historical data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.timeseries(currency='EURUSD', start="2025-04-10-00:00",end="2025-04-11-10:29",interval="hourly",fields=["open", "high", "low","close"]) # returns timeseries data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.cfd_list() # gets list of all cfds available
    
tm.currency_list() # gets list of all currency codes available add two codes to get code for currencypair ex EUR + USD gets EURUSD

                    Copy
Kotlin client JVM
                    
package io.tradermade.test_client_jvm

                Copy
Java and android users can setup our SDK in seconds. We recommend going through our Kotlin JVM Client.

                    

# set api key
val api = TraderMadeAPI("YOUR_API_KEY")

#get data
val liveData = api.getLiveData("EURUSD,GBPUSD") // returns live data 

val historicalData = api.getHistoricalData("EURUSD", "2023-08-01") // returns historical data for the currency requested.

val timeSeriesData = api.getTimeSeriesData("EURUSD", "2023-08-01", "2023-08-10", "daily", "1") // returns timeseries data for the currency requested interval is daily, hourly, minute.

val convertedAmount = api.convertCurrency("EUR", "USD", 1000.0) // returns live currency conversion rates 


                Copy
Error Codes
Below are the error codes and responses for all the API endpoints.

Codes
HTTP Status
Message
401
200 - OK
API Key is invalid | Your plan doesn't allow access to this dataset
204
200 - OK
Data for the date requested not available | Currency pair currently not available
400
400 - BAD REQUEST
Input payload validation failed (often due to a missing parameter or wrong input) Reasons may be an incorrect currency code, date format, or end date before the start date.
403
403 - Forbidden
No data for weekend | Data outside max historical data we provide
                        
// 400 will return error which includes the details of the error   
    {
        "errors": {
            "date": "YYYY-MM-DD time data '2019-10-' does not match format '%Y-%m-%d'"
        },
        "message": "Input payload validation failed"
    }

                    Copy
Data Endpoints
Live Currencies List
You can request the live_currencies_list endpoint to access a list of the available currencies for the /live and the /convert endpoint.endpoint. Add the currency codes to form a currency pair to request currency data. For example EURUSD can be requested by adding EUR and USD together. Reverse the quote to USDEUR to get the inverse of the same pair. To access the JSON object containing all available currency codes verus USD, append your api_key to the TraderMade exchange rates API apicurrencies endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Live Crypto List
We offer data for 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. A list of the available cryptocurrencies for the /live endpoint, can be accessed through requesting the live_cypto_list endpoint. In order to request currency data, add the currencies codes together to form a currency pair. For example DOGEUSD can be requested by adding DOGE and USD together. In order to get the inverse of the same pair, simply reverse the quote to USDDOGE. To access JSON object containing all available crypto codes verus USD, Simply append your api_key to the TraderMade live crypto API endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_crypto_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Currencies List
We support over 1600 currency pairs on our historical data endpoints. Request the historical_currencies_list endpoint or visit the list of historical exchange rates page to access a list of the available currencies for historical, pandasDF, timeseries, and the minute_historical endpoints. The below example is an abbreviated version.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Exchange rates API
The TraderMade exchange rates API has nine endpoints serving different sets of data. Below has one example for each of the endpoints.

Request URL

    // live endpoint 
    https://marketdata.tradermade.com/api/v1/live?currency=EURGBP,GBPJPY&api_key=PXC--8DtI3s4Gbfptfd7
    
    // historical  
    https://marketdata.tradermade.com/api/v1/historical?date=2019-10-10&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical  
    https://marketdata.tradermade.com//api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical_sample  
    https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // minute_historical 
    https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2019-10-09-13:24&api_key=PXC--8DtI3s4Gbfptfd7
    
    // hour_historical  
    https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&date_time=2019-10-10-13:00&api_key=PXC--8DtI3s4Gbfptfd7
    
    // convert  
    https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
    
    // timeseries  
    https://marketdata.tradermade.com/api/v1/timeseries?start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
    
    // pandasDF  
    https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
                                
Copy
Live Rates
The live rates endpoint provides live sub-second data for over 4200+ currency pairs and 20+ CFDs. For the complete list, visit the live currencies list page or check the live currencies list endpoint section Node Providers, BlockChain and Smart Contract companies are allowed to request only one currency per request. Requesting multiple currencies will lead to several API call charges. For example, seeking five pairs in a single request will cost 5 API calls (only applicable to Blockchain Companies). Max currency pairs per call is limited to 10 unless otherwise agreed.

Params	Description
currency	EURUSD,GBPUSD,UK100
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live?currency=EURUSD,GBPUSD,UK100&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Rates
The historical endpoint provides daily exchange rate data for the available currency pairs. Our daily bars are 22/22 as is the norm in financial markets. The daily bar finishes at and starts from 22:00 GMT. Our API lets you query any trading day over the past 20+ years (for some exotic currency pairs history may be less). The trading week starts at 22:00 hours on a Sunday, and for a date requested for Saturday or Sunday, it returns the Friday date.

Params	Description
currency	EURUSD,GBPUSD
date	2019-10-09
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical?currency=EURUSD,GBPUSD&date=2019-10-09&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Tick Historical Rates
The Tick historical endpoint provides tick FX rate data for 50+ currency pairs. You can visit the historical currencies list page for a complete list of codes. Historical Tick provides one month of data with each chunk not exceeding 60 minutes. This feature is only available on Advanced plan and uses 5 API requests each time.You can request only one currency pair every time

You can't access tick historical data without an advanced plan. But you can request a sample tick (shown below), which will get you to tick data going back four working days, not including today. A maximum chunk of tick data in one request is 30 minutes and will take 5 requests away. You can only request one currency pair per request.

Params

Description

URL

/tick_historical/symbol/startdate/enddate

symbol

GBPUSD

startdate

YYYY-mm-dd HH:MM - (2025-04-10 08:30)

enddate

YYYY-mm-dd HH:MM - (2025-04-10 09:00)

format

json or csv - default is json

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?api_key=PXC--8DtI3s4Gbfptfd7&format=json
Copy



https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Minute Historical Rates
The API lets you query historical data for any minute for the past 30 years. You can only request one currency pair and one minute of data in one single request.

Params	Description
currency	EURUSD
date_time	YYYY-mm-dd-HH:MM
(2019-10-10-13:24)
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2025-04-11-10:29&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Hour Historical Rates
The API provides historical rates (OHLC) for the given hour over the past two years

Params	Description
currency	EURUSD
date_time	2019-10-10-13:00
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&date_time=2025-04-11-10:29 
Copy
Timeseries
Time series API provides historical currency rates (OHLC) for daily, hourly and granular endpoints. Daily timeseries data is available for up to 15 years (for some exotic currency pairs, history may be less). But the max request is one-year per request. You can get hourly data for up to 12 months (max one-month data per request) and minute interval data for up to one month (max 2-days data per call). For example, if you request 15-minute data on Friday, you can only request a start date from Thursday 00:00 GMT (in one call). You can seek one currency pair per call.

History - daily - fifteen years | hourly - 12 months | minute - 1 Month

You can also use our timeseries endpoint to plot data in highcharts - replace apikey with your API key. You can read the chart tutorial here

Params

Description

currency

EURUSD

start_date

daily - 2019-10-01 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

end_date

daily - 2019-10-10 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

interval

daily (other choices are - hourly or minute)

period

Daily Interval equals 1 | Hourly interval, choices are - 1, 2, 4, 6, 8, 24 | Minute interval, choices are - 1, 5, 10, 15, 30

format

records (other choices are - csv, index, columns, split)

api_key

Your API key

Request URL
Daily
Hourly
Minute
Response JSON
https://marketdata.tradermade.com/api/v1/timeseries?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records
Copy
Pandas Data Frame
PandasDF API endpoint provides daily OHLC data for the currency requested in a pandas Data Frame that makes it easy for python developers to use historical currency data. Request single currency when field parameter is "OHLC". You can request multiple currency when the field is "close". Data is available for upto 15 years (for some exotic currency pairs history may be less) but the max request is one-year per request.

Params

Description

currency

EURUSD

start_date

2019-10-01

end_date

2019-10-10

format

records (other choices are - index, columns, split)

fields

ohlc (another choice is - close)

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records&fields=ohlc
Copy
Convert
The API provides conversion from one currency to another in real time.

Params	Description
from	EUR
to	GBP
amount	1000
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
Copy
Examples
Below is an example showing the convert exchange rates data

PHP (CURL)
Python
R
Go
C#
JavaScript (axios)
JavaScript (fetch)
JavaScript (jQuery)
$curl = curl_init();
    
    curl_setopt_array( $curl, array(
        CURLOPT_PORT => "443",
        CURLOPT_URL => "https://marketdata.tradermade.com/api/v1/convert?from=EUR&to=USD&amount=1000&api_key=PXC--8DtI3s4Gbfptfd7",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => "",
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "GET",
    ));
    
    $response = curl_exec($curl);
    $err = curl_error($curl);
    
    curl_close($curl);
    
    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        echo $response;
    }
                                    
Copy
Products
Forex Data
CFD Data
Crypto Data
Live Streaming Data API
Download Historical Data
Resources
Data Documentation
Live Forex Rates
Currency Converter
Knowledge Base
Tutorials
Blog
Company
About Us
Contact Us
Affiliate Program
Startup Program
Pricing
View Pricing
Instagram
X
YouTube
LinkedIn
© 2024 Tradermade, All rights reserved

Terms of Service
Privacy Policy
We use cookies on this website. To learn more about cookies and how to manage your preferences, visit our cookies policy page.

ALLOW All
Accept only essential cookies

TraderMadetradermade logo
Product
Resources
Company
Pricing


Dashboard
Documentation
Restful API WebSockets FIX
RESTful API
Getting Started
Quick Start Guide
Authentication
Query Generator
Supported Currencies
Available SDK’s
Python
Kotlin
Error Codes
API Endpoints
Currency Data Endpoints
Live Rates
Historical Rates
Tick Historical Rates
Minute Historical Rates
Hour Historical Rates
Time-Series
Pandas
Convert
Examples
Getting Started
Welcome to TraderMade. We provide clean forex and CFD data via easy to use delivery methods. We use HTTPS and RESTful structures that make it easier to request data. Authentication is over a secure HTTPS protocol and responses are in JSON Format.

Following are a few simple steps to start getting data:

1. Sign up for API : Sign Up ↗
2. Get your API Key : API Key ↗.
3. Start getting data : API Endpoints ↗
Quick Start Guide
We have created a number of tutorials to help you get started with our REST API. Our tutorials cover topics such as Excel, Python, C#.

See our quick start tutorials : Visit Tutorials ↗
Also check our interactive API Definition : Technical Documentation ↗
Authentication
You need to include your API Key with each request to get data. You can find your API Key in your Dashboard once you signin. We will prepopulate your API Key for you to run sample API queries once you Sign In .

You can also learn more on how to use our forex data API on the tutorials page ↗

copied to clipboard!Error
Query Generator
1. Request URLCopy
https://marketdata.tradermade.com/api/v1/?api_key=PXC--8DtI3s4Gbfptfd7
Choose API Endpoint *

Select Endpoint
Insert your API key *
PXC--8DtI3s4Gbfptfd7
2. Select Parameters
Parameter 1

Select
Parameter 2

Select
Parameter 3

Select
Parameter 4

Select
Parameter 5

Select
Parameter 6

Select
Start and end date time must be GMT and not at a future period. Please check each endpoint docs to find out the data history available.

Run Query
                        

                    Copy
COPY
RESET QUERY
Supported Currencies
We support over 8000+ currency pairs on our API endpoints. It includes 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. We also have CFDs, Visit the CFD list page for codes.

Available SDKs
Python SDK
                        
pip install tradermade

                    Copy
Python users can install our SDK to start using our API in seconds. We recommend going through our python SDK documentation. Alternatively, you can read our tutorial on how to use our Python-SDK for Forex Data

                        
import tradermade as tm
# set api key
tm.set_rest_api_key("api_key")

#get data
tm.live(currency='EURUSD,GBPUSD',fields=["bid", "mid", "ask"]) # returns live data - fields is optional
    
tm.historical(currency='EURUSD,GBPUSD', date="2021-04-22",interval="daily", fields=["open", "high", "low","close"]) # returns historical data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.timeseries(currency='EURUSD', start="2025-04-10-00:00",end="2025-04-11-10:29",interval="hourly",fields=["open", "high", "low","close"]) # returns timeseries data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.cfd_list() # gets list of all cfds available
    
tm.currency_list() # gets list of all currency codes available add two codes to get code for currencypair ex EUR + USD gets EURUSD

                    Copy
Kotlin client JVM
                    
package io.tradermade.test_client_jvm

                Copy
Java and android users can setup our SDK in seconds. We recommend going through our Kotlin JVM Client.

                    

# set api key
val api = TraderMadeAPI("YOUR_API_KEY")

#get data
val liveData = api.getLiveData("EURUSD,GBPUSD") // returns live data 

val historicalData = api.getHistoricalData("EURUSD", "2023-08-01") // returns historical data for the currency requested.

val timeSeriesData = api.getTimeSeriesData("EURUSD", "2023-08-01", "2023-08-10", "daily", "1") // returns timeseries data for the currency requested interval is daily, hourly, minute.

val convertedAmount = api.convertCurrency("EUR", "USD", 1000.0) // returns live currency conversion rates 


                Copy
Error Codes
Below are the error codes and responses for all the API endpoints.

Codes
HTTP Status
Message
401
200 - OK
API Key is invalid | Your plan doesn't allow access to this dataset
204
200 - OK
Data for the date requested not available | Currency pair currently not available
400
400 - BAD REQUEST
Input payload validation failed (often due to a missing parameter or wrong input) Reasons may be an incorrect currency code, date format, or end date before the start date.
403
403 - Forbidden
No data for weekend | Data outside max historical data we provide
                        
// 400 will return error which includes the details of the error   
    {
        "errors": {
            "date": "YYYY-MM-DD time data '2019-10-' does not match format '%Y-%m-%d'"
        },
        "message": "Input payload validation failed"
    }

                    Copy
Data Endpoints
Live Currencies List
You can request the live_currencies_list endpoint to access a list of the available currencies for the /live and the /convert endpoint.endpoint. Add the currency codes to form a currency pair to request currency data. For example EURUSD can be requested by adding EUR and USD together. Reverse the quote to USDEUR to get the inverse of the same pair. To access the JSON object containing all available currency codes verus USD, append your api_key to the TraderMade exchange rates API apicurrencies endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Live Crypto List
We offer data for 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. A list of the available cryptocurrencies for the /live endpoint, can be accessed through requesting the live_cypto_list endpoint. In order to request currency data, add the currencies codes together to form a currency pair. For example DOGEUSD can be requested by adding DOGE and USD together. In order to get the inverse of the same pair, simply reverse the quote to USDDOGE. To access JSON object containing all available crypto codes verus USD, Simply append your api_key to the TraderMade live crypto API endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_crypto_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Currencies List
We support over 1600 currency pairs on our historical data endpoints. Request the historical_currencies_list endpoint or visit the list of historical exchange rates page to access a list of the available currencies for historical, pandasDF, timeseries, and the minute_historical endpoints. The below example is an abbreviated version.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Exchange rates API
The TraderMade exchange rates API has nine endpoints serving different sets of data. Below has one example for each of the endpoints.

Request URL

    // live endpoint 
    https://marketdata.tradermade.com/api/v1/live?currency=EURGBP,GBPJPY&api_key=PXC--8DtI3s4Gbfptfd7
    
    // historical  
    https://marketdata.tradermade.com/api/v1/historical?date=2019-10-10&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical  
    https://marketdata.tradermade.com//api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical_sample  
    https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // minute_historical 
    https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2019-10-09-13:24&api_key=PXC--8DtI3s4Gbfptfd7
    
    // hour_historical  
    https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&date_time=2019-10-10-13:00&api_key=PXC--8DtI3s4Gbfptfd7
    
    // convert  
    https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
    
    // timeseries  
    https://marketdata.tradermade.com/api/v1/timeseries?start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
    
    // pandasDF  
    https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
                                
Copy
Live Rates
The live rates endpoint provides live sub-second data for over 4200+ currency pairs and 20+ CFDs. For the complete list, visit the live currencies list page or check the live currencies list endpoint section Node Providers, BlockChain and Smart Contract companies are allowed to request only one currency per request. Requesting multiple currencies will lead to several API call charges. For example, seeking five pairs in a single request will cost 5 API calls (only applicable to Blockchain Companies). Max currency pairs per call is limited to 10 unless otherwise agreed.

Params	Description
currency	EURUSD,GBPUSD,UK100
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live?currency=EURUSD,GBPUSD,UK100&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Rates
The historical endpoint provides daily exchange rate data for the available currency pairs. Our daily bars are 22/22 as is the norm in financial markets. The daily bar finishes at and starts from 22:00 GMT. Our API lets you query any trading day over the past 20+ years (for some exotic currency pairs history may be less). The trading week starts at 22:00 hours on a Sunday, and for a date requested for Saturday or Sunday, it returns the Friday date.

Params	Description
currency	EURUSD,GBPUSD
date	2019-10-09
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical?currency=EURUSD,GBPUSD&date=2019-10-09&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Tick Historical Rates
The Tick historical endpoint provides tick FX rate data for 50+ currency pairs. You can visit the historical currencies list page for a complete list of codes. Historical Tick provides one month of data with each chunk not exceeding 60 minutes. This feature is only available on Advanced plan and uses 5 API requests each time.You can request only one currency pair every time

You can't access tick historical data without an advanced plan. But you can request a sample tick (shown below), which will get you to tick data going back four working days, not including today. A maximum chunk of tick data in one request is 30 minutes and will take 5 requests away. You can only request one currency pair per request.

Params

Description

URL

/tick_historical/symbol/startdate/enddate

symbol

GBPUSD

startdate

YYYY-mm-dd HH:MM - (2025-04-10 08:30)

enddate

YYYY-mm-dd HH:MM - (2025-04-10 09:00)

format

json or csv - default is json

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?api_key=PXC--8DtI3s4Gbfptfd7&format=json
Copy



https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Minute Historical Rates
The API lets you query historical data for any minute for the past 30 years. You can only request one currency pair and one minute of data in one single request.

Params	Description
currency	EURUSD
date_time	YYYY-mm-dd-HH:MM
(2019-10-10-13:24)
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2025-04-11-10:29&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Hour Historical Rates
The API provides historical rates (OHLC) for the given hour over the past two years

Params	Description
currency	EURUSD
date_time	2019-10-10-13:00
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&date_time=2025-04-11-10:29 
Copy
Timeseries
Time series API provides historical currency rates (OHLC) for daily, hourly and granular endpoints. Daily timeseries data is available for up to 15 years (for some exotic currency pairs, history may be less). But the max request is one-year per request. You can get hourly data for up to 12 months (max one-month data per request) and minute interval data for up to one month (max 2-days data per call). For example, if you request 15-minute data on Friday, you can only request a start date from Thursday 00:00 GMT (in one call). You can seek one currency pair per call.

History - daily - fifteen years | hourly - 12 months | minute - 1 Month

You can also use our timeseries endpoint to plot data in highcharts - replace apikey with your API key. You can read the chart tutorial here

Params

Description

currency

EURUSD

start_date

daily - 2019-10-01 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

end_date

daily - 2019-10-10 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

interval

daily (other choices are - hourly or minute)

period

Daily Interval equals 1 | Hourly interval, choices are - 1, 2, 4, 6, 8, 24 | Minute interval, choices are - 1, 5, 10, 15, 30

format

records (other choices are - csv, index, columns, split)

api_key

Your API key

Request URL
Daily
Hourly
Minute
Response JSON
https://marketdata.tradermade.com/api/v1/timeseries?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records
Copy
Pandas Data Frame
PandasDF API endpoint provides daily OHLC data for the currency requested in a pandas Data Frame that makes it easy for python developers to use historical currency data. Request single currency when field parameter is "OHLC". You can request multiple currency when the field is "close". Data is available for upto 15 years (for some exotic currency pairs history may be less) but the max request is one-year per request.

Params

Description

currency

EURUSD

start_date

2019-10-01

end_date

2019-10-10

format

records (other choices are - index, columns, split)

fields

ohlc (another choice is - close)

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records&fields=ohlc
Copy
Convert
The API provides conversion from one currency to another in real time.

Params	Description
from	EUR
to	GBP
amount	1000
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
Copy
Examples
Below is an example showing the convert exchange rates data

PHP (CURL)
Python
R
Go
C#
JavaScript (axios)
JavaScript (fetch)
JavaScript (jQuery)
$curl = curl_init();
    
    curl_setopt_array( $curl, array(
        CURLOPT_PORT => "443",
        CURLOPT_URL => "https://marketdata.tradermade.com/api/v1/convert?from=EUR&to=USD&amount=1000&api_key=PXC--8DtI3s4Gbfptfd7",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => "",
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "GET",
    ));
    
    $response = curl_exec($curl);
    $err = curl_error($curl);
    
    curl_close($curl);
    
    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        echo $response;
    }
                                    
Copy
Products
Forex Data
CFD Data
Crypto Data
Live Streaming Data API
Download Historical Data
Resources
Data Documentation
Live Forex Rates
Currency Converter
Knowledge Base
Tutorials
Blog
Company
About Us
Contact Us
Affiliate Program
Startup Program
Pricing
View Pricing
Instagram
X
YouTube
LinkedIn
© 2024 Tradermade, All rights reserved

Terms of Service
Privacy Policy
We use cookies on this website. To learn more about cookies and how to manage your preferences, visit our cookies policy page.

ALLOW All
Accept only essential cookies

TraderMadetradermade logo
Product
Resources
Company
Pricing


Dashboard
Documentation
Restful API WebSockets FIX
RESTful API
Getting Started
Quick Start Guide
Authentication
Query Generator
Supported Currencies
Available SDK’s
Python
Kotlin
Error Codes
API Endpoints
Currency Data Endpoints
Live Rates
Historical Rates
Tick Historical Rates
Minute Historical Rates
Hour Historical Rates
Time-Series
Pandas
Convert
Examples
Getting Started
Welcome to TraderMade. We provide clean forex and CFD data via easy to use delivery methods. We use HTTPS and RESTful structures that make it easier to request data. Authentication is over a secure HTTPS protocol and responses are in JSON Format.

Following are a few simple steps to start getting data:

1. Sign up for API : Sign Up ↗
2. Get your API Key : API Key ↗.
3. Start getting data : API Endpoints ↗
Quick Start Guide
We have created a number of tutorials to help you get started with our REST API. Our tutorials cover topics such as Excel, Python, C#.

See our quick start tutorials : Visit Tutorials ↗
Also check our interactive API Definition : Technical Documentation ↗
Authentication
You need to include your API Key with each request to get data. You can find your API Key in your Dashboard once you signin. We will prepopulate your API Key for you to run sample API queries once you Sign In .

You can also learn more on how to use our forex data API on the tutorials page ↗

copied to clipboard!Error
Query Generator
1. Request URLCopy
https://marketdata.tradermade.com/api/v1/?api_key=PXC--8DtI3s4Gbfptfd7
Choose API Endpoint *

Select Endpoint
Insert your API key *
PXC--8DtI3s4Gbfptfd7
2. Select Parameters
Parameter 1

Select
Parameter 2

Select
Parameter 3

Select
Parameter 4

Select
Parameter 5

Select
Parameter 6

Select
Start and end date time must be GMT and not at a future period. Please check each endpoint docs to find out the data history available.

Run Query
                        

                    Copy
COPY
RESET QUERY
Supported Currencies
We support over 8000+ currency pairs on our API endpoints. It includes 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. We also have CFDs, Visit the CFD list page for codes.

Available SDKs
Python SDK
                        
pip install tradermade

                    Copy
Python users can install our SDK to start using our API in seconds. We recommend going through our python SDK documentation. Alternatively, you can read our tutorial on how to use our Python-SDK for Forex Data

                        
import tradermade as tm
# set api key
tm.set_rest_api_key("api_key")

#get data
tm.live(currency='EURUSD,GBPUSD',fields=["bid", "mid", "ask"]) # returns live data - fields is optional
    
tm.historical(currency='EURUSD,GBPUSD', date="2021-04-22",interval="daily", fields=["open", "high", "low","close"]) # returns historical data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.timeseries(currency='EURUSD', start="2025-04-10-00:00",end="2025-04-11-10:29",interval="hourly",fields=["open", "high", "low","close"]) # returns timeseries data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.cfd_list() # gets list of all cfds available
    
tm.currency_list() # gets list of all currency codes available add two codes to get code for currencypair ex EUR + USD gets EURUSD

                    Copy
Kotlin client JVM
                    
package io.tradermade.test_client_jvm

                Copy
Java and android users can setup our SDK in seconds. We recommend going through our Kotlin JVM Client.

                    

# set api key
val api = TraderMadeAPI("YOUR_API_KEY")

#get data
val liveData = api.getLiveData("EURUSD,GBPUSD") // returns live data 

val historicalData = api.getHistoricalData("EURUSD", "2023-08-01") // returns historical data for the currency requested.

val timeSeriesData = api.getTimeSeriesData("EURUSD", "2023-08-01", "2023-08-10", "daily", "1") // returns timeseries data for the currency requested interval is daily, hourly, minute.

val convertedAmount = api.convertCurrency("EUR", "USD", 1000.0) // returns live currency conversion rates 


                Copy
Error Codes
Below are the error codes and responses for all the API endpoints.

Codes
HTTP Status
Message
401
200 - OK
API Key is invalid | Your plan doesn't allow access to this dataset
204
200 - OK
Data for the date requested not available | Currency pair currently not available
400
400 - BAD REQUEST
Input payload validation failed (often due to a missing parameter or wrong input) Reasons may be an incorrect currency code, date format, or end date before the start date.
403
403 - Forbidden
No data for weekend | Data outside max historical data we provide
                        
// 400 will return error which includes the details of the error   
    {
        "errors": {
            "date": "YYYY-MM-DD time data '2019-10-' does not match format '%Y-%m-%d'"
        },
        "message": "Input payload validation failed"
    }

                    Copy
Data Endpoints
Live Currencies List
You can request the live_currencies_list endpoint to access a list of the available currencies for the /live and the /convert endpoint.endpoint. Add the currency codes to form a currency pair to request currency data. For example EURUSD can be requested by adding EUR and USD together. Reverse the quote to USDEUR to get the inverse of the same pair. To access the JSON object containing all available currency codes verus USD, append your api_key to the TraderMade exchange rates API apicurrencies endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Live Crypto List
We offer data for 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. A list of the available cryptocurrencies for the /live endpoint, can be accessed through requesting the live_cypto_list endpoint. In order to request currency data, add the currencies codes together to form a currency pair. For example DOGEUSD can be requested by adding DOGE and USD together. In order to get the inverse of the same pair, simply reverse the quote to USDDOGE. To access JSON object containing all available crypto codes verus USD, Simply append your api_key to the TraderMade live crypto API endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_crypto_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Currencies List
We support over 1600 currency pairs on our historical data endpoints. Request the historical_currencies_list endpoint or visit the list of historical exchange rates page to access a list of the available currencies for historical, pandasDF, timeseries, and the minute_historical endpoints. The below example is an abbreviated version.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Exchange rates API
The TraderMade exchange rates API has nine endpoints serving different sets of data. Below has one example for each of the endpoints.

Request URL

    // live endpoint 
    https://marketdata.tradermade.com/api/v1/live?currency=EURGBP,GBPJPY&api_key=PXC--8DtI3s4Gbfptfd7
    
    // historical  
    https://marketdata.tradermade.com/api/v1/historical?date=2019-10-10&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical  
    https://marketdata.tradermade.com//api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical_sample  
    https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // minute_historical 
    https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2019-10-09-13:24&api_key=PXC--8DtI3s4Gbfptfd7
    
    // hour_historical  
    https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&date_time=2019-10-10-13:00&api_key=PXC--8DtI3s4Gbfptfd7
    
    // convert  
    https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
    
    // timeseries  
    https://marketdata.tradermade.com/api/v1/timeseries?start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
    
    // pandasDF  
    https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
                                
Copy
Live Rates
The live rates endpoint provides live sub-second data for over 4200+ currency pairs and 20+ CFDs. For the complete list, visit the live currencies list page or check the live currencies list endpoint section Node Providers, BlockChain and Smart Contract companies are allowed to request only one currency per request. Requesting multiple currencies will lead to several API call charges. For example, seeking five pairs in a single request will cost 5 API calls (only applicable to Blockchain Companies). Max currency pairs per call is limited to 10 unless otherwise agreed.

Params	Description
currency	EURUSD,GBPUSD,UK100
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live?currency=EURUSD,GBPUSD,UK100&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Rates
The historical endpoint provides daily exchange rate data for the available currency pairs. Our daily bars are 22/22 as is the norm in financial markets. The daily bar finishes at and starts from 22:00 GMT. Our API lets you query any trading day over the past 20+ years (for some exotic currency pairs history may be less). The trading week starts at 22:00 hours on a Sunday, and for a date requested for Saturday or Sunday, it returns the Friday date.

Params	Description
currency	EURUSD,GBPUSD
date	2019-10-09
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical?currency=EURUSD,GBPUSD&date=2019-10-09&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Tick Historical Rates
The Tick historical endpoint provides tick FX rate data for 50+ currency pairs. You can visit the historical currencies list page for a complete list of codes. Historical Tick provides one month of data with each chunk not exceeding 60 minutes. This feature is only available on Advanced plan and uses 5 API requests each time.You can request only one currency pair every time

You can't access tick historical data without an advanced plan. But you can request a sample tick (shown below), which will get you to tick data going back four working days, not including today. A maximum chunk of tick data in one request is 30 minutes and will take 5 requests away. You can only request one currency pair per request.

Params

Description

URL

/tick_historical/symbol/startdate/enddate

symbol

GBPUSD

startdate

YYYY-mm-dd HH:MM - (2025-04-10 08:30)

enddate

YYYY-mm-dd HH:MM - (2025-04-10 09:00)

format

json or csv - default is json

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?api_key=PXC--8DtI3s4Gbfptfd7&format=json
Copy



https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Minute Historical Rates
The API lets you query historical data for any minute for the past 30 years. You can only request one currency pair and one minute of data in one single request.

Params	Description
currency	EURUSD
date_time	YYYY-mm-dd-HH:MM
(2019-10-10-13:24)
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2025-04-11-10:29&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Hour Historical Rates
The API provides historical rates (OHLC) for the given hour over the past two years

Params	Description
currency	EURUSD
date_time	2019-10-10-13:00
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&date_time=2025-04-11-10:29 
Copy
Timeseries
Time series API provides historical currency rates (OHLC) for daily, hourly and granular endpoints. Daily timeseries data is available for up to 15 years (for some exotic currency pairs, history may be less). But the max request is one-year per request. You can get hourly data for up to 12 months (max one-month data per request) and minute interval data for up to one month (max 2-days data per call). For example, if you request 15-minute data on Friday, you can only request a start date from Thursday 00:00 GMT (in one call). You can seek one currency pair per call.

History - daily - fifteen years | hourly - 12 months | minute - 1 Month

You can also use our timeseries endpoint to plot data in highcharts - replace apikey with your API key. You can read the chart tutorial here

Params

Description

currency

EURUSD

start_date

daily - 2019-10-01 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

end_date

daily - 2019-10-10 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

interval

daily (other choices are - hourly or minute)

period

Daily Interval equals 1 | Hourly interval, choices are - 1, 2, 4, 6, 8, 24 | Minute interval, choices are - 1, 5, 10, 15, 30

format

records (other choices are - csv, index, columns, split)

api_key

Your API key

Request URL
Daily
Hourly
Minute
Response JSON
https://marketdata.tradermade.com/api/v1/timeseries?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records
Copy
Pandas Data Frame
PandasDF API endpoint provides daily OHLC data for the currency requested in a pandas Data Frame that makes it easy for python developers to use historical currency data. Request single currency when field parameter is "OHLC". You can request multiple currency when the field is "close". Data is available for upto 15 years (for some exotic currency pairs history may be less) but the max request is one-year per request.

Params

Description

currency

EURUSD

start_date

2019-10-01

end_date

2019-10-10

format

records (other choices are - index, columns, split)

fields

ohlc (another choice is - close)

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records&fields=ohlc
Copy
Convert
The API provides conversion from one currency to another in real time.

Params	Description
from	EUR
to	GBP
amount	1000
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
Copy
Examples
Below is an example showing the convert exchange rates data

PHP (CURL)
Python
R
Go
C#
JavaScript (axios)
JavaScript (fetch)
JavaScript (jQuery)
$curl = curl_init();
    
    curl_setopt_array( $curl, array(
        CURLOPT_PORT => "443",
        CURLOPT_URL => "https://marketdata.tradermade.com/api/v1/convert?from=EUR&to=USD&amount=1000&api_key=PXC--8DtI3s4Gbfptfd7",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => "",
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "GET",
    ));
    
    $response = curl_exec($curl);
    $err = curl_error($curl);
    
    curl_close($curl);
    
    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        echo $response;
    }
                                    
Copy
Products
Forex Data
CFD Data
Crypto Data
Live Streaming Data API
Download Historical Data
Resources
Data Documentation
Live Forex Rates
Currency Converter
Knowledge Base
Tutorials
Blog
Company
About Us
Contact Us
Affiliate Program
Startup Program
Pricing
View Pricing
Instagram
X
YouTube
LinkedIn
© 2024 Tradermade, All rights reserved

Terms of Service
Privacy Policy
We use cookies on this website. To learn more about cookies and how to manage your preferences, visit our cookies policy page.

ALLOW All
Accept only essential cookies

TraderMadetradermade logo
Product
Resources
Company
Pricing


Dashboard
Documentation
Restful API WebSockets FIX
RESTful API
Getting Started
Quick Start Guide
Authentication
Query Generator
Supported Currencies
Available SDK’s
Python
Kotlin
Error Codes
API Endpoints
Currency Data Endpoints
Live Rates
Historical Rates
Tick Historical Rates
Minute Historical Rates
Hour Historical Rates
Time-Series
Pandas
Convert
Examples
Getting Started
Welcome to TraderMade. We provide clean forex and CFD data via easy to use delivery methods. We use HTTPS and RESTful structures that make it easier to request data. Authentication is over a secure HTTPS protocol and responses are in JSON Format.

Following are a few simple steps to start getting data:

1. Sign up for API : Sign Up ↗
2. Get your API Key : API Key ↗.
3. Start getting data : API Endpoints ↗
Quick Start Guide
We have created a number of tutorials to help you get started with our REST API. Our tutorials cover topics such as Excel, Python, C#.

See our quick start tutorials : Visit Tutorials ↗
Also check our interactive API Definition : Technical Documentation ↗
Authentication
You need to include your API Key with each request to get data. You can find your API Key in your Dashboard once you signin. We will prepopulate your API Key for you to run sample API queries once you Sign In .

You can also learn more on how to use our forex data API on the tutorials page ↗

copied to clipboard!Error
Query Generator
1. Request URLCopy
https://marketdata.tradermade.com/api/v1/?api_key=PXC--8DtI3s4Gbfptfd7
Choose API Endpoint *

Select Endpoint
Insert your API key *
PXC--8DtI3s4Gbfptfd7
2. Select Parameters
Parameter 1

Select
Parameter 2

Select
Parameter 3

Select
Parameter 4

Select
Parameter 5

Select
Parameter 6

Select
Start and end date time must be GMT and not at a future period. Please check each endpoint docs to find out the data history available.

Run Query
                        

                    Copy
COPY
RESET QUERY
Supported Currencies
We support over 8000+ currency pairs on our API endpoints. It includes 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. We also have CFDs, Visit the CFD list page for codes.

Available SDKs
Python SDK
                        
pip install tradermade

                    Copy
Python users can install our SDK to start using our API in seconds. We recommend going through our python SDK documentation. Alternatively, you can read our tutorial on how to use our Python-SDK for Forex Data

                        
import tradermade as tm
# set api key
tm.set_rest_api_key("api_key")

#get data
tm.live(currency='EURUSD,GBPUSD',fields=["bid", "mid", "ask"]) # returns live data - fields is optional
    
tm.historical(currency='EURUSD,GBPUSD', date="2021-04-22",interval="daily", fields=["open", "high", "low","close"]) # returns historical data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.timeseries(currency='EURUSD', start="2025-04-10-00:00",end="2025-04-11-10:29",interval="hourly",fields=["open", "high", "low","close"]) # returns timeseries data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.cfd_list() # gets list of all cfds available
    
tm.currency_list() # gets list of all currency codes available add two codes to get code for currencypair ex EUR + USD gets EURUSD

                    Copy
Kotlin client JVM
                    
package io.tradermade.test_client_jvm

                Copy
Java and android users can setup our SDK in seconds. We recommend going through our Kotlin JVM Client.

                    

# set api key
val api = TraderMadeAPI("YOUR_API_KEY")

#get data
val liveData = api.getLiveData("EURUSD,GBPUSD") // returns live data 

val historicalData = api.getHistoricalData("EURUSD", "2023-08-01") // returns historical data for the currency requested.

val timeSeriesData = api.getTimeSeriesData("EURUSD", "2023-08-01", "2023-08-10", "daily", "1") // returns timeseries data for the currency requested interval is daily, hourly, minute.

val convertedAmount = api.convertCurrency("EUR", "USD", 1000.0) // returns live currency conversion rates 


                Copy
Error Codes
Below are the error codes and responses for all the API endpoints.

Codes
HTTP Status
Message
401
200 - OK
API Key is invalid | Your plan doesn't allow access to this dataset
204
200 - OK
Data for the date requested not available | Currency pair currently not available
400
400 - BAD REQUEST
Input payload validation failed (often due to a missing parameter or wrong input) Reasons may be an incorrect currency code, date format, or end date before the start date.
403
403 - Forbidden
No data for weekend | Data outside max historical data we provide
                        
// 400 will return error which includes the details of the error   
    {
        "errors": {
            "date": "YYYY-MM-DD time data '2019-10-' does not match format '%Y-%m-%d'"
        },
        "message": "Input payload validation failed"
    }

                    Copy
Data Endpoints
Live Currencies List
You can request the live_currencies_list endpoint to access a list of the available currencies for the /live and the /convert endpoint.endpoint. Add the currency codes to form a currency pair to request currency data. For example EURUSD can be requested by adding EUR and USD together. Reverse the quote to USDEUR to get the inverse of the same pair. To access the JSON object containing all available currency codes verus USD, append your api_key to the TraderMade exchange rates API apicurrencies endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Live Crypto List
We offer data for 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. A list of the available cryptocurrencies for the /live endpoint, can be accessed through requesting the live_cypto_list endpoint. In order to request currency data, add the currencies codes together to form a currency pair. For example DOGEUSD can be requested by adding DOGE and USD together. In order to get the inverse of the same pair, simply reverse the quote to USDDOGE. To access JSON object containing all available crypto codes verus USD, Simply append your api_key to the TraderMade live crypto API endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_crypto_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Currencies List
We support over 1600 currency pairs on our historical data endpoints. Request the historical_currencies_list endpoint or visit the list of historical exchange rates page to access a list of the available currencies for historical, pandasDF, timeseries, and the minute_historical endpoints. The below example is an abbreviated version.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Exchange rates API
The TraderMade exchange rates API has nine endpoints serving different sets of data. Below has one example for each of the endpoints.

Request URL

    // live endpoint 
    https://marketdata.tradermade.com/api/v1/live?currency=EURGBP,GBPJPY&api_key=PXC--8DtI3s4Gbfptfd7
    
    // historical  
    https://marketdata.tradermade.com/api/v1/historical?date=2019-10-10&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical  
    https://marketdata.tradermade.com//api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical_sample  
    https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // minute_historical 
    https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2019-10-09-13:24&api_key=PXC--8DtI3s4Gbfptfd7
    
    // hour_historical  
    https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&date_time=2019-10-10-13:00&api_key=PXC--8DtI3s4Gbfptfd7
    
    // convert  
    https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
    
    // timeseries  
    https://marketdata.tradermade.com/api/v1/timeseries?start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
    
    // pandasDF  
    https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
                                
Copy
Live Rates
The live rates endpoint provides live sub-second data for over 4200+ currency pairs and 20+ CFDs. For the complete list, visit the live currencies list page or check the live currencies list endpoint section Node Providers, BlockChain and Smart Contract companies are allowed to request only one currency per request. Requesting multiple currencies will lead to several API call charges. For example, seeking five pairs in a single request will cost 5 API calls (only applicable to Blockchain Companies). Max currency pairs per call is limited to 10 unless otherwise agreed.

Params	Description
currency	EURUSD,GBPUSD,UK100
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live?currency=EURUSD,GBPUSD,UK100&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Rates
The historical endpoint provides daily exchange rate data for the available currency pairs. Our daily bars are 22/22 as is the norm in financial markets. The daily bar finishes at and starts from 22:00 GMT. Our API lets you query any trading day over the past 20+ years (for some exotic currency pairs history may be less). The trading week starts at 22:00 hours on a Sunday, and for a date requested for Saturday or Sunday, it returns the Friday date.

Params	Description
currency	EURUSD,GBPUSD
date	2019-10-09
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical?currency=EURUSD,GBPUSD&date=2019-10-09&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Tick Historical Rates
The Tick historical endpoint provides tick FX rate data for 50+ currency pairs. You can visit the historical currencies list page for a complete list of codes. Historical Tick provides one month of data with each chunk not exceeding 60 minutes. This feature is only available on Advanced plan and uses 5 API requests each time.You can request only one currency pair every time

You can't access tick historical data without an advanced plan. But you can request a sample tick (shown below), which will get you to tick data going back four working days, not including today. A maximum chunk of tick data in one request is 30 minutes and will take 5 requests away. You can only request one currency pair per request.

Params

Description

URL

/tick_historical/symbol/startdate/enddate

symbol

GBPUSD

startdate

YYYY-mm-dd HH:MM - (2025-04-10 08:30)

enddate

YYYY-mm-dd HH:MM - (2025-04-10 09:00)

format

json or csv - default is json

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?api_key=PXC--8DtI3s4Gbfptfd7&format=json
Copy



https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Minute Historical Rates
The API lets you query historical data for any minute for the past 30 years. You can only request one currency pair and one minute of data in one single request.

Params	Description
currency	EURUSD
date_time	YYYY-mm-dd-HH:MM
(2019-10-10-13:24)
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2025-04-11-10:29&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Hour Historical Rates
The API provides historical rates (OHLC) for the given hour over the past two years

Params	Description
currency	EURUSD
date_time	2019-10-10-13:00
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&date_time=2025-04-11-10:29 
Copy
Timeseries
Time series API provides historical currency rates (OHLC) for daily, hourly and granular endpoints. Daily timeseries data is available for up to 15 years (for some exotic currency pairs, history may be less). But the max request is one-year per request. You can get hourly data for up to 12 months (max one-month data per request) and minute interval data for up to one month (max 2-days data per call). For example, if you request 15-minute data on Friday, you can only request a start date from Thursday 00:00 GMT (in one call). You can seek one currency pair per call.

History - daily - fifteen years | hourly - 12 months | minute - 1 Month

You can also use our timeseries endpoint to plot data in highcharts - replace apikey with your API key. You can read the chart tutorial here

Params

Description

currency

EURUSD

start_date

daily - 2019-10-01 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

end_date

daily - 2019-10-10 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

interval

daily (other choices are - hourly or minute)

period

Daily Interval equals 1 | Hourly interval, choices are - 1, 2, 4, 6, 8, 24 | Minute interval, choices are - 1, 5, 10, 15, 30

format

records (other choices are - csv, index, columns, split)

api_key

Your API key

Request URL
Daily
Hourly
Minute
Response JSON
https://marketdata.tradermade.com/api/v1/timeseries?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records
Copy
Pandas Data Frame
PandasDF API endpoint provides daily OHLC data for the currency requested in a pandas Data Frame that makes it easy for python developers to use historical currency data. Request single currency when field parameter is "OHLC". You can request multiple currency when the field is "close". Data is available for upto 15 years (for some exotic currency pairs history may be less) but the max request is one-year per request.

Params

Description

currency

EURUSD

start_date

2019-10-01

end_date

2019-10-10

format

records (other choices are - index, columns, split)

fields

ohlc (another choice is - close)

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records&fields=ohlc
Copy
Convert
The API provides conversion from one currency to another in real time.

Params	Description
from	EUR
to	GBP
amount	1000
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
Copy
Examples
Below is an example showing the convert exchange rates data

PHP (CURL)
Python
R
Go
C#
JavaScript (axios)
JavaScript (fetch)
JavaScript (jQuery)
$curl = curl_init();
    
    curl_setopt_array( $curl, array(
        CURLOPT_PORT => "443",
        CURLOPT_URL => "https://marketdata.tradermade.com/api/v1/convert?from=EUR&to=USD&amount=1000&api_key=PXC--8DtI3s4Gbfptfd7",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => "",
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "GET",
    ));
    
    $response = curl_exec($curl);
    $err = curl_error($curl);
    
    curl_close($curl);
    
    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        echo $response;
    }
                                    
Copy
Products
Forex Data
CFD Data
Crypto Data
Live Streaming Data API
Download Historical Data
Resources
Data Documentation
Live Forex Rates
Currency Converter
Knowledge Base
Tutorials
Blog
Company
About Us
Contact Us
Affiliate Program
Startup Program
Pricing
View Pricing
Instagram
X
YouTube
LinkedIn
© 2024 Tradermade, All rights reserved

Terms of Service
Privacy Policy
We use cookies on this website. To learn more about cookies and how to manage your preferences, visit our cookies policy page.

ALLOW All
Accept only essential cookies

TraderMadetradermade logo
Product
Resources
Company
Pricing


Dashboard
Documentation
Restful API WebSockets FIX
RESTful API
Getting Started
Quick Start Guide
Authentication
Query Generator
Supported Currencies
Available SDK’s
Python
Kotlin
Error Codes
API Endpoints
Currency Data Endpoints
Live Rates
Historical Rates
Tick Historical Rates
Minute Historical Rates
Hour Historical Rates
Time-Series
Pandas
Convert
Examples
Getting Started
Welcome to TraderMade. We provide clean forex and CFD data via easy to use delivery methods. We use HTTPS and RESTful structures that make it easier to request data. Authentication is over a secure HTTPS protocol and responses are in JSON Format.

Following are a few simple steps to start getting data:

1. Sign up for API : Sign Up ↗
2. Get your API Key : API Key ↗.
3. Start getting data : API Endpoints ↗
Quick Start Guide
We have created a number of tutorials to help you get started with our REST API. Our tutorials cover topics such as Excel, Python, C#.

See our quick start tutorials : Visit Tutorials ↗
Also check our interactive API Definition : Technical Documentation ↗
Authentication
You need to include your API Key with each request to get data. You can find your API Key in your Dashboard once you signin. We will prepopulate your API Key for you to run sample API queries once you Sign In .

You can also learn more on how to use our forex data API on the tutorials page ↗

copied to clipboard!Error
Query Generator
1. Request URLCopy
https://marketdata.tradermade.com/api/v1/?api_key=PXC--8DtI3s4Gbfptfd7
Choose API Endpoint *

Select Endpoint
Insert your API key *
PXC--8DtI3s4Gbfptfd7
2. Select Parameters
Parameter 1

Select
Parameter 2

Select
Parameter 3

Select
Parameter 4

Select
Parameter 5

Select
Parameter 6

Select
Start and end date time must be GMT and not at a future period. Please check each endpoint docs to find out the data history available.

Run Query
                        

                    Copy
COPY
RESET QUERY
Supported Currencies
We support over 8000+ currency pairs on our API endpoints. It includes 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. We also have CFDs, Visit the CFD list page for codes.

Available SDKs
Python SDK
                        
pip install tradermade

                    Copy
Python users can install our SDK to start using our API in seconds. We recommend going through our python SDK documentation. Alternatively, you can read our tutorial on how to use our Python-SDK for Forex Data

                        
import tradermade as tm
# set api key
tm.set_rest_api_key("api_key")

#get data
tm.live(currency='EURUSD,GBPUSD',fields=["bid", "mid", "ask"]) # returns live data - fields is optional
    
tm.historical(currency='EURUSD,GBPUSD', date="2021-04-22",interval="daily", fields=["open", "high", "low","close"]) # returns historical data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.timeseries(currency='EURUSD', start="2025-04-10-00:00",end="2025-04-11-10:29",interval="hourly",fields=["open", "high", "low","close"]) # returns timeseries data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.cfd_list() # gets list of all cfds available
    
tm.currency_list() # gets list of all currency codes available add two codes to get code for currencypair ex EUR + USD gets EURUSD

                    Copy
Kotlin client JVM
                    
package io.tradermade.test_client_jvm

                Copy
Java and android users can setup our SDK in seconds. We recommend going through our Kotlin JVM Client.

                    

# set api key
val api = TraderMadeAPI("YOUR_API_KEY")

#get data
val liveData = api.getLiveData("EURUSD,GBPUSD") // returns live data 

val historicalData = api.getHistoricalData("EURUSD", "2023-08-01") // returns historical data for the currency requested.

val timeSeriesData = api.getTimeSeriesData("EURUSD", "2023-08-01", "2023-08-10", "daily", "1") // returns timeseries data for the currency requested interval is daily, hourly, minute.

val convertedAmount = api.convertCurrency("EUR", "USD", 1000.0) // returns live currency conversion rates 


                Copy
Error Codes
Below are the error codes and responses for all the API endpoints.

Codes
HTTP Status
Message
401
200 - OK
API Key is invalid | Your plan doesn't allow access to this dataset
204
200 - OK
Data for the date requested not available | Currency pair currently not available
400
400 - BAD REQUEST
Input payload validation failed (often due to a missing parameter or wrong input) Reasons may be an incorrect currency code, date format, or end date before the start date.
403
403 - Forbidden
No data for weekend | Data outside max historical data we provide
                        
// 400 will return error which includes the details of the error   
    {
        "errors": {
            "date": "YYYY-MM-DD time data '2019-10-' does not match format '%Y-%m-%d'"
        },
        "message": "Input payload validation failed"
    }

                    Copy
Data Endpoints
Live Currencies List
You can request the live_currencies_list endpoint to access a list of the available currencies for the /live and the /convert endpoint.endpoint. Add the currency codes to form a currency pair to request currency data. For example EURUSD can be requested by adding EUR and USD together. Reverse the quote to USDEUR to get the inverse of the same pair. To access the JSON object containing all available currency codes verus USD, append your api_key to the TraderMade exchange rates API apicurrencies endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Live Crypto List
We offer data for 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. A list of the available cryptocurrencies for the /live endpoint, can be accessed through requesting the live_cypto_list endpoint. In order to request currency data, add the currencies codes together to form a currency pair. For example DOGEUSD can be requested by adding DOGE and USD together. In order to get the inverse of the same pair, simply reverse the quote to USDDOGE. To access JSON object containing all available crypto codes verus USD, Simply append your api_key to the TraderMade live crypto API endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_crypto_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Currencies List
We support over 1600 currency pairs on our historical data endpoints. Request the historical_currencies_list endpoint or visit the list of historical exchange rates page to access a list of the available currencies for historical, pandasDF, timeseries, and the minute_historical endpoints. The below example is an abbreviated version.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Exchange rates API
The TraderMade exchange rates API has nine endpoints serving different sets of data. Below has one example for each of the endpoints.

Request URL

    // live endpoint 
    https://marketdata.tradermade.com/api/v1/live?currency=EURGBP,GBPJPY&api_key=PXC--8DtI3s4Gbfptfd7
    
    // historical  
    https://marketdata.tradermade.com/api/v1/historical?date=2019-10-10&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical  
    https://marketdata.tradermade.com//api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical_sample  
    https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // minute_historical 
    https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2019-10-09-13:24&api_key=PXC--8DtI3s4Gbfptfd7
    
    // hour_historical  
    https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&date_time=2019-10-10-13:00&api_key=PXC--8DtI3s4Gbfptfd7
    
    // convert  
    https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
    
    // timeseries  
    https://marketdata.tradermade.com/api/v1/timeseries?start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
    
    // pandasDF  
    https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
                                
Copy
Live Rates
The live rates endpoint provides live sub-second data for over 4200+ currency pairs and 20+ CFDs. For the complete list, visit the live currencies list page or check the live currencies list endpoint section Node Providers, BlockChain and Smart Contract companies are allowed to request only one currency per request. Requesting multiple currencies will lead to several API call charges. For example, seeking five pairs in a single request will cost 5 API calls (only applicable to Blockchain Companies). Max currency pairs per call is limited to 10 unless otherwise agreed.

Params	Description
currency	EURUSD,GBPUSD,UK100
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live?currency=EURUSD,GBPUSD,UK100&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Rates
The historical endpoint provides daily exchange rate data for the available currency pairs. Our daily bars are 22/22 as is the norm in financial markets. The daily bar finishes at and starts from 22:00 GMT. Our API lets you query any trading day over the past 20+ years (for some exotic currency pairs history may be less). The trading week starts at 22:00 hours on a Sunday, and for a date requested for Saturday or Sunday, it returns the Friday date.

Params	Description
currency	EURUSD,GBPUSD
date	2019-10-09
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical?currency=EURUSD,GBPUSD&date=2019-10-09&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Tick Historical Rates
The Tick historical endpoint provides tick FX rate data for 50+ currency pairs. You can visit the historical currencies list page for a complete list of codes. Historical Tick provides one month of data with each chunk not exceeding 60 minutes. This feature is only available on Advanced plan and uses 5 API requests each time.You can request only one currency pair every time

You can't access tick historical data without an advanced plan. But you can request a sample tick (shown below), which will get you to tick data going back four working days, not including today. A maximum chunk of tick data in one request is 30 minutes and will take 5 requests away. You can only request one currency pair per request.

Params

Description

URL

/tick_historical/symbol/startdate/enddate

symbol

GBPUSD

startdate

YYYY-mm-dd HH:MM - (2025-04-10 08:30)

enddate

YYYY-mm-dd HH:MM - (2025-04-10 09:00)

format

json or csv - default is json

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?api_key=PXC--8DtI3s4Gbfptfd7&format=json
Copy



https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Minute Historical Rates
The API lets you query historical data for any minute for the past 30 years. You can only request one currency pair and one minute of data in one single request.

Params	Description
currency	EURUSD
date_time	YYYY-mm-dd-HH:MM
(2019-10-10-13:24)
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2025-04-11-10:29&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Hour Historical Rates
The API provides historical rates (OHLC) for the given hour over the past two years

Params	Description
currency	EURUSD
date_time	2019-10-10-13:00
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&date_time=2025-04-11-10:29 
Copy
Timeseries
Time series API provides historical currency rates (OHLC) for daily, hourly and granular endpoints. Daily timeseries data is available for up to 15 years (for some exotic currency pairs, history may be less). But the max request is one-year per request. You can get hourly data for up to 12 months (max one-month data per request) and minute interval data for up to one month (max 2-days data per call). For example, if you request 15-minute data on Friday, you can only request a start date from Thursday 00:00 GMT (in one call). You can seek one currency pair per call.

History - daily - fifteen years | hourly - 12 months | minute - 1 Month

You can also use our timeseries endpoint to plot data in highcharts - replace apikey with your API key. You can read the chart tutorial here

Params

Description

currency

EURUSD

start_date

daily - 2019-10-01 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

end_date

daily - 2019-10-10 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

interval

daily (other choices are - hourly or minute)

period

Daily Interval equals 1 | Hourly interval, choices are - 1, 2, 4, 6, 8, 24 | Minute interval, choices are - 1, 5, 10, 15, 30

format

records (other choices are - csv, index, columns, split)

api_key

Your API key

Request URL
Daily
Hourly
Minute
Response JSON
https://marketdata.tradermade.com/api/v1/timeseries?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records
Copy
Pandas Data Frame
PandasDF API endpoint provides daily OHLC data for the currency requested in a pandas Data Frame that makes it easy for python developers to use historical currency data. Request single currency when field parameter is "OHLC". You can request multiple currency when the field is "close". Data is available for upto 15 years (for some exotic currency pairs history may be less) but the max request is one-year per request.

Params

Description

currency

EURUSD

start_date

2019-10-01

end_date

2019-10-10

format

records (other choices are - index, columns, split)

fields

ohlc (another choice is - close)

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records&fields=ohlc
Copy
Convert
The API provides conversion from one currency to another in real time.

Params	Description
from	EUR
to	GBP
amount	1000
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
Copy
Examples
Below is an example showing the convert exchange rates data

PHP (CURL)
Python
R
Go
C#
JavaScript (axios)
JavaScript (fetch)
JavaScript (jQuery)
$curl = curl_init();
    
    curl_setopt_array( $curl, array(
        CURLOPT_PORT => "443",
        CURLOPT_URL => "https://marketdata.tradermade.com/api/v1/convert?from=EUR&to=USD&amount=1000&api_key=PXC--8DtI3s4Gbfptfd7",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => "",
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "GET",
    ));
    
    $response = curl_exec($curl);
    $err = curl_error($curl);
    
    curl_close($curl);
    
    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        echo $response;
    }
                                    
Copy
Products
Forex Data
CFD Data
Crypto Data
Live Streaming Data API
Download Historical Data
Resources
Data Documentation
Live Forex Rates
Currency Converter
Knowledge Base
Tutorials
Blog
Company
About Us
Contact Us
Affiliate Program
Startup Program
Pricing
View Pricing
Instagram
X
YouTube
LinkedIn
© 2024 Tradermade, All rights reserved

Terms of Service
Privacy Policy
We use cookies on this website. To learn more about cookies and how to manage your preferences, visit our cookies policy page.

ALLOW All
Accept only essential cookies

TraderMadetradermade logo
Product
Resources
Company
Pricing


Dashboard
Documentation
Restful API WebSockets FIX
RESTful API
Getting Started
Quick Start Guide
Authentication
Query Generator
Supported Currencies
Available SDK’s
Python
Kotlin
Error Codes
API Endpoints
Currency Data Endpoints
Live Rates
Historical Rates
Tick Historical Rates
Minute Historical Rates
Hour Historical Rates
Time-Series
Pandas
Convert
Examples
Getting Started
Welcome to TraderMade. We provide clean forex and CFD data via easy to use delivery methods. We use HTTPS and RESTful structures that make it easier to request data. Authentication is over a secure HTTPS protocol and responses are in JSON Format.

Following are a few simple steps to start getting data:

1. Sign up for API : Sign Up ↗
2. Get your API Key : API Key ↗.
3. Start getting data : API Endpoints ↗
Quick Start Guide
We have created a number of tutorials to help you get started with our REST API. Our tutorials cover topics such as Excel, Python, C#.

See our quick start tutorials : Visit Tutorials ↗
Also check our interactive API Definition : Technical Documentation ↗
Authentication
You need to include your API Key with each request to get data. You can find your API Key in your Dashboard once you signin. We will prepopulate your API Key for you to run sample API queries once you Sign In .

You can also learn more on how to use our forex data API on the tutorials page ↗

copied to clipboard!Error
Query Generator
1. Request URLCopy
https://marketdata.tradermade.com/api/v1/?api_key=PXC--8DtI3s4Gbfptfd7
Choose API Endpoint *

Select Endpoint
Insert your API key *
PXC--8DtI3s4Gbfptfd7
2. Select Parameters
Parameter 1

Select
Parameter 2

Select
Parameter 3

Select
Parameter 4

Select
Parameter 5

Select
Parameter 6

Select
Start and end date time must be GMT and not at a future period. Please check each endpoint docs to find out the data history available.

Run Query
                        

                    Copy
COPY
RESET QUERY
Supported Currencies
We support over 8000+ currency pairs on our API endpoints. It includes 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. We also have CFDs, Visit the CFD list page for codes.

Available SDKs
Python SDK
                        
pip install tradermade

                    Copy
Python users can install our SDK to start using our API in seconds. We recommend going through our python SDK documentation. Alternatively, you can read our tutorial on how to use our Python-SDK for Forex Data

                        
import tradermade as tm
# set api key
tm.set_rest_api_key("api_key")

#get data
tm.live(currency='EURUSD,GBPUSD',fields=["bid", "mid", "ask"]) # returns live data - fields is optional
    
tm.historical(currency='EURUSD,GBPUSD', date="2021-04-22",interval="daily", fields=["open", "high", "low","close"]) # returns historical data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.timeseries(currency='EURUSD', start="2025-04-10-00:00",end="2025-04-11-10:29",interval="hourly",fields=["open", "high", "low","close"]) # returns timeseries data for the currency requested interval is daily, hourly, minute - fields is optional
    
tm.cfd_list() # gets list of all cfds available
    
tm.currency_list() # gets list of all currency codes available add two codes to get code for currencypair ex EUR + USD gets EURUSD

                    Copy
Kotlin client JVM
                    
package io.tradermade.test_client_jvm

                Copy
Java and android users can setup our SDK in seconds. We recommend going through our Kotlin JVM Client.

                    

# set api key
val api = TraderMadeAPI("YOUR_API_KEY")

#get data
val liveData = api.getLiveData("EURUSD,GBPUSD") // returns live data 

val historicalData = api.getHistoricalData("EURUSD", "2023-08-01") // returns historical data for the currency requested.

val timeSeriesData = api.getTimeSeriesData("EURUSD", "2023-08-01", "2023-08-10", "daily", "1") // returns timeseries data for the currency requested interval is daily, hourly, minute.

val convertedAmount = api.convertCurrency("EUR", "USD", 1000.0) // returns live currency conversion rates 


                Copy
Error Codes
Below are the error codes and responses for all the API endpoints.

Codes
HTTP Status
Message
401
200 - OK
API Key is invalid | Your plan doesn't allow access to this dataset
204
200 - OK
Data for the date requested not available | Currency pair currently not available
400
400 - BAD REQUEST
Input payload validation failed (often due to a missing parameter or wrong input) Reasons may be an incorrect currency code, date format, or end date before the start date.
403
403 - Forbidden
No data for weekend | Data outside max historical data we provide
                        
// 400 will return error which includes the details of the error   
    {
        "errors": {
            "date": "YYYY-MM-DD time data '2019-10-' does not match format '%Y-%m-%d'"
        },
        "message": "Input payload validation failed"
    }

                    Copy
Data Endpoints
Live Currencies List
You can request the live_currencies_list endpoint to access a list of the available currencies for the /live and the /convert endpoint.endpoint. Add the currency codes to form a currency pair to request currency data. For example EURUSD can be requested by adding EUR and USD together. Reverse the quote to USDEUR to get the inverse of the same pair. To access the JSON object containing all available currency codes verus USD, append your api_key to the TraderMade exchange rates API apicurrencies endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Live Crypto List
We offer data for 4000+ cryptocurrency pairs. A list of Forex and Crypto codes for live endpoint can be accessed by visting our live currencies list page. A list of the available cryptocurrencies for the /live endpoint, can be accessed through requesting the live_cypto_list endpoint. In order to request currency data, add the currencies codes together to form a currency pair. For example DOGEUSD can be requested by adding DOGE and USD together. In order to get the inverse of the same pair, simply reverse the quote to USDDOGE. To access JSON object containing all available crypto codes verus USD, Simply append your api_key to the TraderMade live crypto API endpoint.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live_crypto_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Currencies List
We support over 1600 currency pairs on our historical data endpoints. Request the historical_currencies_list endpoint or visit the list of historical exchange rates page to access a list of the available currencies for historical, pandasDF, timeseries, and the minute_historical endpoints. The below example is an abbreviated version.

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical_currencies_list?api_key=PXC--8DtI3s4Gbfptfd7
Copy
Exchange rates API
The TraderMade exchange rates API has nine endpoints serving different sets of data. Below has one example for each of the endpoints.

Request URL

    // live endpoint 
    https://marketdata.tradermade.com/api/v1/live?currency=EURGBP,GBPJPY&api_key=PXC--8DtI3s4Gbfptfd7
    
    // historical  
    https://marketdata.tradermade.com/api/v1/historical?date=2019-10-10&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical  
    https://marketdata.tradermade.com//api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // tick_historical_sample  
    https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
    
    // minute_historical 
    https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2019-10-09-13:24&api_key=PXC--8DtI3s4Gbfptfd7
    
    // hour_historical  
    https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&date_time=2019-10-10-13:00&api_key=PXC--8DtI3s4Gbfptfd7
    
    // convert  
    https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
    
    // timeseries  
    https://marketdata.tradermade.com/api/v1/timeseries?start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
    
    // pandasDF  
    https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&start_date=2015-01-01&end_date=2015-05-01&api_key=PXC--8DtI3s4Gbfptfd7
                                
Copy
Live Rates
The live rates endpoint provides live sub-second data for over 4200+ currency pairs and 20+ CFDs. For the complete list, visit the live currencies list page or check the live currencies list endpoint section Node Providers, BlockChain and Smart Contract companies are allowed to request only one currency per request. Requesting multiple currencies will lead to several API call charges. For example, seeking five pairs in a single request will cost 5 API calls (only applicable to Blockchain Companies). Max currency pairs per call is limited to 10 unless otherwise agreed.

Params	Description
currency	EURUSD,GBPUSD,UK100
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/live?currency=EURUSD,GBPUSD,UK100&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Historical Rates
The historical endpoint provides daily exchange rate data for the available currency pairs. Our daily bars are 22/22 as is the norm in financial markets. The daily bar finishes at and starts from 22:00 GMT. Our API lets you query any trading day over the past 20+ years (for some exotic currency pairs history may be less). The trading week starts at 22:00 hours on a Sunday, and for a date requested for Saturday or Sunday, it returns the Friday date.

Params	Description
currency	EURUSD,GBPUSD
date	2019-10-09
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/historical?currency=EURUSD,GBPUSD&date=2019-10-09&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Tick Historical Rates
The Tick historical endpoint provides tick FX rate data for 50+ currency pairs. You can visit the historical currencies list page for a complete list of codes. Historical Tick provides one month of data with each chunk not exceeding 60 minutes. This feature is only available on Advanced plan and uses 5 API requests each time.You can request only one currency pair every time

You can't access tick historical data without an advanced plan. But you can request a sample tick (shown below), which will get you to tick data going back four working days, not including today. A maximum chunk of tick data in one request is 30 minutes and will take 5 requests away. You can only request one currency pair per request.

Params

Description

URL

/tick_historical/symbol/startdate/enddate

symbol

GBPUSD

startdate

YYYY-mm-dd HH:MM - (2025-04-10 08:30)

enddate

YYYY-mm-dd HH:MM - (2025-04-10 09:00)

format

json or csv - default is json

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/tick_historical/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?api_key=PXC--8DtI3s4Gbfptfd7&format=json
Copy



https://marketdata.tradermade.com//api/v1/tick_historical_sample/GBPUSD/2025-04-10 08:30/2025-04-10 09:00?format=json&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Minute Historical Rates
The API lets you query historical data for any minute for the past 30 years. You can only request one currency pair and one minute of data in one single request.

Params	Description
currency	EURUSD
date_time	YYYY-mm-dd-HH:MM
(2019-10-10-13:24)
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/minute_historical?currency=EURUSD&date_time=2025-04-11-10:29&api_key=PXC--8DtI3s4Gbfptfd7
Copy
Hour Historical Rates
The API provides historical rates (OHLC) for the given hour over the past two years

Params	Description
currency	EURUSD
date_time	2019-10-10-13:00
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/hour_historical?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&date_time=2025-04-11-10:29 
Copy
Timeseries
Time series API provides historical currency rates (OHLC) for daily, hourly and granular endpoints. Daily timeseries data is available for up to 15 years (for some exotic currency pairs, history may be less). But the max request is one-year per request. You can get hourly data for up to 12 months (max one-month data per request) and minute interval data for up to one month (max 2-days data per call). For example, if you request 15-minute data on Friday, you can only request a start date from Thursday 00:00 GMT (in one call). You can seek one currency pair per call.

History - daily - fifteen years | hourly - 12 months | minute - 1 Month

You can also use our timeseries endpoint to plot data in highcharts - replace apikey with your API key. You can read the chart tutorial here

Params

Description

currency

EURUSD

start_date

daily - 2019-10-01 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

end_date

daily - 2019-10-10 (YYYY-MM-DD) | hourly / minute - (YYYY-MM-DD-HH:MM)

interval

daily (other choices are - hourly or minute)

period

Daily Interval equals 1 | Hourly interval, choices are - 1, 2, 4, 6, 8, 24 | Minute interval, choices are - 1, 5, 10, 15, 30

format

records (other choices are - csv, index, columns, split)

api_key

Your API key

Request URL
Daily
Hourly
Minute
Response JSON
https://marketdata.tradermade.com/api/v1/timeseries?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records
Copy
Pandas Data Frame
PandasDF API endpoint provides daily OHLC data for the currency requested in a pandas Data Frame that makes it easy for python developers to use historical currency data. Request single currency when field parameter is "OHLC". You can request multiple currency when the field is "close". Data is available for upto 15 years (for some exotic currency pairs history may be less) but the max request is one-year per request.

Params

Description

currency

EURUSD

start_date

2019-10-01

end_date

2019-10-10

format

records (other choices are - index, columns, split)

fields

ohlc (another choice is - close)

api_key

Your API key

Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/pandasDF?currency=EURUSD&api_key=PXC--8DtI3s4Gbfptfd7&start_date=2019-10-01&end_date=2019-10-10&format=records&fields=ohlc
Copy
Convert
The API provides conversion from one currency to another in real time.

Params	Description
from	EUR
to	GBP
amount	1000
api_key	Your API key
Request URL
Response JSON
https://marketdata.tradermade.com/api/v1/convert?api_key=PXC--8DtI3s4Gbfptfd7&from=EUR&to=GBP&amount=1000
Copy
Examples
Below is an example showing the convert exchange rates data

PHP (CURL)
Python
R
Go
C#
JavaScript (axios)
JavaScript (fetch)
JavaScript (jQuery)
$curl = curl_init();
    
    curl_setopt_array( $curl, array(
        CURLOPT_PORT => "443",
        CURLOPT_URL => "https://marketdata.tradermade.com/api/v1/convert?from=EUR&to=USD&amount=1000&api_key=PXC--8DtI3s4Gbfptfd7",
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => "",
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "GET",
    ));
    
    $response = curl_exec($curl);
    $err = curl_error($curl);
    
    curl_close($curl);
    
    if ($err) {
        echo "cURL Error #:" . $err;
    } else {
        echo $response;
    }
                                    
Copy
Products
Forex Data
CFD Data
Crypto Data
Live Streaming Data API
Download Historical Data
Resources
Data Documentation
Live Forex Rates
Currency Converter
Knowledge Base
Tutorials
Blog
Company
About Us
Contact Us
Affiliate Program
Startup Program
Pricing
View Pricing
Instagram
X
YouTube
LinkedIn
© 2024 Tradermade, All rights reserved

Terms of Service
Privacy Policy
We use cookies on this website. To learn more about cookies and how to manage your preferences, visit our cookies policy page.

ALLOW All
Accept only essential cookies

