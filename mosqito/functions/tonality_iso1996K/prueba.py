# -*- coding: utf-8 -*-
"""
    Autor: Cristina Taboada (TinaTabo)
    Fecha inicio: 19/11/2021
    Fecha última modificación: 19/11/2021
    Descripción: Esto es un programa de prueba de la función "tone_detector" correspondiente
                 a la detección de tonalidad especificada en la iso 1996-2:Anexo K.
"""

#-- Importar función
from tonality_iso1996K import tone_detector


#-- Fichero a leer --> Se debe introducir el nombre del fichero por linea de comandos.
file = input('Enter the data file name: ')

#-- Comprobar funcionamiento
tonos_prominentes = tone_detector(file)
print(tonos_prominentes)