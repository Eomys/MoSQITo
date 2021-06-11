# -*- coding: utf-8 -*-

from numpy import zeros, sqrt, exp, pi
from scipy.special import comb


def gammatone(freq, order=5, fs=48000):
    """
    ECMA-418-2 Gammatone filter design

    This function computes the coefficients of a gammatone digital filter according to ECMA-418-2 section 5.1.3.

    Parameters
    ----------
    freq: float
        Center frequency of the filter ['Hz'].

    order: int, optional
        The order of the filter. Default is "5" according to ECMA-418.2.

    fs: float, optional
        The sampling frequency of the signal. Default is 48000 Hz.

    Returns
    -------
    b, a: ndarray, ndarray
        Numerator (b) and denominator (a) polynomials of the filter.

    """

    # ECMA-74 constant
    af_f0 = 81.9289
    c = 0.1618

    # Bandwidth
    f_bandwidth = sqrt((af_f0 ** 2) + ((c * freq) ** 2))

    # Exponent of the delay
    exponent_1 = (2.0 * order) - 1.0

    # Binomial coefficient
    n_binomial = (2.0 * order) - 2.0
    k_binomial = order - 1.0
    binomial_coef_1 = float(comb(int(n_binomial), int(k_binomial), exact=True))

    # Time constant, delay
    t_delay = (1.0 / (2.0 ** exponent_1)) * binomial_coef_1 * (1.0 / f_bandwidth)

    # "d" coefficient
    d_coefficients = float(exp((-1.0) / (fs * t_delay)))

    # The "e" coefficients are used for the calculation of the bm coefficients for the Auditory Filtering Bank
    e_coefficients_array = [0.0, 1.0, 11.0, 11.0, 1.0]
    # Coefficients for the "Auditory Filtering Bank"
    am_mod_coefficient_band_array = zeros(int(order + 1), dtype=complex)
    bm_mod_coefficient_band_array = zeros(int(order + 1), dtype=complex)

    # Coefficient calculation
    bm_sum = 0.00

    # "b" summation sequence, fraction calculation (F.12)
    for j in range(order - 1):
        iterator_sum = j + 1
        bm_sum = bm_sum + (
            e_coefficients_array[iterator_sum] * (d_coefficients ** iterator_sum)
        )

    bm_numerator = (1 - d_coefficients) ** order
    bm_fraction = bm_numerator / bm_sum

    # Implementation of the recursive formula (F.10)
    for m in range(order + 1):
        exp_factor = (2 * pi * freq * m) / fs
        complex_exponential = 1j * exp_factor

        # Binomial coefficient, "am" coefficient calculation (F.11)
        if m == 0:
            am_coefficient = 1.0
        else:
            binomial_coef_2 = float(comb(order, m, exact=True))

            if (m % 2) == 0:
                am_coefficient = (d_coefficients ** m) * binomial_coef_2
            else:
                am_coefficient = (-1) * (d_coefficients ** m) * binomial_coef_2

        # "bm" coefficient calculation (F.12)
        if m == order:
            bm_coefficient = 0.0
        else:
            bm_coefficient = (
                bm_fraction * (d_coefficients ** m) * e_coefficients_array[m]
            )

        # Transformation from low-pass filter coefficients to band-pass.
        # (*) In this step is where the error that is mentioned at the start of the Auditory Filtering Bank section
        # was found
        am_mod_coefficient_band = am_coefficient * exp(complex_exponential)
        bm_mod_coefficient_band = bm_coefficient * exp(complex_exponential)

        am_mod_coefficient_band_array[m] = am_mod_coefficient_band
        bm_mod_coefficient_band_array[m] = bm_mod_coefficient_band

    return bm_mod_coefficient_band_array, am_mod_coefficient_band_array
