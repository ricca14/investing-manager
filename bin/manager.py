import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()

import requests_cache
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'


msft = yf.Ticker("ADSK", session=session)
a = msft.info
# get stock info

print('=> {}\n'.format(a ))
