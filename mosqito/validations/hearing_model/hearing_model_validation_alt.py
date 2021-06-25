# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import numpy as np
import math
import scipy as sp
import matplotlib.pyplot as plt
from scipy.signal import welch

# Project Imports
from mosqito.functions.hearing_model.sone2phone import sone2phone
from mosqito.functions.hearing_model.phone2spl import phone2spl
from mosqito.functions.hearing_model.comp_loudness import comp_loudness
from mosqito.functions.hearing_model.equal_loudness_contours import (
    equal_loudness_contours,
)
from mosqito.functions.hearing_model.sine_wave_generator import sine_wave_generator

import sys

sys.path.append("../../..")


def hearing_model_validation():
    """Function that serves for the validation of the hearing model presented in Annex F of ECMA-74.

    Parameters
    ----------

    Returns
    -------

    """
    # Duration of the signal
    duration = 1
    # Sampling frequency
    fs = 48000.0

    phons = [20, 40, 60, 80]

    plt.figure(figsize=(10, 5))
    col_vec = ["b", "g", "r", "c"]

    for phon, col in zip(phons, col_vec):
        spl_vec, freq_vec = equal_loudness_contours(phon)

        # The next sentence returns an array with the dB SPL values for an specific phon value
        # spl_contours_array = equal_loudness_contours(phons[i_phone_contours])[0]
        print("Phone cont: " + str(phon))
        # phon_ref_value = phons[i_phone_contours]

        loudness = []

        for freq, spl in zip(freq_vec, spl_vec):
            signal, _ = sine_wave_generator(fs, duration, spl, freq)
            print("Freq: " + str(freq))

            """
            The next sentence returns the "t_array" from the function comp_loudness to then calculate the mean value 
            of the array. That makes possible to retain the resulting loudness.
            """
            t_array = comp_loudness(signal, validation=False)[1]
            mean_loudness_value = np.mean(t_array[:, 0])
            loudness.append(sone2phone(mean_loudness_value))

        plt.semilogx(freq_vec, spl_vec, col + ":")
        plt.semilogx(freq_vec, loudness, col, label=str(phon) + " phons")

    plt.xlim(left=100, right=10100)
    plt.ylabel("Sound pressure level [dB SPL]")
    plt.xlabel("Frequency [Hz]")
    plt.title("Specific loudness contours")
    plt.grid(which="both", linestyle="-", color="grey")
    plt.xticks(
        [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000],
        ["20", "50", "100", "200", "500", "1K", "2K", "5K", "10K", "20K"],
    )
    plt.legend()
    plt.show()

    print("Validation passed")


if __name__ == "__main__":
    hearing_model_validation()
