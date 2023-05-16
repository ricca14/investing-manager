from sql.config import DBIntelligent
sql = DBIntelligent()


class ParametriSource():

    def get_parametri(tipo):
        q = "SELECT chiave, valore FROM parametri WHERE tipo = '{}';".format(tipo)
        return sql.select(q)

    