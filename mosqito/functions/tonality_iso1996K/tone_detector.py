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
    - data: fichero.csv con los Lp promedio de las banda de tercio de octava.

    Outputs
    -------
    - prominent_tone: array con pares fc:Lp_promedio donde se detectan tonos prominentes.
"""

#-- Obtener Lp promedio para las bandas de tercio de octava
#-- del fichero.csv

#-- 1º --> Objetivo: leer e imprimmir el contenido del fichero.csv
#-- 2º --> Objetivo: obtener una lista con los arrays de las filas
with open('data.csv', 'r') as csvfile:
    data = list(csv.reader(csvfile, delimiter=","))

#print(data)
frec_centrales = data[0][1:32]
#print(frec_centrales)
Lp_promedio = data[1][1:32]
#print(Lp_promedio)

#-- 3º --> Objetivo: Crear un diccionario {'frecuencia central':'Lp promedio banda 1/3 oct'}
dict_oct3_levels = dict(zip(frec_centrales, Lp_promedio))
print(dict_oct3_levels)

#-- Con todo esto quiero crear una funcion a la que se le pase como entrada el archivo.csv
#-- y como salida devuelva un diccionario con el par {'frecuencia central':'Lp promedio banda 1/3 oct'}