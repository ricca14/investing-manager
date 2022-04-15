from sql.config import DBIntelligent
sql = DBIntelligent("intelligent_investor")


class StockSource():

    def get_stock(sigla):
        q = "SELECT * FROM stock WHERE sigla = '%s';" % sigla
        return sql.select(q)

    def insert_stock(ticker, id_market):
        success = sql.insert('stock', ['sigla', 'mercato'], [ticker, id_market])
        return success


class MarketSource():

    def get_market(sigla):
        q = "SELECT * FROM mercati WHERE sigla = '%s';" % sigla
        return sql.select(q)

    def insert_market(sigla):
        success = sql.insert('mercati', ['sigla'], [sigla])
        return success
