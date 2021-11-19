# -*- coding: utf-8 -*-
"""
    Autor: Cristina Taboada (TinaTabo)
    Fecha inicio: 17/11/2021
    Fecha última modificación: 19/11/2021
    Descripción: Función para detectar tonos prominentes a partir de un archivo
                 .csv de datos (niveles de presión sonora promediados para cada
                 tercio de octava).
"""

#-- Librerias
import csv

"""
    Parameters
    ----------
    - file: fichero.csv con los Lp promedio de las banda de tercio de octava.

    Outputs
    -------
    - prominent_tones: diccionario con pares {fc:Lp_mean} donde se detectan tonos prominentes.
"""

#-- Obtener Lp promedio para las bandas de tercio de octava
#-- del fichero.csv

#-- Fichero a leer --> Mas adelante cambiar para introducir nombre del fichero por linea de comandos.
file = input('Enter the data file name: ')


def tone_detector(file):
    #-- Leer el archivo y extraer los datos
    with open('data.csv', 'r') as csvfile:
        data = list(csv.reader(csvfile, delimiter=","))

    #-- Obtener las listas de las frec.centrales y los Lp_promedio.
    fc = data[0][1:32]
    Lp_mean = data[1][1:32]

    #-- Longitud de las listas, las 2 tienen la misma long.
    Lp_len = len(Lp_mean)
    print(Lp_len)

    #-- Lista donde se guardaran los indices correspondientes a las posiciones donde hay 
    #-- un tono prominente
    index_tone_list = []

    #-- Creadas las listas. Itinerar lista Lp_mean
    print("------------------------------------------")

    for x in range (0, Lp_len):
        if x > 0 and x < 30:
            #-- Variables a comparar
            Lp_prev = int(Lp_mean[x-1])
            Lp = int(Lp_mean[x])
            Lp_post = int(Lp_mean[x+1])

            #-- calculamos la diferencia
            Lp_diff_prev = Lp - Lp_prev
            print(Lp_diff_prev)
            Lp_diff_post = Lp - Lp_post
            print(Lp_diff_post)

            #-- Comparar niveles para determinar si es un tono prominente.
            if x > 0 and x < 9:
                print("BAJA FRECUENCIA --> diferencia 15 dB")
                if Lp_diff_prev >= 15 and Lp_diff_post >= 15:
                    #-- hay un tono en x, guardamos su valor.
                    index_tone_list.append(x)
                
            elif x > 8 and x < 14:
                print("MEDIA FRECUENCIA --> diferencia 8 dB")
                if Lp_diff_prev >= 8 and Lp_diff_post >= 8:
                    #-- hay un tono en x, guardamos su valor.
                    index_tone_list.append(x)
            elif x > 13 and x < 30:
                print("ALTA FRECUENCIA --> diferencia 5 dB")
                if Lp_diff_prev >= 5 and Lp_diff_post >= 5:
                    #-- hay un tono en x, guardamos su valor.
                    index_tone_list.append(x)
    print("------------------------------------------")
    print("-------------LISTA POSICIONES DE LOS TONOS-------------")
    print(index_tone_list)

    #-- Ya tengo las posiciones de los tonos en la lista, ahora debo buscar los datos correspondientes
    #-- en ambas listas y mostrar dichos datos.

    #-- Ahora si voy a crear un diccionario en el que se guardarán los datos correspondientes a los
    #-- tonos prominentes, es decir,  {fc : Lp_mean} 
    prominent_tones = {}

    for i in range (0, len(index_tone_list)):
        index = index_tone_list[i]
        key = fc[index]
        value = Lp_mean[index]
        prominent_tones[key] = value
    
    return prominent_tones

#-- FUNCIONA!!!!!
tonos_prominentes = tone_detector(file)
print(tonos_prominentes)
