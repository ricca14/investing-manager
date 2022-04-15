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
sql = DBIntelligent("intelligent_investor")
# from .source import get_market

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

import time
start_time = time.time()

def insert_market(sigla):
    q = "SELECT * FROM mercati WHERE sigla = '%s';" % sigla
    r = sql.select(q)
    if not r:
        success = sql.insert('mercati', ['sigla'], [sigla])
        print('\n{} record inserito\n'.format(success))

def insert_stock(sigla):
    q = "SELECT * FROM mercati WHERE sigla = '%s';" % sigla
    r = sql.select(q)
    if not r:
        success = sql.insert('mercati', ['sigla'], [sigla])
        print('\n{} record inserito\n'.format(success))


for market in ticker:
    insert_market(market)
    print('UPDATE %s' % market)
    tickers = ticker[market]


print("\n--- %s secondi dall'inizio ---" % (time.time() - start_time))
