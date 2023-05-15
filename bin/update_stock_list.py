import time
import traceback
from sql.config import DBIntelligent
sql = DBIntelligent()
from source.source import StockSource, MarketSource

import yfinance as yf
yf.pdr_override()

import requests_cache
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'

# #######################
search_new_ticker = False
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

def insert_market(sigla):
    r = MarketSource.get_market(sigla)
    if not r:
        success = MarketSource.insert_market(sigla)
        print('{} record inserito\n'.format(success))

def insert_stock(ticker, name, market):
    print(ticker, name, market)
    print('----------------------')
    try:
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
    
    except Exception as ex:
        traceback.print_exception()
        print(ex)



def get_stock_update_list(st_list):
    # Faccio la GET della lista di Ticker
    stock_info = yf.Tickers(st_list)

    list_element = []
    list_tck = list(filter(None, st_list.split(' ')))
    # print('stock_info {}'.format(stock_info))
    for tck in list_tck:
        try:
            element = []        
            info = stock_info.tickers[tck].info
            stock_name = info.get('shortName', '')
            try:
                stock_name = stock_name.replace("'", "\\'")
            except:
                stock_name = ''
            element.append({'nome':stock_name})
            element.append({'sigla':tck})
            
            # Il rendimento dei dividendi: dividendRate
            # Il rapporto corso/valore contabile: bookValue
            # EPS: trailingEps, forwardEps
            # Valutazioni analisti: targetLowPrice, targetMeanPrice, targetHighPrice
            # Il rendimento del capitale proprio : returnOnEquity
            # La crescita dell’utile: pegRatio
            for key in key_list:
                value = info.get(key, '') if key in info and info[key] else ''
                element.append({key.lower():value})

            list_element.append(element)
        except:
            print('IMPOSSIBILE RECUPERARE: {}'.format(tck))

    # print('\n list_element: {}'.format(list_element))
    return list_element



def select_all_ticker():
    tickers_dict = StockSource.get_all_tickers()
    t_list = []
    for el in tickers_dict:
        t_list.append(el['sigla'])
    # return
    return t_list


def get_ticket_query(stock_tickers):
    match_stock_id = {}
    trailing_eps_stock = {}
    list_ticker_getter = []
    list_ticker_getter_str = ''
    i = 0
    for st in stock_tickers:
        if i == 5:
            i = 0
            list_ticker_getter.append(list_ticker_getter_str)
            list_ticker_getter_str = ''

        try:
            # print('CERCO: {}'.format(st))
            stock = StockSource.get_stock(st)
            if not stock:
                insert_stock(st, st, market)
                stock = StockSource.get_stock(st)[0]
            else:
                stock = stock[0]

            match_stock_id[st] = stock['id']
            trailing_eps_stock[st] = stock['trailingeps']
            list_ticker_getter_str += ' {}'.format(st)
            i += 1
        except Exception as ex:
            print(ex)
            traceback.print_exception()

    if i < 5:
        list_ticker_getter.append(list_ticker_getter_str)
    
    return list_ticker_getter, match_stock_id, trailing_eps_stock



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
        stock_tickers = StockSource.get_stock_ticker()

    main(stock_tickers)

def main(stock_tickers):
        list_ticker_getter, match_stock_id, trailing_eps_stock = get_ticket_query(stock_tickers)
        for list_tck in list_ticker_getter:
            start_time_list = time.time()
            list_tickers = get_stock_update_list(list_tck)
            try:
                for update_list in list_tickers:
                    # print('update_list: {}'.format(update_list))
                    sigla = [upd['sigla'] for upd in update_list if 'sigla' in upd][0]
                    trailingeps_now = [upd['trailingeps'] for upd in update_list if 'trailingeps' in upd][0]
                    trailingEps = trailing_eps_stock.get(sigla, 0)

                    print('VS: {} = {}'.format(trailingeps_now, trailingEps))
                    
                    if trailingeps_now != trailingEps:
                        success = StockSource.update_stock(update_list, match_stock_id[sigla])
                        print('{}: AGGIORNATO'.format(sigla))
                    else:
                        print('{}: DATI NON MODIFICATI'.format(sigla))
            
                
                print( "\n--- {} secondi per la lista ---\n".format(time.time() - start_time_list))
            except Exception as ex:
                print(ex)
                traceback.print_exception()


# ##########################
# TUTTO INIZIA DALLA FINE
# ##########################

start_ASCII()
handle()
print("\n--- {} secondi dall'inizio ---".format(time.time() - start_time))






