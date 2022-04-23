import time
import traceback
from sql.config import DBIntelligent
sql = DBIntelligent()
from source.source import StockSource, MarketSource

import yahoo_fin.stock_info as si
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()

import requests_cache
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'

ticker = {}
ticker['DWJ'] = si.tickers_dow()
# # ticker['FTSE100'] = si.tickers_ftse100()
# # ticker['FTSE250'] = si.tickers_ftse250()
# # ticker['IBVSPA'] = si.tickers_ibovespa()
ticker['NSDQ'] = si.tickers_nasdaq()
# # ticker['NFT50'] = si.tickers_nifty50()
# # ticker['NFTB'] = si.tickers_niftybank()
# # ticker['OTH'] = si.tickers_other()
ticker['SP500'] = si.tickers_sp500()

# ticker = select_all_ticker()
print('TICKER TOTAL: {}'.format(ticker))

key_list = ['bookValue','targetLowPrice', 'targetMedianPrice', 'targetMeanPrice', 'targetHighPrice','trailingEps', 'forwardEps','dividendRate','currentPrice','returnOnEquity','pegRatio','revenueGrowth', 'revenueQuarterlyGrowth', 'earningsGrowth', 'earningsQuarterlyGrowth','trailingPE', 'forwardPE']

import time
start_time = time.time()

def insert_market(sigla):
    r = MarketSource.get_market(sigla)
    if not r:
        success = MarketSource.insert_market(sigla)
        print('{} record inserito\n'.format(success))

def insert_stock(ticker, name, market):
    r = MarketSource.get_market(market)
    if not r:
        print('\nERRORE: {} non trovato\n'.format(market))

    try:
        market = r[0];
    except Exception as ex:
        print(ex)

    stock = StockSource.get_stock(ticker)
    try:
        stock = stock[0]
    except Exception as ex:
        print(ex)

    if not stock:
        success = StockSource.insert_stock(ticker, name, market['id'])
        print('\n{} record inserito\n'.format(success))
    elif 'nome' not in stock or not stock['nome']:
        print(ticker, name, stock)
        success = StockSource.update_stock(name, stock['id'])
        print('\n{} record inserito\n'.format(success))
    else:
        print('\nNO {} -- -- %s secondi'.format((time.time() - start_time)))

    print('\n{} -- -- %s secondi\n'.format((time.time() - start_time)))

def get_stock_update_list(st):
    element = []

    stock_info = yf.Ticker(st)
    info = stock_info.info

    # print('\n info: {}'.format(info));

    stock_name = info.get('shortName', '')
    try:
        stock_name = stock_name.replace("'", "\\'")
    except:
        stock_name = ''
    element.append({'nome':stock_name})

    # Il rendimento dei dividendi: dividendRate
    # Il rapporto corso/valore contabile: bookValue
    # EPS: trailingEps, forwardEps
    # Valutazioni analisti: targetLowPrice, targetMeanPrice, targetHighPrice
    # Il rendimento del capitale proprio : returnOnEquity
    # La crescita dell’utile: pegRatio
    for key in key_list:
        value = info.get(key, '') if key in info and info[key] else ''
        element.append({key.lower():value})

    return element

def select_all_ticker():
    tickers_dict = StockSource.get_all_tickers()
    t_list = []
    for el in tickers_dict:
        t_list.append(el['sigla'])
    # return
    return t_list


# CON MARKET
for market in ticker:
    insert_market(market)
    stock_tickers = ticker[market]
    for st in stock_tickers:
        try:
            stock = StockSource.get_stock(st)
            if not stock:
                insert_stock(stock, ST, market)

            stock = StockSource.get_stock(st)
            if stock:
                stock = stock[0]
                update_list = get_stock_update_list(st)
                trailingEps = ''
                for u in update_list:
                    trailingEps = u['trailingeps'] if 'trailingeps' in u else trailingEps

                if stock['trailingeps'] != trailingEps:
                    print(st, update_list, stock)
                    success = StockSource.update_stock(update_list, stock['id'])
                else:
                    print('DATI NON MODIFICATI')
            else:
                print('\n\n INSERIRE MANUALMENTE: {} \n\n'.format(st))
        except Exception as ex:
            print(ex)
            traceback.print_exception()

print("\n--- %s secondi dall'inizio ---" % (time.time() - start_time))
