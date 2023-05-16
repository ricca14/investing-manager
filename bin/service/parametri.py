from typing import Any
from source.parametri import ParametriSource


class ParametriService():

    def get_parametri(tipo):
        list = ParametriSource.get_parametri(tipo)
        return_dict = {}
        for el in list:


            return_dict[el['chiave']] = valore

        return return_dict

