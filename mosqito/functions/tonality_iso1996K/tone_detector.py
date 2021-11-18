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
from types import ClassMethodDescriptorType
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
#-- 4º --> Objetivo: Crear función para crear el diccionario con los datos del archivo.csv
#-- OBJETIVOS 3º Y 4º NO SIRVEN.
#-- 5º --> Objetivo: Con las listas de las frecuencias centrales y los Lp promedio crear una funcion para
#--                  obtener los tonos prominentes.

#-- Fichero a leer --> Mas adelante cambiar para introducir nombre del fichero por linea de comandos.
file = 'data.csv'


def create_data_dict(file):
    #-- Leer el archivo y extraer los datos
    with open('data.csv', 'r') as csvfile:
        data = list(csv.reader(csvfile, delimiter=","))

    #-- Obtener las listas de las frec.centrales y los Lp_promedio.
    fc = data[0][1:32]
    Lp_mean = data[1][1:32]

    return fc, Lp_mean

frec_centrales, Lp_promedio = create_data_dict(file)

#-- Longitud de las listas, las 2 tienen la misma long.
Lp_len = len(Lp_promedio)
print(Lp_len)

#-- Creadas las listas. Itinerar lista Lp_promedio
print("------------------------------------------")

for x in range (0, Lp_len):
    if x > 0 and x < 30:
        print("------------------")
        print(frec_centrales[x-1], ":", Lp_promedio[x-1])
        Lp_anterior = Lp_promedio[x-1]
        print(frec_centrales[x], ":", Lp_promedio[x])
        Lp = Lp_promedio[x]
        print(frec_centrales[x+1], ":", Lp_promedio[x+1])
        Lp_posterior = Lp_promedio[x+1]
        print("------------------")

        #-- Comparar niveles para determinar si es un tono prominente.
        if x > 0 and x < 9:
            print("BAJA FRECUENCIA")
        elif x > 8 and x < 14:
            print("MEDIA FRECUENCIA")
        elif x > 13 and x < 30:
            print("ALTA FRECUENCIA")
print("------------------------------------------")