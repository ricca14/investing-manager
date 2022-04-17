# import investpy
# df = investpy.get_stock_historical_data(stock='AAPL', country='United States', from_date='01/01/2010', to_date='01/01/2020')
# print(df)

import yahoo_fin.stock_info as si
from yahoo_fin import options
import pandas as pd

from collections import OrderedDict
import math
import time
from sql.config import DBIntelligent
sql = DBIntelligent()
from source.source import StockSource, MarketSource

ticker = {}
ticker['DWJ'] = si.tickers_dow()
ticker['FTSE100'] = si.tickers_ftse100()
ticker['FTSE250'] = si.tickers_ftse250()
ticker['IBVSPA'] = si.tickers_ibovespa()
ticker['NSDQ'] = si.tickers_nasdaq()
ticker['NFT50'] = si.tickers_nifty50()
ticker['NFTB'] = si.tickers_niftybank()
ticker['OTH'] = si.tickers_other()
ticker['SP500'] = si.tickers_sp500()

print('TICKER TOTAL: {}'.format(ticker))

import time
start_time = time.time()

def insert_market(sigla):
    r = MarketSource.get_market(sigla)
    if not r:
        success = MarketSource.insert_market(sigla)
        print('{} record inserito\n'.format(success))

def insert_stock(ticker, market):
    r = MarketSource.get_market(market)
    if not r:
        print('\nERRORE: {} non trovato@\n'.format(market))

    try:
        market = r[0];
    except Exception as ex:
        print(ex)

    stock = StockSource.get_stock(ticker)
    if not stock:
        print('\n{} -- -- %s secondi'.format((time.time() - start_time)))
        success = StockSource.insert_stock(ticker, market['id'])
        print('\n{} record inserito\n'.format(success))
    else:
        print('\nNO {} -- -- %s secondi'.format((time.time() - start_time)))

for market in ticker:
    insert_market(market)
    print('UPDATE %s' % market)
    stock_ticker = ticker[market]
    for stock in stock_ticker:
        print('INSERT: {}'.format(stock))
        insert_stock(stock, market)
    #
    # print("\n--- %s secondi dall'inizio ---" % (time.time() - start_time))


print("\n--- %s secondi dall'inizio ---" % (time.time() - start_time))
