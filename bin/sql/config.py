import mysql.connector
from config.credentials import *
# mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="reventon7", database="intelligent_investor")
mydb = None
cursor = None
db = ''

log_query = False
log_response = False

class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

class DBIntelligent():

    def __init__(self):
        self.mydb = mysql.connector.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DB)
        # self.cursor = self.mydb.cursor(cursor_class=MySQLCursorDict)
        self.cursor = self.mydb.cursor(dictionary=True)

    def log_query(self, q, log_rage=False):
        # Metodo che logga cose in automatico
        if log_query or log_rage:
            print("\nRUN: {}\n".format(q))

    def log_response(self, res, log_rage=False):
        # Metodo che logga cose in automatico
        if log_response or log_rage:
            if type(res) == int:
                print("RESPONSE: {}".format(res))
            else:
                print("RESPONSE: ")
                for x in res:
                    print('{}\n'.format(x))


    def select(self, q, log_rage=False):
        """
        Metodo che passato una query la esegue
        """
        self.log_query(q, log_rage=log_rage)
        self.cursor.execute(q)
        response = []
        for x in self.cursor:
            response.append(x)

        self.log_response(response, log_rage=log_rage)
        return response


    def insert(self, tab, campi, val, log_rage=False):
        fields = self.create_field_query(campi) if type(campi) == list else campi
        items = ''
        for i in val:
            items += ', ' if items else items
            items += '%s '

        q = "INSERT INTO {tabella} ({campi}) VALUES ({items})".format(
            tabella=tab,
            campi=fields,
            items=items
        )
        self.log_query(q, log_rage=log_rage)
        self.cursor.execute(q, val)
        self.mydb.commit()

        response = self.cursor.rowcount
        self.log_response(response, log_rage=log_rage)
        return self.cursor.rowcount

    def create_field_query(self, fields):
        """
            Metodo che genera la lista di campi per la INSERT
        """
        q = ""
        for f in fields:
            q += ', ' if q else q
            q += f

        return q

    def update(self, table, update_list, where_list, log_rage=False):
        """
            table: str, tabella da update_stock
            update: list, ['campo': "nuovo valore"]
            where: list, ['campo': "campo match"]
        """

        where_string = ''
        for where in where_list:
            for w in where:
                if where_string:
                    where_string += ','
                where_string += "{} = '{}'".format(w, where[w])


        update_string = ''
        for update in update_list:
            for u in update:
                if update_string:
                    update_string += ','
                update_string += "{} = '{}'".format(u, update[u])

        q = "UPDATE {table} SET {update} WHERE {where}".format(table=table, update=update_string, where=where_string)
        self.log_query(q, log_rage=log_rage)
        self.cursor.execute(q)
        self.mydb.commit()

        response = self.cursor.rowcount
        self.log_response(response, log_rage=log_rage)
        return self.cursor.rowcount
