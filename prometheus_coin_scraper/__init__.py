import sys

from prometheus_coin_scraper.PrometheusClient import PrometheusClient

if __name__ == '__main__':
    port = int(sys.argv[1])
    client = PrometheusClient(port=port)
