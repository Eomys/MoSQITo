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

    """    In the following section, the signal is filtered by a series of 53 asymmetric and overlapping filters. They are 
    supposed to replicate the activation process of the auditory hair cells, and their shape matches the one from the 
    gammatone filters. First, we have to calculate the parameters (central frequency, bandwidth, delay, and "d" 
    coefficient) that are going to define our filter and that are used in the recursive formula number 10. Second, 
    we have to link the critical band rate scale "z", with a certain hop size "sh_array" and its band dependent block 
    size "sb_array" (Table G.1). After that, it comes the coefficient calculation (Formula 11 and 12), in which we 
    compute the values for the filter coefficients (*), and we store them in a list. Finally, the end of this section 
    comes with the filtering of the signal.

    (*) An error in the standard has been found in expressions 13 and 14. The prior paragraph says that in order to 
    obtain the approximation of the band-pass filter, the low-pass filter coefficients shall be modified by adding a 
    negative exponential with the transformation parameters "complex_exponential". If we try to develop the filter with 
    these guidelines, we find that the resulting filter is a low-pass filter, not a band-pass. The actual way of 
    obtaining a band-pass filter by transforming a low-pass filter is to multiply the low pass filter coefficients in 
    time with a positive exponential. After the multiplication we will have complex filter coefficients, we have 2 
    options in order to fix this. Either we make 2 transformations, one to the right and another one to the left, and 
    we adapt the transformation parameter, or we take for granted the last transformation by discarding the complex part 
    of the filter and multiplying by "2" (two transformations) and by a cosine with the original transformation 
    parameter. We decided to implement the second option as they did on ECMA-418-2."""

    # ECMA-418-2 constants
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
