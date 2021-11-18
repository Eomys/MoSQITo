# -*- coding: utf-8 -*-
"""
    Autor: Cristina Taboada (TinaTabo)
    Fecha inicio: 17/11/2021
    Fecha última modificación: 17/11/2021
    Descripción: Función para detectar tonos prominentes a partir de un archivo
                 .csv de datos (niveles de presión sonora promediados para cada
                 tercio de octava).
"""

#-- Librerias
import numpy as np
import csv

"""
    Parameters
    ----------
    - file: fichero.csv con los Lp promedio de las banda de tercio de octava.

    Outputs
    -------
    - prominent_tones: diccionario con pares {fc:Lp_promedio} donde se detectan tonos prominentes.
"""

#-- Obtener Lp promedio para las bandas de tercio de octava
#-- del fichero.csv

#-- 1º --> Objetivo: leer e imprimmir el contenido del fichero.csv
#-- 2º --> Objetivo: obtener una lista con los arrays de las filas
#-- 3º --> Objetivo: Crear un diccionario {'frecuencia central':'Lp promedio banda 1/3 oct'}
#.. 4º --> Objetivo: Crear función para crear el diccionario con los datos del archivo.csv

#-- Fichero a leer --> Mas adelante cambiar para introducir nombre del fichero por linea de comandos.
file = 'data.csv'


def create_data_dict(file):
    #-- Leer el archivo y extraer los datos
    with open('data.csv', 'r') as csvfile:
        data = list(csv.reader(csvfile, delimiter=","))

    #-- Crear el diccionario con lo datos extraidos.
    frec_centrales = data[0][1:32]
    Lp_promedio = data[1][1:32]
    oct3_levels = dict(zip(frec_centrales, Lp_promedio))

    return oct3_levels

dict_oct3_levels = create_data_dict(file)
print(dict_oct3_levels)