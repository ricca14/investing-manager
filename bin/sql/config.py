import mysql.connector
mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="reventon7", database="intelligent_investor")
cursor = mydb.cursor()

log_query = True
log_response = True

print('{} === {}'.format(mydb, cursor))
def run_query(q, log_rage=False):
    if log_query or log_rage:
        print("\nRUN: {}\n".format(q))

    cursor.execute(q)
    if log_response or log_rage:
        print("\nRESPONSE: ")
        for x in cursor:
            print(x)



    return cursor
