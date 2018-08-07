from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException
import pytest
import requests_mock
import time
from time import sleep
import signal
import requests
import math
import cmath
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException
from binance.validation import validate_order
from binance.enums import TIME_IN_FORCE_GTC, SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET
import coin
def diff(a,b):
    return (b-a)/a*100
def market_info(client):
    try:
        return client.get_products()
    except requests.exceptions.ConnectionError:
        print("Error in market_info. Connection refused by the server..")
        print("Short sleep initiated..")
        time.sleep(5)
        return None
    except ValueError:
        print("Error in market_info. Value error..")
        return None
    except:
        print("Error in market_info. Error type unknown..")
        return None
def coin_init(client):
    baseAsset=[]
    symbol=[]
    close=[]
    coin_name=[]
    coin_price=[]
    coin_symbol=[]
    dict=market_info(client)
    if dict is not None:
        list=dict['data']
    else:
        print "warning, binance initialization error..."
        return None
    for i in range(len(list)):
        for key, value in list[i].items():
            if key == 'baseAsset': baseAsset.append(str(value))
            if key == 'symbol': symbol.append(str(value))
            if key == 'close': close.append(float(value))
    for i in range(len(baseAsset)):
        if baseAsset[i]+'BTC' == symbol[i]:
            coin_name.append(baseAsset[i])
            coin_price.append(close[i])
            coin_symbol.append(symbol[i])

    objs = [coin.Coin(coin_name[i],coin_symbol[i],[coin_price[i],coin_price[i]], client) for i in range(len(coin_name))]
    print "object initiated, now update price..."
    while len(objs[0].price)<120:
        baseAsset = []
        symbol = []
        close = []
        coin_name = []
        coin_price = []
        coin_symbol = []
        dict = market_info(client)
        if dict is not None:
            list = dict['data']
        else:
            continue
        for i in range(len(list)):
            for key, value in list[i].items():
                if key == 'baseAsset': baseAsset.append(str(value))
                if key == 'symbol': symbol.append(str(value))
                if key == 'close': close.append(float(value))
            for i in range(len(baseAsset)):
                if baseAsset[i] + 'BTC' == symbol[i]:
                    coin_name.append(baseAsset[i])
                    coin_price.append(close[i])
                    coin_symbol.append(symbol[i])
        for i in range(len(objs)):
            for j in range(len(coin_symbol)):
                if objs[i].symbol==coin_symbol[j]:
                    objs[i].price.append(coin_price[j])
                    break
        sleep(0.05)
    print "initialization finished..."
    return objs
def update(objs,client):
    baseAsset = []
    symbol = []
    close = []
    coin_name = []
    coin_price = []
    coin_symbol = []
    dict = market_info(client)
    if dict is not None:
        list = dict['data']
    else:
        return None
    for i in range(len(list)):
        for key, value in list[i].items():
            if key == 'baseAsset': baseAsset.append(str(value))
            if key == 'symbol': symbol.append(str(value))
            if key == 'close': close.append(float(value))
        for i in range(len(baseAsset)):
            if baseAsset[i] + 'BTC' == symbol[i]:
                coin_name.append(baseAsset[i])
                coin_price.append(close[i])
                coin_symbol.append(symbol[i])
    for i in range(len(objs)):
        for j in range(len(coin_symbol)):
            if objs[i].symbol == coin_symbol[j]:
                objs[i].price.append(coin_price[j])
                objs[i].price.pop(0)
                break
    return objs
def log(coin,client):
    t_end = time.time() + 60*2
    print "rich niddle detected, logging process initiated..."
    print "trading pair:"
    print coin.name
    while time.time() < t_end:
        with open("test.txt", "a") as myfile:
            myfile.write(str(coin.get_book()))
            myfile.write('\n')
            myfile.write(str(coin.market_price()))
            myfile.write('\n')





