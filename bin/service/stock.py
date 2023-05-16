from typing import Any
import yfinance as yf
from source.stock import StockSource, MarketSource
from source.parametri import ParametriSource

class StockService():

    def get_stock(ticker):
        return StockSource.get_stock(ticker)

    def select_all_ticker():
        tickers_dict = StockSource.get_all_tickers()
        t_list = []
        for el in tickers_dict:
            t_list.append(el['sigla'])
        return t_list

    def insert_stock(ticker, name, market):
        print(ticker, name, market)
        print('----------------------')
        try:
            r = MarketSource.get_market(market)
            if not r:
                print('\nERRORE: {} non trovato\n'.format(market))

            try:
                market = r[0]
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
                element.append({'nome': stock_name})
                element.append({'sigla': tck})

                # Il rendimento dei dividendi: dividendRate
                # Il rapporto corso/valore contabile: bookValue
                # EPS: trailingEps, forwardEps
                # Valutazioni analisti: targetLowPrice, targetMeanPrice, targetHighPrice
                # Il rendimento del capitale proprio : returnOnEquity
                # La crescita dell’utile: pegRatio
                for key in key_list:
                    value = info.get(key, '') if key in info and info[key] else ''
                    element.append({key.lower(): value})

                list_element.append(element)
            except:
                print('IMPOSSIBILE RECUPERARE: {}'.format(tck))

        # print('\n list_element: {}'.format(list_element))
        return list_element
