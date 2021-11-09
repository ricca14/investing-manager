# import investpy
# df = investpy.get_stock_historical_data(stock='AAPL', country='United States', from_date='01/01/2010', to_date='01/01/2020')
# print(df)

import yahoo_fin.stock_info as si
from yahoo_fin import options
import pandas as pd

from collections import OrderedDict
import math
import time


# tickers_dow = si.tickers_dow()
# tickers_ftse100 = si.tickers_ftse100()
# tickers_ftse250 = si.tickers_ftse250()
# tickers_ibovespa = si.tickers_ibovespa()
#tickers_nasdaq = si.tickers_nasdaq()
# tickers_nifty50 = si.tickers_nifty50()
# tickers_niftybank = si.tickers_niftybank()
# tickers_other = si.tickers_other()
tickers_sp500 = si.tickers_sp500()

all_ticker = tickers_sp500
all_ticker = list(dict.fromkeys(all_ticker))

all_ticker_error = []
all_ticker_data = []
all_ticker_dict = {}

i = 1
import time
start_time = time.time()

def add_ticker(ticker):
    ticker_dict = si.get_stats_valuation(ticker)

    field_ebitda = None
    field_pe = None
    field_peg = None
    field_trailing = None
    for n, field in ticker_dict[0].iteritems():
        if 'EBITDA' in field:
            field_ebitda = n
        elif 'Forward P/E' in field:
            field_forward = n
        elif 'PEG' in field:
            field_peg = n
        elif 'Trailing P/E' in field:
            field_pe = n

    next_better = bool(field_forward > field_pe)
    if next_better:
        ticker_element = {
            'TICKER': ticker,
            'EBITDA': float(0) if math.isnan(float(ticker_dict[1][field_ebitda])) else float(ticker_dict[1][field_ebitda]),
            'PE': float(999) if math.isnan(float(ticker_dict[1][field_pe])) else float(ticker_dict[1][field_pe]),
            'PEG': float(999) if math.isnan(float(ticker_dict[1][field_peg])) else float(ticker_dict[1][field_peg]),
            'PE_NEXT': next_better
        }
        all_ticker_data.append(ticker_element)
        all_ticker_dict[ticker] = ticker_element

for ticker in all_ticker:
    print('Processo {} ------> {}/{}'.format(ticker, i, len(all_ticker)))
    try:
        add_ticker(ticker)
        i = i+1
        print("--- %s secondi dall'inizio ---" % (time.time() - start_time))
    except:
        print("--- %s secondi dall'inizio ---" % (time.time() - start_time))
        print('\n\nERRORE. {}\n'.format(ticker))
        all_ticker_error.append(ticker)


for ticker in all_ticker_error:
    print('Processo {} ------> {}/{}'.format(ticker, i, len(all_ticker)))
    try:
        add_ticker(ticker)
        i = i+1
    except:
        print('\n\nERRORE. {}\n'.format(ticker))
        all_ticker_error.append(ticker)



print("\n\n--- %s seconds ---\n\n" % (time.time() - start_time))
print("--- {}/{} -- {} in errore ---\n\n".format(len(all_ticker_dict), len(all_ticker), len(all_ticker_error)))
# print('all_ticker_data: {}'.format(all_ticker_data))
# print('all_ticker_dict: {}'.format(all_ticker_dict))

sort_ebitda = OrderedDict(sorted(all_ticker_dict.items(), key=lambda x: x[1]['EBITDA'], reverse=True))


# FLOW PEG
final_result = OrderedDict(sorted(sort_ebitda.items(), key=lambda x: x[1]['PE'], reverse=False))
sort_peg = OrderedDict(sorted(final_result.items(), key=lambda x: x[1]['PEG'], reverse=False))

print('\n\n===========================================================\n')
print('================== FLOW PEG\n')
print(sort_peg)
print('\n\n ===========================================================')

# FLOW PE
sort_peg = OrderedDict(sorted(sort_ebitda.items(), key=lambda x: x[1]['PEG'], reverse=False))
final_result = OrderedDict(sorted(sort_peg.items(), key=lambda x: x[1]['PE'], reverse=False))

print('\n\n ===========================================================\n')
print('================== FLOW PE\n')
print(final_result)
print('\n\n ===========================================================')
