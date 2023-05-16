# import yfinance as yf
# tickers = yf.Tickers('MSFT AAPL GOOG')
# print(tickers.tickers['MSFT'].info)


# tickers = yf.Ticker('MSFT')
# print(tickers.info)
from service.parametri import ParametriService
a = ParametriService.get_parametri('update_stock')
print(a)