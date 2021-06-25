# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import cmath
import numpy as np
import math
import scipy as sp
from scipy.special import comb


def afb_coefficients(fs, filter_order_k, centre_freq, d_coefficients):
    """Function for the calculation of the filter coefficients in the Auditory Filtering Bank section (5.1.3). Here, as
    it has been mentioned in the principal function for the specific loudness, it is calculated the band-pass equivalent
    of the low-pass filter. The typo/error found in the formulas (13 and 14) presented in the ECMA-418-2 has been
    already corrected.

    Parameters
    ----------
    fs: float
        'Hz', sampling frequency.

    filter_order_k: int
        Order of the auditory filtering bank.

    centre_freq: float
        'Hz', central frequency of the filter.

    d_coefficients: float
        "d" coefficient, related with sampling rate and delay.

    Returns
    -------
    am_mod_coefficient_band_array: numpy.array
        "am" coefficient to filter a signal.

    bm_mod_coefficient_band_array: numpy.array
        "bm" coefficient to filter a signal.
    """
    print("This function is deprecated and will be removed form the project")

    # The "e" coefficients are used for the calculation of the bm coefficients for the Auditory Filtering Bank
    e_coefficients_array = [0.0, 1.0, 11.0, 11.0, 1.0]
    # Coefficients for the "Auditory Filtering Bank"
    am_mod_coefficient_band_array = np.zeros(int(filter_order_k + 1), dtype=complex)
    bm_mod_coefficient_band_array = np.zeros(int(filter_order_k + 1), dtype=complex)

    # Coefficient calculation
    bm_sum = 0.00

    # "b" summation sequence, fraction calculation (F.12)
    for j in range(filter_order_k - 1):
        iterator_sum = j + 1
        bm_sum = bm_sum + (
            e_coefficients_array[iterator_sum] * (d_coefficients ** iterator_sum)
        )

    bm_numerator = (1 - d_coefficients) ** filter_order_k
    bm_fraction = bm_numerator / bm_sum

    # Implementation of the recursive formula (F.10)
    for m in range(filter_order_k + 1):
        exp_factor = (2 * math.pi * centre_freq * m) / fs
        complex_exponential = 1j * exp_factor

        # Binomial coefficient, "am" coefficient calculation (F.11)
        if m == 0:
            am_coefficient = 1.0
        else:
            binomial_coef_2 = float(sp.special.comb(filter_order_k, m, exact=True))

            if (m % 2) == 0:
                am_coefficient = (d_coefficients ** m) * binomial_coef_2
            else:
                am_coefficient = (-1) * (d_coefficients ** m) * binomial_coef_2

        # "bm" coefficient calculation (F.12)
        if m == filter_order_k:
            bm_coefficient = 0.0
        else:
            bm_coefficient = (
                bm_fraction * (d_coefficients ** m) * e_coefficients_array[m]
            )

        # Transformation from low-pass filter coefficients to band-pass.
        # (*) In this step is where the error that is mentioned at the start of the Auditory Filtering Bank section
        # was found
        am_mod_coefficient_band = am_coefficient * cmath.exp(complex_exponential)
        bm_mod_coefficient_band = bm_coefficient * cmath.exp(complex_exponential)

        am_mod_coefficient_band_array[m] = am_mod_coefficient_band
        bm_mod_coefficient_band_array[m] = bm_mod_coefficient_band

    return am_mod_coefficient_band_array, bm_mod_coefficient_band_array
