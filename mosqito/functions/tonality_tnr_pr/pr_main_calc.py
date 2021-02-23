# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:12:18 2020

@author: wantysal
"""

import numpy as np
from numpy.fft import fft

# from scipy.signal import welch, periodogram

# Local functions imports
from mosqito.functions.shared.conversion import amp2db
from mosqito.functions.tonality_tnr_pr.critical_band import (
    critical_band,
    lower_critical_band,
    upper_critical_band,
)
from mosqito.functions.tonality_tnr_pr.screening_for_tones import screening_for_tones
from mosqito.functions.tonality_tnr_pr.find_highest_tone import find_highest_tone


def pr_main_calc(signal, fs):
    """
        Calculation of the tone-to noise ratio according to the method described
        in ECMA 74, annex D.
        The method to find the tonal candidates is the one described by Wade Bray
        in 'Methods for automating prominent tone evaluation and for considerin
        variations with time or other reference quantities'
        The total value calculated, T-PR, is calculated according to ECMA TR/108

    Parameters
    ----------
    signal : numpy.array
        time history values
    fs : integer
        sampling frequency

    Output
    ------
    tones_freqs : list of float
        frequency of the tones
    tnr : list of float
        TNR value calculated for each tone
    prominence : list of boolean
        prominence criteria as described in ECMA 74
    total_tnr : list of float
        sum of the specific TNR
    """

    #### Spectrum creation #######################################################

    n = len(signal)
    window = np.hanning(n)
    window = window / np.sum(window)

    # Creation of the spectrum by FFT
    spectrum = fft(signal * window) * 1.42

    # Conversion into dB level
    module = np.abs(spectrum)
    spectrum_db = amp2db(module, ref=0.00002)

    # Frequency axis of interest
    freq_axis = np.arange(0, int(n / 2), 1) * (fs / n)
    freq_index = np.where((freq_axis > 89.1) & (freq_axis < 11200))[0]
    freqs = freq_axis[freq_index]
    spec_db = spectrum_db[freq_index]

    #### Screening to find the potential tonal components ########################

    peak_index = screening_for_tones(freqs, spec_db, "smoothed", 90, 11200)
    nb_tones = len(peak_index)

    #### Evaluation of each candidate ############################################

    # Initialization of the results lists
    tones_freqs = np.array(())
    pr = np.array(())
    prominence = []
    # Each candidate is studied and then deleted from the list until all have been treated
    while nb_tones > 0:
        ind = peak_index[0]

        # Find the highest tone in the critical band
        if len(peak_index) > 1:
            ind, _, peak_index, nb_tones = find_highest_tone(
                freqs, spec_db, peak_index, nb_tones, ind
            )

        ft = freqs[ind]

        # Level of the middle critical band
        f1, f2 = critical_band(ft)
        low_limit_idx = np.argmin(np.abs(freqs - f1))
        high_limit_idx = np.argmin(np.abs(freqs - f2))

        spec_sum = sum(10 ** (spec_db[low_limit_idx:high_limit_idx] / 10))
        if spec_sum != 0:
            Lm = 10 * np.log10(spec_sum)
        else:
            Lm = 0

        # Level of the lower critical band
        f1, f2 = lower_critical_band(ft)
        low_limit = np.argmin(np.abs(freqs - f1))
        high_limit = np.argmin(np.abs(freqs - f2))

        spec_sum = sum(10 ** (spec_db[low_limit:high_limit] / 10))
        if spec_sum != 0:
            Ll = 10 * np.log10(spec_sum)
        else:
            Ll = 0

        delta_f = f2 - f1

        # Level of the upper critical band
        f1, f2 = upper_critical_band(ft)
        low_limit = np.argmin(np.abs(freqs - f1))
        high_limit = np.argmin(np.abs(freqs - f2))

        spec_sum = sum(10 ** (spec_db[low_limit:high_limit] / 10))
        if spec_sum != 0:
            Lu = 10 * np.log10(spec_sum)
        else:
            Lu = 0

        if ft <= 171.4:
            delta = 10 * np.log10(10 ** (0.1 * Lm)) - 10 * np.log10(
                ((100 / delta_f) * 10 ** (0.1 * Ll) + 10 ** (0.1 * Lu)) * 0.5
            )

        elif ft > 171.4:
            delta = 10 * np.log10(10 ** (0.1 * Lm)) - 10 * np.log10(
                (10 ** (0.1 * Ll) + 10 ** (0.1 * Lu)) * 0.5
            )

        if delta > 0:
            pr = np.append(pr, delta)
            tones_freqs = np.append(tones_freqs, ft)

            # Prominent discrete tone criteria
            if ft >= 89.1 and ft <= 1000:
                if delta >= 9 + 10 * np.log10(1000 / ft):
                    prominence.append(True)
                else:
                    prominence.append(False)
            elif ft > 1000:
                if delta >= 9:
                    prominence.append(True)
                else:
                    prominence.append(False)

        # suppression from the list of tones of all the candidates belonging to the
        # same critical band
        sup = np.where((peak_index >= low_limit_idx) & (peak_index <= high_limit_idx))[
            0
        ]
        peak_index = np.delete(peak_index, sup)
        nb_tones -= len(sup)

    if sum(np.power(10, (pr / 10))) != 0:
        t_pr = 10 * np.log10(sum(np.power(10, (pr / 10))))
    else:
        t_pr = 0

    return tones_freqs, pr, prominence, t_pr
