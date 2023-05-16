from typing import Any

class DBService():

    def cast_value(value):
        if value == 'True':
            valore = True
        elif value == 'False':
            valore = False
        else:
            try:
                valore = int(value)
            except:
                valore = value

        return valore