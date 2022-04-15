# import investpy
# df = investpy.get_stock_historical_data(stock='AAPL', country='United States', from_date='01/01/2010', to_date='01/01/2020')
# print(df)

import yahoo_fin.stock_info as si
from yahoo_fin import options
import pandas as pd

from collections import OrderedDict
import math
import time
import sql.config as sql
# from .source import get_market

ticker = {}
ticker['DWJ'] = si.tickers_dow()
# ticker['FTSE100'] = si.tickers_ftse100()
# ticker['FTSE250'] = si.tickers_ftse250()
# ticker['IBVSPA'] = si.tickers_ibovespa()
# ticker['NASDQ'] = si.tickers_nasdaq()
# ticker['NFT50'] = si.tickers_nifty50()
# ticker['NFTB'] = si.tickers_niftybank()
# ticker['OTH'] = si.tickers_other()
# ticker['SP500'] = si.tickers_sp500()

import time
start_time = time.time()

def get_market(sigla):
    q = "SELECT * FROM mercati WHERE sigla = '%s';" % sigla
    r = sql.run_query(q)


for market in ticker:
    print('UPDATE %s' % market)
    tickers = ticker[market]
    r = get_market(market)


    print("\n--- %s secondi dall'inizio ---" % (time.time() - start_time))
