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
    duration = 2
    # Sampling frequency
    fs = 48000.0
    # Pressure of reference
    p_ref = float((2 * (10 ** (-5))))

    # Array of frequencies of the AFB
    freq_array1 = np.array(
        [
            41.00914871505695,
            82.2868409326493,
            124.10337868030052,
            166.73259255100055,
            210.45363485007306,
            255.55280759063885,
            302.32543730808527,
            351.0778089705394,
            402.12917164932713,
            455.8138290833099,
            512.4833288269103,
            572.5087643172005,
            636.2832049348641,
            704.2242699719933,
            776.7768633620453,
            854.4160870800056,
            937.6503522908124,
            1027.024708619026,
            1123.1244133410646,
            1226.5787638724394,
            1338.0652186465666,
            1458.3138333702414,
            1588.1120417060679,
            1728.3098116875572,
            1879.8252116330764,
            2043.6504220063591,
            2220.858232591531,
            2412.6090675286264,
            2620.15858421219,
            2844.8658958134583,
            3088.2024712702996,
            3351.7617710254617,
            3637.2696816115767,
            3946.5958174125717,
            4281.765763609721,
            4644.974340483777,
            5038.599975932929,
            5465.22028032323,
            5927.628925661629,
            6428.853939622738,
            6972.177534225708,
            7561.157599006812,
            8199.650999433281,
            8891.838833125257,
            9642.253809273152,
            10455.809930541354,
            11337.834671826557,
            12294.103866589578,
            13330.879529209504,
        ]
    )

    # Array of frequencies for loudness contours
    freq_array = np.array(
        [
            20.0,
            25.0,
            31.5,
            40.0,
            50.0,
            63.0,
            80.0,
            100.0,
            125.0,
            160.0,
            200.0,
            250.0,
            315.0,
            400.0,
            500.0,
            630.0,
            800.0,
            1000.0,
            1250.0,
            1600.0,
            2000.0,
            2500.0,
            3150.0,
            4000.0,
            5000.0,
            6300.0,
            8000.0,
            10000.0,
            12500.0,
        ]
    )

    n_frequencies = len(freq_array)

    phons = [20, 40, 60, 80]
    # phons = [15.45, 40.1, 67.25, 94.9]

    n_phons = len(phons)

    phon_loudness_array = np.zeros((n_phons, n_frequencies), dtype=float)
    phon_final_array = np.zeros((n_phons, n_frequencies), dtype=float)

    for i_phone_contours in range(n_phons):
        # The next sentence returns an array with the dB SPL values for an specific phon value
        # spl_contours_array = equal_loudness_contours(phons[i_phone_contours])[0]
        print("Phone cont: " + str(phons[i_phone_contours]))
        phon_ref_value = phons[i_phone_contours]

        for i_freq in range(n_frequencies):
            signal, samples = sine_wave_generator(
                fs, duration, phon_ref_value, freq_array[i_freq]
            )
            print("Freq: " + str(freq_array[i_freq]))

            """
            The next sentence returns the "t_array" from the function comp_loudness to then calculate the mean value 
            of the array. That makes possible to retain the resulting loudness.
            """
            t_array = comp_loudness(signal, validation=False)[1]
            # CHANGED TO MAX
            mean_loudness_value = float(np.mean(t_array[:, 0]))
            print("t_array: " + str(mean_loudness_value))

            """
            Here is calculated the phon value for the result that is in sones.
            """
            phon_loudness_value = sone2phone(mean_loudness_value)

            phon_loudness_array[i_phone_contours][i_freq] = phon_loudness_value
            print("phone_loudness_value: " + str(phon_loudness_value))

            phon_diff = abs(phon_ref_value - phon_loudness_value)

            phon_final_value = (
                phon_ref_value - phon_diff
                if (phon_ref_value <= phon_loudness_value)
                else phon_ref_value + phon_diff
            )

            phon_final_array[i_phone_contours][i_freq] = phon_final_value
            print("phone_loudness_value: " + str(phon_final_value))

    spl_array_0_phons, frequencies = equal_loudness_contours(0)
    spl_array_20_phons = equal_loudness_contours(20)[0]
    spl_array_40_phons = equal_loudness_contours(40)[0]
    spl_array_60_phons = equal_loudness_contours(60)[0]
    spl_array_80_phons = equal_loudness_contours(80)[0]

    plt.figure(figsize=(10, 5))
    # plt.semilogx(frequencies, spl_array_0_phons, 'g:')
    plt.semilogx(frequencies, spl_array_20_phons, "b:")
    plt.semilogx(frequencies, spl_array_40_phons, "g:")
    plt.semilogx(frequencies, spl_array_60_phons, "r:")
    plt.semilogx(frequencies, spl_array_80_phons, "c:")

    plt.semilogx(freq_array, phon_final_array[0, :], "b", label="20 phons")
    plt.semilogx(freq_array, phon_final_array[1, :], "g", label="40 phons")
    plt.semilogx(freq_array, phon_final_array[2, :], "r", label="60 phons")
    plt.semilogx(freq_array, phon_final_array[3, :], "c", label="80 phons")
    # [
    #     plt.semilogx(
    #         freq_array,
    #         phon_final_array[ii_phone_contour, :],
    #         label=str(phons[ii_phone_contour]) + " phons",
    #     )
    #     for ii_phone_contour in range(n_phons)
    # ]

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
    # hearing_model_validation()
    sig, samp = sine_wave_generator(48000, 5, 100, 1000)

    # plt.figure(figsize=(10, 5))
    # plt.plot(samp, sig)
    # plt.xlim(left=0)
    # plt.ylabel('Sound pressure level [dB SPL]')
    # plt.xlabel('Time (s)')
    # plt.title('prueba')
    # plt.grid(which='both', linestyle='-', color='grey')
    # plt.show()
    #
    # spl_array_0_phons, frequencies = equal_loudness_contours(0)
    # spl_array_20_phons = equal_loudness_contours(20)[0]
    # spl_array_40_phons = equal_loudness_contours(40)[0]
    # spl_array_60_phons = equal_loudness_contours(60)[0]
    # spl_array_80_phons = equal_loudness_contours(80)[0]
    #
    # plt.figure(figsize=(10, 5))
    # plt.semilogx(frequencies, spl_array_0_phons, 'green')
    # plt.semilogx(frequencies, spl_array_20_phons, 'purple')
    # plt.semilogx(frequencies, spl_array_40_phons, 'yellow')
    # plt.semilogx(frequencies, spl_array_60_phons, 'red')
    # plt.semilogx(frequencies, spl_array_80_phons, 'blue')
    # plt.xlim(right=20000)
    # plt.ylabel('Sound pressure level [dB SPL]')
    # plt.xlabel('Frequency [Hz]')
    # plt.title('Specific loudness contours (Right channel)')
    # plt.grid(which='both', linestyle='-', color='grey')
    # plt.show()

    # fs = 48000
    # n = len(sig)
    # plt.figure(figsize=(10, 5))
    # freqs = np.linspace(0, fs / 2, n)
    # spectrum = 20 * np.log10(abs(np.fft.fft(sig * np.blackman(n))))

    # plt.plot(freqs, spectrum)

    # plt.xscale('log')
    # plt.xlim(10, 10000)
    # plt.ylim(0, 200)
    # plt.xlabel("Frequency [Hz]")
    # plt.ylabel("Amplitude [dB]")
    # plt.show()

    hearing_model_validation()
