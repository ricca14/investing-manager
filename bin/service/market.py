from source.stock import MarketSource

class MarketService():

    def insert_market(sigla):
        r = MarketSource.get_market(sigla)
        if not r:
            success = MarketSource.insert_market(sigla)
            print('{} record inserito\n'.format(success))
