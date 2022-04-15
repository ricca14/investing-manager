import sql.config as sql
def get_market(sigla):
    q = "SELECT * FROM mercati WHERE sigla = '%s';" % sigla
    r = sql.run_query(q)
