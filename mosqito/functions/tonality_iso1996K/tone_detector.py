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

#-- Declaración de variables

"""
    Parameters
    ----------
    - data: fichero.csv con los Lp promedio de las banda de tercio de octava.

    Outputs
    -------
    - prominent_tone: array con pares fc:Lp_promedio donde se detectan tonos prominentes.
"""

#-- prueba inicial
print('Hola Mundo')
A = np.array([[1,2,3],
             [4,5,6]])
print(A)