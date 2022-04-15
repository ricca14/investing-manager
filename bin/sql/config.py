import mysql.connector
# mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="reventon7", database="intelligent_investor")
mydb = None
cursor = None
db = ''

log_query = True
log_response = True

class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None

class DBIntelligent():

    def __init__(self, name):
        self.db = name
        self.mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="reventon7", database=self.db)
        # self.cursor = self.mydb.cursor(cursor_class=MySQLCursorDict)
        self.cursor = self.mydb.cursor(dictionary=True)

    def log_query(self, q, log_rage=False):
        # Metodo che logga cose in automatico
        if log_query or log_rage:
            print("\nRUN: {}\n".format(q))

    def log_response(self, res, log_rage=False):
        # Metodo che logga cose in automatico
        if log_response or log_rage:
            print("\nRESPONSE: ")
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
            items += '%s '

        q = "INSERT INTO {tabella} ({campi}) VALUES ({items})".format(
            tabella=tab,
            campi=fields,
            items=items
        )
        self.log_query(q)
        self.cursor.execute(q, val)
        self.mydb.commit()

        response = self.cursor.rowcount
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
