import requests_mock
import time
import signal
import requests
import math
import cmath
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException
from binance.validation import validate_order
from binance.enums import TIME_IN_FORCE_GTC, SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET
import trading_core
class Coin:

    def __init__(self, name, symbol, price, client):
        self.name = name
        self.symbol=symbol
        self.price = price
        self.maxima=max(price)
        self.minima=min(price)
        self.client=client

    def difference(self):
        self.maxima = max(self.price)
        self.minima = min(self.price)
        return trading_core.diff(self.maxima, self.minima)

    def niddle_judge(self):
        self.maxima = max(self.price)
        self.minima = min(self.price)
        if trading_core.diff(self.maxima,self.minima)<-50:
            return True
        else:
            return False

    def get_book(self):
        try:
            return self.client.get_order_book(symbol=self.symbol)
        except requests.exceptions.ConnectionError:
            print("Error in getting orderbook, connection refused by the server..")
            time.sleep(0.5)
            return None
        except ValueError:
            print("value error in get order book")
            return None
        except:
            return None

    def market_price(self):
        try:
            return self.client.get_ticker(symbol=self.symbol)
        except requests.exceptions.ConnectionError:
            print("Error in getting market_price, connection refused by the server..")
            time.sleep(5)
            return None
        except ValueError:
            print("value error in getting market price")
            return None
        except:
            return None


