# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 15:03:31 2020

@author: wantysal
"""

import numpy as np
from numpy.fft import fft

# Local functions imports
from mosqito.functions.shared.conversion import amp2db
from mosqito.functions.tonality_tnr_pr.critical_band import critical_band
from mosqito.functions.tonality_tnr_pr.screening_for_tones import screening_for_tones
from mosqito.functions.tonality_tnr_pr.find_highest_tone import find_highest_tone
from mosqito.functions.tonality_tnr_pr.peak_level import spectrum_peak_level


def tnr_main_calc(signal, fs):
    """
        Calculation of the tone-to noise ratio according to the method described
        in ECMA 74, annex D.
        The method to find the tonal candidates is the one described by Wade Bray
        in 'Methods for automating prominent tone evaluation and for considerin
        variations with time or other reference quantities'
        The total value calculated, T-TNR, is calculated according to ECMA TR/108

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
    t_tnr : list of float
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
    tnr = np.array(())
    tones_freqs = np.array(())
    prominence = []

    # Each candidate is studied and then deleted from the list until all have been treated
    while nb_tones > 0:
        ind = peak_index[0]
        if len(peak_index) > 1:
            ind_p, ind_s, peak_index, nb_tones = find_highest_tone(
                freqs, spec_db, peak_index, nb_tones, ind
            )
        else:
            ind_p = ind
            ind_s = None

        # multiple tones in a critical band
        if ind_s != None:
            fp = freqs[ind_p]
            fs = freqs[ind_s]

            # proximity criterion
            delta_f = 21 * 10 ** ((1.2 * (np.abs(np.log10(fp / 212))) ** 1.8))
            if np.abs(fs - fp) < delta_f:

                # tone SPL
                Lp = spectrum_peak_level(freqs, spec_db, ind_p)
                Ls = spectrum_peak_level(freqs, spec_db, ind_s)

                Lt = 10 * np.log10(((10 ** (Lp / 10) + 10 ** (Ls / 10))))

                # total SPL in the critical band
                f1, f2 = critical_band(fp)
                low_limit_idx = np.argmin(np.abs(freqs - f1))
                high_limit_idx = np.argmin(np.abs(freqs - f2))

                spec_sum = sum(10 ** (spec_db[low_limit_idx:high_limit_idx] / 10))
                Ltot = 10 * np.log10(spec_sum)

                # suppression of the second highest tone from the list of tones
                sup = np.where(peak_index == ind_s)[0]
                peak_index = np.delete(peak_index, sup)
                nb_tones -= 1

                delta_ft = 2 * (freq_axis[1] - freq_axis[0])

            else:
                # the two highest tones are not close enough to be considered as one
                # tone SPL
                Lt = spec_db[ind_p]

                # total SPL in the critical band
                f1, f2 = critical_band(freqs[ind_p])
                low_limit_idx = np.argmin(np.abs(freqs - f1))
                high_limit_idx = np.argmin(np.abs(freqs - f2))

                spec_sum = sum(10 ** (spec_db[low_limit_idx:high_limit_idx] / 10))
                Ltot = 10 * np.log10(spec_sum)

                delta_ft = freqs[1] - freqs[0]

        # single tone in a critical band
        else:
            # tone SPL
            Lt = spectrum_peak_level(freqs, spec_db, ind_p)

            # total SPL in the critical band
            f1, f2 = critical_band(freqs[ind_p])
            low_limit_idx = np.argmin(np.abs(freqs - f1))
            high_limit_idx = np.argmin(np.abs(freqs - f2))

            spec_sum = sum(10 ** (spec_db[low_limit_idx:high_limit_idx] / 10))
            Ltot = 10 * np.log10(spec_sum)

            delta_ft = freqs[1] - freqs[0]

        # SPL of the masking noise
        delta_fc = f2 - f1
        delta_ftot = freq_axis[high_limit_idx] - freq_axis[low_limit_idx]
        Ln = 10 * np.log10(10 ** (Ltot / 10) - 10 ** (Lt / 10)) + 10 * np.log10(
            delta_fc / (delta_ftot - delta_ft)
        )

        # Tone-to-noise ratio
        f = freqs[ind_p]
        delta_t = Lt - Ln
        if delta_t > 0:
            tones_freqs = np.append(tones_freqs, f)
            tnr = np.append(tnr, delta_t)

            # Prominence criteria
            if f >= 89.1 and f < 1000:
                if delta_t >= 8 + 8.33 * np.log10(1000 / f):
                    prominence.append(True)
                else:
                    prominence.append(False)
            elif f >= 1000 and f <= 11200:
                if delta_t >= 8:
                    prominence.append(True)
                else:
                    prominence.append(False)

        # suppression from the list of tones
        sup = np.where(peak_index == ind_p)[0]
        peak_index = np.delete(peak_index, sup)
        nb_tones -= 1

    if sum(np.power(10, (tnr / 10))) != 0:
        t_tnr = 10 * np.log10(sum(np.power(10, (tnr / 10))))
    else:
        t_tnr = 0

    return tones_freqs, tnr, prominence, t_tnr
