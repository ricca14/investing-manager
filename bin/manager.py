import yfinance as yf
import yfinance as yf

msft = yf.Ticker("MSFT")

# get stock info
print('=> {}\n'.format(msft.info))

# get historical market data
hist = msft.history(period="max")
print('=> {}\n'.format(hist))
# show actions (dividends, splits)
print('=> {}\n'.format(msft.actions))

# show dividends
print('=> {}\n'.format(msft.dividends))

# show splits
print('=> {}\n'.format(msft.splits))

# show financials
print('=> {}\n'.format(msft.financials))
print('=> {}\n'.format(msft.quarterly_financials))

# show major holders
print('=> {}\n'.format(msft.major_holders))

# show institutional holders
print('=> {}\n'.format(msft.institutional_holders))

# show balance sheet
print('=> {}\n'.format(msft.balance_sheet))
print('=> {}\n'.format(msft.quarterly_balance_sheet))

# show cashflow
print('=> {}\n'.format(msft.cashflow))
print('=> {}\n'.format(msft.quarterly_cashflow))

# show earnings
print('=> {}\n'.format(msft.earnings))
print('=> {}\n'.format(msft.quarterly_earnings))

# show sustainability
print('=> {}\n'.format(msft.sustainability))

# show analysts recommendations
print('=> {}\n'.format(msft.recommendations))

# show next event (earnings, etc)
print('=> {}\n'.format(msft.calendar))

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
print('=> {}\n'.format(msft.isin))

# show options expirations
print('=> {}\n'.format(msft.options))

# show news
print('=> {}\n'.format(msft.news))

# get option chain for specific expiration
opt = msft.option_chain('2022-04-22')
# data available via: opt.calls, opt.puts

print('+++++++++++++++++++++++++++++++++')
print(opt)
print('+++++++++++++++++++++++++++++++++')


# from pandas_datareader import data as pdr
#
# yf.pdr_override() # <== that's all it takes :-)
#
# print('\n\n')
# # download dataframe
# data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
# print('+++++++++++++++++++++++++++++++++')
# print(data)
# print('+++++++++++++++++++++++++++++++++')
