# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import numpy as np
import matplotlib.pyplot as plt


# Project Imports
from mosqito.functions.loudness_ecma_spain.sone2phone import sone2phone
from mosqito.functions.loudness_ecma_spain.comp_loudness_alt import comp_loudness
from mosqito.functions.loudness_ecma_spain.equal_loudness_contours import (
    equal_loudness_contours,
)
from mosqito.functions.loudness_ecma_spain.sine_wave_generator import (
    sine_wave_generator,
)


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
            n_array = comp_loudness(signal)
            specific_loudness = np.array(n_array)
            tot_loudness = np.sum(specific_loudness, axis=0)
            mean_tot_loudness = np.mean(tot_loudness)
            loudness.append(sone2phone(mean_tot_loudness))

        plt.semilogx(freq_vec, phon * np.ones(freq_vec.size), col + ":")
        plt.semilogx(freq_vec, loudness, col, label=str(phon) + " phons")

    plt.xlim(left=100, right=10100)
    plt.ylabel("Loudness [Phons]")
    plt.xlabel("Frequency [Hz]")
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
