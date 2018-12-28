import threading
import time

from cryptocurrencies_scraper.CurrencyService import Manager
from prometheus_client import start_http_server, Gauge


class PrometheusClient:
    FETCH_TIME = Gauge('coin_scrapper_fetch_time', 'Time spent fetching all currencies values')
    UPDATE_TIME_GAUGES = Gauge('coin_scrapper_gauge_update_time',
                               'Time spent updating all gauge values')
    LAST_FETCH_DATE = Gauge('coin_scrapper_last_update', 'Last time coin values have been updated')
    NUMBER_CURRENCIES = Gauge('coin_scrapper_currencies_number', "Display the current number of updated currencies")
    COIN_USD_VALUES = Gauge('coin_scrapper_coin_value_usd', "Value of multiple coins", ['symbol', 'name', 'source'])
    COIN_BTC_VALUES = Gauge('coin_scrapper_coin_value_btc', "Value of multiple coins", ['symbol', 'name', 'source'])
    COIN_LAST_PLATFORM_UPDATE = Gauge('coin_scrapper_coin_last_platform_update', "last update of multiple coins",
                                      ['symbol', 'name', 'source'])
    COIN_CHANGES_VALUES = Gauge('coin_scrapper_coin_changes', "changes over time of multiple coins",
                                ['symbol', 'name', 'source', 'interval'])

    manager: Manager = None

    def __init__(self, port=8000):
        self.manager = Manager()
        start_http_server(port)

        def init_timer():
            self.update_data()
            print("Updated !")

            self.update_gauges()
            threading.Timer(30, init_timer).start()

        init_timer()
        while True:
            time.sleep(1000)

    @FETCH_TIME.time()
    def update_data(self):
        try:
            self.manager.update()
            self.LAST_FETCH_DATE.set_to_current_time()
        except:
            print("Error while fetching....")

    @UPDATE_TIME_GAUGES.time()
    def update_gauges(self):
        self.NUMBER_CURRENCIES.set(len(self.manager.all_currencies()))
        for k, coinlist in self.manager.all_currencies().items():
            for coin in coinlist:
                self.COIN_USD_VALUES.labels(coin.symbol.upper(), coin.name.lower(), coin.source).set(coin.valueUSD)
                self.COIN_BTC_VALUES.labels(coin.symbol.upper(), coin.name.lower(), coin.source).set(coin.valueBTC)
                self.COIN_LAST_PLATFORM_UPDATE.labels(coin.symbol.upper(), coin.name.lower(), coin.source).set(
                    coin.lastUpdate)
                for it, change in coin.changes.items():
                    self.COIN_CHANGES_VALUES.labels(coin.symbol.upper(), coin.name.lower(), coin.source, it).set(change)
