from sql.config import DBIntelligent
sql = DBIntelligent()

class StockSource():

    def get_stock(sigla):
        q = "SELECT * FROM stock WHERE sigla = '%s';" % sigla
        return sql.select(q)

    def insert_stock(ticker, name, id_market):
        success = sql.insert('stock', ['sigla', 'nome', 'mercato'], [ticker, name, id_market])
        return success

    def update_stock(campi, id_stock):
        success = sql.update('stock', campi, [{'id': id_stock}], log_rage=True)
        return success


class MarketSource():

    def get_market(sigla):
        q = "SELECT * FROM mercati WHERE sigla = '%s';" % sigla
        return sql.select(q)

    def insert_market(sigla):
        success = sql.insert('mercati', ['sigla'], [sigla])
        return success
