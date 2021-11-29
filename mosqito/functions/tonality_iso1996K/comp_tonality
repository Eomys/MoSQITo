# -*- coding: utf-8 -*-
"""
    Autor: Cristina Taboada (TinaTabo)
    Fecha inicio: 17/11/2021
    Fecha última modificación: 19/11/2021
    Descripción: Función para detectar tonos prominentes a partir de un archivo
                 .csv de datos (niveles de presión sonora promediados para cada
                 tercio de octava).
"""

# Local imports
from mosqito.functions.oct3filter.comp_third_spectrum import comp_third_spec
from mosqito.functions.shared.load import load

# -- Librerias
import csv


def comp_tonality(signal, fs):
    """
    <Descirption in english ;-)>

    Parameters
    ----------
    signal : numpy.array
        time signal values
    fs : integer
        sampling frequency

    Outputs
    -------
    - prominent_tones: diccionario con pares {fc:Lp_mean} donde se detectan tonos prominentes.
    """

    third_spec = comp_third_spec(is_stationary=True, signal=signal, fs=fs)

    # -- Obtener las listas de las frec.centrales y los Lp_promedio.
    fc = third_spec["freqs"]
    Lp_mean = third_spec["values"]

    # -- Longitud de las listas, las 2 tienen la misma long.
    Lp_len = len(Lp_mean)

    # -- Lista donde se guardaran los indices correspondientes a las posiciones donde hay
    # -- un tono prominente
    index_tone_list = []

    for x in range(0, Lp_len):
        if x > 0 and x < 27:  # dirty correction, to be improved
            # -- Variables a comparar
            Lp_prev = int(Lp_mean[x - 1])
            Lp = int(Lp_mean[x])
            Lp_post = int(Lp_mean[x + 1])

            # -- calculamos la diferencia
            Lp_diff_prev = Lp - Lp_prev
            Lp_diff_post = Lp - Lp_post

            # -- Comparar niveles para determinar si es un tono prominente.
            if x > 0 and x < 9:
                # -- "BAJA FRECUENCIA --> diferencia 15 dB"
                if Lp_diff_prev >= 15 and Lp_diff_post >= 15:
                    # -- hay un tono en x, guardamos su valor.
                    index_tone_list.append(x)

            elif x > 8 and x < 14:
                # -- "MEDIA FRECUENCIA --> diferencia 8 dB"
                if Lp_diff_prev >= 8 and Lp_diff_post >= 8:
                    # -- hay un tono en x, guardamos su valor.
                    index_tone_list.append(x)
            elif x > 13 and x < 30:
                # -- "ALTA FRECUENCIA --> diferencia 5 dB"
                if Lp_diff_prev >= 5 and Lp_diff_post >= 5:
                    # -- hay un tono en x, guardamos su valor.
                    index_tone_list.append(x)

    # -- Diccionario en el que se guardarán los datos correspondientes a los
    # -- tonos prominentes, es decir,  {fc : Lp_mean}
    prominent_tones = {}

    for i in range(0, len(index_tone_list)):
        index = index_tone_list[i]
        key = fc[index]
        value = Lp_mean[index]
        prominent_tones[key] = value

    # -- Retorno de la función.
    return prominent_tones


if __name__ == "__main__":
    sig, fs = load(True, "tests/input/1KHZ60DB.WAV", calib=1)
    tones = comp_tonality(sig, fs)
    pass