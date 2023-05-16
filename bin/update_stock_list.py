from datetime import datetime, date
import traceback
from sql.config import DBIntelligent
sql = DBIntelligent()

from service.stock import StockService
from service.parametri import ParametriService

import yfinance as yf
# yf.pdr_override()

import requests_cache
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'

# #######################
skip_today = True
search_new_ticker = False
n_ticker = 10
if not search_new_ticker:
    import yahoo_fin.stock_info as si
    ticker = {}
    ticker['DWJ'] = si.tickers_dow()
    ticker['NSDQ'] = si.tickers_nasdaq()
    ticker['SP500'] = si.tickers_sp500()

# # ticker['FTSE100'] = si.tickers_ftse100()
# # ticker['FTSE250'] = si.tickers_ftse250()
# # ticker['IBVSPA'] = si.tickers_ibovespa()
# # ticker['NFT50'] = si.tickers_nifty50()
# # ticker['NFTB'] = si.tickers_niftybank()
# # ticker['OTH'] = si.tickers_other()

# ticker = select_all_ticker()
# print('TICKER TOTAL: {}'.format(ticker))

key_list = ['bookValue','targetLowPrice', 'targetMedianPrice', 'targetMeanPrice', 'targetHighPrice','trailingEps', 'forwardEps','dividendRate','currentPrice','returnOnEquity','pegRatio','revenueGrowth', 'revenueQuarterlyGrowth', 'earningsGrowth', 'earningsQuarterlyGrowth','trailingPE', 'forwardPE']

import time
start_time = time.time()

# ##########################
# METODI DI RACCORDO
# ##########################

def get_ticket_query(stock_tickers):
    match_stock_id = {}
    trailing_eps_stock = {}
    update_today = {}
    list_ticker_getter = []
    list_ticker_getter_str = ''
    i = 0
    for st in stock_tickers:
        if i == n_ticker:
            i = 0
            list_ticker_getter.append(list_ticker_getter_str)
            list_ticker_getter_str = ''

        try:
            # print('CERCO: {}'.format(st))
            stock = StockService.get_stock(st)
            if not stock:
                StockService.insert_stock(st, st, market)
                stock = StockService.get_stock(st)[0]
            else:
                stock = stock[0]

            match_stock_id[st] = stock['id']
            trailing_eps_stock[st] = stock['trailingeps']
            update_today[st] = its_update_today(stock['upd_datetime'])
            list_ticker_getter_str += ' {}'.format(st)
            i += 1
        except Exception as ex:
            print(ex)
            traceback.print_exception()

    if i < 5:
        list_ticker_getter.append(list_ticker_getter_str)
    
    return list_ticker_getter, match_stock_id, trailing_eps_stock, update_today


def its_update_today(upd_datetime):
    today = datetime.now()
    return (abs((today - upd_datetime).days) == 0)



# ##########################
# METODI PRINCIPALI
# ##########################

def start_ASCII():
    print("""
            _.---.__
          .'        `-.
         /      .--.   |
         \/  / /    |_/
          `\/|/    _(_)
      ___  /|_.--'    `.   .
       \  `--' .---.     \ /|
        )   `       \     //|
        | __    __   |   '/||
        |/  \  /  \      / ||
        ||  |  |   \     \  |
        \|  |  |   /        |
       __\\@/  |@ | ___ \--'
      (     /' `--'  __)|
     __>   (  .  .--' &"\
    /   `--|_/--'     &  |
    |                 #. |
    |                 q# |
     \              ,ad#'
      `.________.ad####'
        `#####""""""''
         `&#"
          &# 
          "&
          """)

def handle():   
    stock_tickers = []
    if search_new_ticker:
        # CON MARKET
        for market in ticker:
            insert_market(market)
            stock_tickers = stock_tickers + ticker[market]
    else:
        stock_tickers = StockSource.get_stock_ticker_to_update(date.today())

    main(stock_tickers)

def main(stock_tickers):
    list_ticker_getter, match_stock_id, trailing_eps_stock, update_today = get_ticket_query(stock_tickers)
    c = 0
    for list_tck in list_ticker_getter:
        start_time_list = time.time()
        list_tickers = StockService.get_stock_update_list(list_tck)

        # Se non riesce a fare la get dei ticker allinea i contatori
        if len(list_tickers) != n_ticker:
            c += n_ticker - len(list_tickers)

        try:
            for update_list in list_tickers:
                # print('update_list: {}'.format(update_list))
                sigla = [upd['sigla'] for upd in update_list if 'sigla' in upd][0]
                if not update_today[sigla] and skip_today:
                    trailingeps_now = [upd['trailingeps'] for upd in update_list if 'trailingeps' in upd][0]
                    trailingEps = trailing_eps_stock.get(sigla, 0)

                    # print('VS: {} = {}'.format(trailingeps_now, trailingEps))
                    if trailingeps_now and trailingeps_now != trailingEps:
                        success = StockSource.update_stock(update_list, match_stock_id[sigla])
                        print('{}: AGGIORNATO'.format(sigla))
                    else:
                        print('{}: DATI NON MODIFICATI'.format(sigla))
                else:
                    print('{}: AGGIORNATO OGGI'.format(sigla))

                c += 1 

            sec = (time.time()-start_time_list)
            perc = (c*100)/len(stock_tickers)
            print("\n--- {} secondi | lista {}/{} ({}%) ---\n".format(sec, c, len(stock_tickers), round(perc, 2)))
                    
        except Exception as ex:
            print(ex)
            traceback.print_exception()


# ##########################
# TUTTO INIZIA DALLA FINE
# ##########################

start_ASCII()
handle()
print("\n--- {} secondi dall'inizio ---".format(time.time() - start_time))






