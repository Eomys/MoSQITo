# -*- coding: utf-8 -*-
"""
    Autor: Cristina Taboada (TinaTabo)
    Fecha inicio: 17/11/2021
    Fecha última modificación: 17/11/2021
    Descripción: Función para detectar tonos prominentes a partir de un archivo
                 .csv de datos (niveles de presión sonora promediados para cada
                 tercio de octava).
"""

#-- Importar librerias
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

#-- Primera prueba --> Objetivo: leer e imprimmir el contenido del fichero.csv
with open('data.csv') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    for row in filereader:
        print(row)