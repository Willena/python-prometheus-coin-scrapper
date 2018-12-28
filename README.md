# prometheus coin scraper : A simple metric provider for prometheus

This provide a set of metric for all cryptocurencies listed on https://coin360.com/ and http://coinmarketcap.com/

A lot of values are generated from this scrapper ~10000 values today (27/12/2018)

## How to use

Install the pip package 

```
pip install prometheus_coin_scraper
```

to start the metric server that will serve all metrics you can use the following command

```
python -m prometheus_coin_scraper [webport]
```

## In-code usage

This module is also usable inside you code and will produce very simple webserver that is by default reachable on 
http://localhost:8000/ and displays all metrics in a prometheus compatible format

```python
from prometheus_coin_scraper.PrometheusClient import PrometheusClient

PrometheusClient(port=8000)

```

This class start and run the web server. As it is a blocking call you might need to start it in a Thread

```python
from prometheus_coin_scraper.PrometheusClient import PrometheusClient
from threading import Thread

def func():
    PrometheusClient(port=8000)

Thread(target=func).start()
```

## Information on collected Metrics

- `coin_scrapper_fetch_time` : The time spent fetching all currencies values
- `coin_scrapper_gauge_update_time` : The time spent updating all prometheus Gauges values
- `coin_scrapper_last_update` : Last update time
- `coin_scrapper_currencies_number`: The current number currencies in the Index
- `coin_scrapper_coin_value_usd`: Coin value in USD
    
    There are three labels 
    - `symbol`: The currency symbol (BTC, LTC, XRP, ...)
    - `name` : The currency name (Bitcoin, Litecoin, Ripple, ...)
    - `source` : The name of the source for the currency value (coin360.com, ...)
    
- `coin_scrapper_coin_value_btc`:  Coin value in BTC  

    There are three labels 
    - `symbol`: The currency symbol (BTC, LTC, XRP, ...)
    - `name` : The currency name (Bitcoin, Litecoin, Ripple, ...)
    - `source` : The name of the source for the currency value (coin360.com, ...)
    
- `coin_scrapper_coin_last_platform_update` Last update of the coin on the source 

    There are three labels 
    - `symbol`: The currency symbol (BTC, LTC, XRP, ...)
    - `name` : The currency name (Bitcoin, Litecoin, Ripple, ...)
    - `source` : The name of the source for the currency value (coin360.com, ...)
    
- `coin_scrapper_coin_changes` : Calculated changes of the coin over time (1h, 24h, 7d) 

    There are three labels 
    - `symbol`: The currency symbol (BTC, LTC, XRP, ...)
    - `name` : The currency name (Bitcoin, Litecoin, Ripple, ...)
    - `source` : The name of the source for the currency value (coin360.com, ...)
    - `interval`: The interval for the calculated value (1h, 24h or 7d)
    