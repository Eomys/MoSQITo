# -*- coding: utf-8 -*-
"""
@date Created on Fri May 22 2020
@author martin_g for Eomys
"""

# Third party imports
import numpy as np
from scipy import signal

# Local application imports
from mosqito.functions.oct3filter.square_and_smooth import square_and_smooth


def calc_third_octave_levels(sig, fs):
    """3rd octave filtering, squaring, smoothing, level calculation and
    downsampling to temporal resolution: 0,5 ms, i.e. sampling rate: 2 kHz

    See ISO 532-1 section 6.3

    Parameters
    ----------
    sig : numpy.ndarray
        time signal sampled at 48 kHz[pa]
    fs : int
        time signal sampling frequency

    Outputs
    -------
    third_octave_levels : numpy.ndarray
        Set of time signals filtered per third octave bands
    """
    # Sampling frequency shall be equal to 48 kHz (as per ISO 532)
    if fs != 48000:
        raise ValueError("""ERROR: Sampling frequency shall be equal to 48 kHz""")
    # Constants
    n_level_band = 28
    n_filter_coeff = 6
    dec_factor = int(fs / 2000)
    # Initialisation
    coeff = np.zeros(n_filter_coeff)
    # Filter coefficients of one-third-octave-band filters (reference
    # table)
    # ISO 532-1 Table A.1
    third_octave_filter_ref = np.array(
        [[1, 2, 1, 1, -2, 1], [1, 0, -1, 1, -2, 1], [1, -2, 1, 1, -2, 1]]
    )
    # Filter coefficients of one-third-octave-band filters (difference to
    # reference table for 28 one-third-octave-band filters)
    # ISO 532-1 Table A.2
    third_octave_filter = np.array(
        [
            [
                [0, 0, 0, 0, -6.70260e-004, 6.59453e-004],
                [0, 0, 0, 0, -3.75071e-004, 3.61926e-004],
                [0, 0, 0, 0, -3.06523e-004, 2.97634e-004],
            ],
            [
                [0, 0, 0, 0, -8.47258e-004, 8.30131e-004],
                [0, 0, 0, 0, -4.76448e-004, 4.55616e-004],
                [0, 0, 0, 0, -3.88773e-004, 3.74685e-004],
            ],
            [
                [0, 0, 0, 0, -1.07210e-003, 1.04496e-003],
                [0, 0, 0, 0, -6.06567e-004, 5.73553e-004],
                [0, 0, 0, 0, -4.94004e-004, 4.71677e-004],
            ],
            [
                [0, 0, 0, 0, -1.35836e-003, 1.31535e-003],
                [0, 0, 0, 0, -7.74327e-004, 7.22007e-004],
                [0, 0, 0, 0, -6.29154e-004, 5.93771e-004],
            ],
            [
                [0, 0, 0, 0, -1.72380e-003, 1.65564e-003],
                [0, 0, 0, 0, -9.91780e-004, 9.08866e-004],
                [0, 0, 0, 0, -8.03529e-004, 7.47455e-004],
            ],
            [
                [0, 0, 0, 0, -2.19188e-003, 2.08388e-003],
                [0, 0, 0, 0, -1.27545e-003, 1.14406e-003],
                [0, 0, 0, 0, -1.02976e-003, 9.40900e-004],
            ],
            [
                [0, 0, 0, 0, -2.79386e-003, 2.62274e-003],
                [0, 0, 0, 0, -1.64828e-003, 1.44006e-003],
                [0, 0, 0, 0, -1.32520e-003, 1.18438e-003],
            ],
            [
                [0, 0, 0, 0, -3.57182e-003, 3.30071e-003],
                [0, 0, 0, 0, -2.14252e-003, 1.81258e-003],
                [0, 0, 0, 0, -1.71397e-003, 1.49082e-003],
            ],
            [
                [0, 0, 0, 0, -4.58305e-003, 4.15355e-003],
                [0, 0, 0, 0, -2.80413e-003, 2.28135e-003],
                [0, 0, 0, 0, -2.23006e-003, 1.87646e-003],
            ],
            [
                [0, 0, 0, 0, -5.90655e-003, 5.22622e-003],
                [0, 0, 0, 0, -3.69947e-003, 2.87118e-003],
                [0, 0, 0, 0, -2.92205e-003, 2.36178e-003],
            ],
            [
                [0, 0, 0, 0, -7.65243e-003, 6.57493e-003],
                [0, 0, 0, 0, -4.92540e-003, 3.61318e-003],
                [0, 0, 0, 0, -3.86007e-003, 2.97240e-003],
            ],
            [
                [0, 0, 0, 0, -1.00023e-002, 8.29610e-003],
                [0, 0, 0, 0, -6.63788e-003, 4.55999e-003],
                [0, 0, 0, 0, -5.15982e-003, 3.75306e-003],
            ],
            [
                [0, 0, 0, 0, -1.31230e-002, 1.04220e-002],
                [0, 0, 0, 0, -9.02274e-003, 5.73132e-003],
                [0, 0, 0, 0, -6.94543e-003, 4.71734e-003],
            ],
            [
                [0, 0, 0, 0, -1.73693e-002, 1.30947e-002],
                [0, 0, 0, 0, -1.24176e-002, 7.20526e-003],
                [0, 0, 0, 0, -9.46002e-003, 5.93145e-003],
            ],
            [
                [0, 0, 0, 0, -2.31934e-002, 1.64308e-002],
                [0, 0, 0, 0, -1.73009e-002, 9.04761e-003],
                [0, 0, 0, 0, -1.30358e-002, 7.44926e-003],
            ],
            [
                [0, 0, 0, 0, -3.13292e-002, 2.06370e-002],
                [0, 0, 0, 0, -2.44342e-002, 1.13731e-002],
                [0, 0, 0, 0, -1.82108e-002, 9.36778e-003],
            ],
            [
                [0, 0, 0, 0, -4.28261e-002, 2.59325e-002],
                [0, 0, 0, 0, -3.49619e-002, 1.43046e-002],
                [0, 0, 0, 0, -2.57855e-002, 1.17912e-002],
            ],
            [
                [0, 0, 0, 0, -5.91733e-002, 3.25054e-002],
                [0, 0, 0, 0, -5.06072e-002, 1.79513e-002],
                [0, 0, 0, 0, -3.69401e-002, 1.48094e-002],
            ],
            [
                [0, 0, 0, 0, -8.26348e-002, 4.05894e-002],
                [0, 0, 0, 0, -7.40348e-002, 2.24476e-002],
                [0, 0, 0, 0, -5.34977e-002, 1.85371e-002],
            ],
            [
                [0, 0, 0, 0, -1.17018e-001, 5.08116e-002],
                [0, 0, 0, 0, -1.09516e-001, 2.81387e-002],
                [0, 0, 0, 0, -7.85097e-002, 2.32872e-002],
            ],
            [
                [0, 0, 0, 0, -1.67714e-001, 6.37872e-002],
                [0, 0, 0, 0, -1.63378e-001, 3.53729e-002],
                [0, 0, 0, 0, -1.16419e-001, 2.93723e-002],
            ],
            [
                [0, 0, 0, 0, -2.42528e-001, 7.98576e-002],
                [0, 0, 0, 0, -2.45161e-001, 4.43370e-002],
                [0, 0, 0, 0, -1.73972e-001, 3.70015e-002],
            ],
            [
                [0, 0, 0, 0, -3.53142e-001, 9.96330e-002],
                [0, 0, 0, 0, -3.69163e-001, 5.53535e-002],
                [0, 0, 0, 0, -2.61399e-001, 4.65428e-002],
            ],
            [
                [0, 0, 0, 0, -5.16316e-001, 1.24177e-001],
                [0, 0, 0, 0, -5.55473e-001, 6.89403e-002],
                [0, 0, 0, 0, -3.93998e-001, 5.86715e-002],
            ],
            [
                [0, 0, 0, 0, -7.56635e-001, 1.55023e-001],
                [0, 0, 0, 0, -8.34281e-001, 8.58123e-002],
                [0, 0, 0, 0, -5.94547e-001, 7.43960e-002],
            ],
            [
                [0, 0, 0, 0, -1.10165e000, 1.91713e-001],
                [0, 0, 0, 0, -1.23939e000, 1.05243e-001],
                [0, 0, 0, 0, -8.91666e-001, 9.40354e-002],
            ],
            [
                [0, 0, 0, 0, -1.58477e000, 2.39049e-001],
                [0, 0, 0, 0, -1.80505e000, 1.28794e-001],
                [0, 0, 0, 0, -1.32500e000, 1.21333e-001],
            ],
            [
                [0, 0, 0, 0, -2.50630e000, 1.42308e-001],
                [0, 0, 0, 0, -2.19464e000, 2.76470e-001],
                [0, 0, 0, 0, -1.90231e000, 1.47304e-001],
            ],
        ]
    )
    # Filter gain values
    # ISO 532-1 Table A.2
    filter_gain = np.array(
        [
            4.30764e-011,
            8.59340e-011,
            1.71424e-010,
            3.41944e-010,
            6.82035e-010,
            1.36026e-009,
            2.71261e-009,
            5.40870e-009,
            1.07826e-008,
            2.14910e-008,
            4.28228e-008,
            8.54316e-008,
            1.70009e-007,
            3.38215e-007,
            6.71990e-007,
            1.33531e-006,
            2.65172e-006,
            5.25477e-006,
            1.03780e-005,
            2.04870e-005,
            4.05198e-005,
            7.97914e-005,
            1.56511e-004,
            3.04954e-004,
            5.99157e-004,
            1.16544e-003,
            2.27488e-003,
            3.91006e-003,
        ]
    )

    # Definition of the range of preferred filter center frequency
    freq = [
        25,
        31.5,
        40,
        50,
        63,
        80,
        100,
        125,
        160,
        200,
        250,
        315,
        400,
        500,
        630,
        800,
        1000,
        1250,
        1600,
        2000,
        2500,
        3150,
        4000,
        5000,
        6300,
        8000,
        10000,
        12500,
    ]

    n_time = len(sig[::dec_factor])
    time_axis = np.linspace(0, len(sig) / fs, num=n_time)

    third_octave_level = np.zeros((n_level_band, n_time))
    for i_bands in range(n_level_band):
        # Initialisation
        tiny_value = 10 ** -12
        i_ref = 4 * 10 ** -10
        # 2nd order fltering (See ISO 532-1 section 6.3 and A.2)
        coeff = third_octave_filter_ref - third_octave_filter[i_bands, :, :]
        sig_filt = filter_gain[i_bands] * signal.sosfilt(coeff, sig)
        # Calculate center frequency of filter
        center_freq = 10 ** ((i_bands - 16) / 10) * 1000
        # Squaring and smoothing of filtered signal
        sig_filt = square_and_smooth(sig_filt, center_freq, 48000)
        # SPL calculation and decimation
        third_octave_level[i_bands, :] = 10 * np.log10(
            (sig_filt[::dec_factor] + tiny_value) / i_ref
        )

    return third_octave_level, freq, time_axis
