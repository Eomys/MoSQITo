# -*- coding: utf-8 -*-
from numpy import asarray, where, append, empty, array, argmin, log10, power, delete, abs

# from scipy.signal import welch, periodogram

# Local functions imports
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._critical_band import (
    _critical_band,
    _lower_critical_band,
    _upper_critical_band,
)
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._screening_for_tones import _screening_for_tones
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._find_highest_tone import _find_highest_tone


def _pr_main_calc(spectrum_db, freq_axis):
    """
        Calculation of the tone-to noise ratio according to the method described
        in ECMA 74, annex D.
        The method to find the tonal candidates is the one described by Wade Bray
        in 'Methods for automating prominent tone evaluation and for considerin
        variations with time or other reference quantities'
        The total value calculated, T-PR, is calculated according to ECMA TR/108

    Parameters
    ----------
    spectrum_db : array
        Spectrum values in dB [nperseg x nseg]
    freq_axis : array
        frequency axis corresponding to the spectrum [nperseg x nseg]

    Output
    ------
    tones_freqs : array of float
        Frequency list of the tones [number of tones x nseg]
    pr : array of float
        TNR value calculated for each tone [number of tones x nseg]
    prominence : array of boolean
        Prominence criteria as described in ECMA 74 [number of tones x nseg]
    t_pr : array of float
        Sum of the specific TNR
    """

    #### Spectrum creation #######################################################

    if len(spectrum_db.shape) == 1:
        nseg = 1
        # Frequency axis of interest
        freq_index = where((freq_axis > 89.1) & (freq_axis < 11200))[0]
        freqs = freq_axis[freq_index]
        spec_db = spectrum_db[freq_index]

    elif (len(spectrum_db.shape) > 1) & (len(freq_axis.shape) > 1):
        nseg = spectrum_db.shape[1]
        freqs = [[]for i in range(nseg)]
        spec_db = [[]for i in range(nseg)]
        for i in range(nseg):
            # Frequency axis of interest
            freq_index_rows = where(
                (freq_axis[:, i] > 89.1) & (freq_axis[:, i] < 11200))[0]
            freqs[i] = append(freqs[i], freq_axis[freq_index_rows, i])
            spec_db[i] = append(spec_db[i], spectrum_db[freq_index_rows, i])
        freqs = asarray(freqs)
        spec_db = asarray(spec_db)

    elif (len(spectrum_db.shape) > 1) & (len(freq_axis.shape) == 1):
        # Frequency axis of interest
        freq_index = where((freq_axis > 89.1) & (freq_axis < 11200))[0]
        # Initialization
        nfreqs = len(freq_index)
        nseg = spectrum_db.shape[1]
        freqs = empty((nseg, nfreqs))
        spec_db = empty((nseg, nfreqs))
        for i in range(nseg):
            freqs[i, :] = freq_axis[freq_index]
            spec_db[i, :] = spectrum_db[freq_index, i]

    #### Screening to find the potential tonal components ########################

    peak_index = _screening_for_tones(freqs, spec_db, "smoothed", 90, 11200)

    #### Evaluation of each candidate ############################################

    # Initialization of the results lists
    if nseg == 1:
        PR = []
        t_pr = []
        tones_freqs = []
        prominence = []
    else:
        PR = [[]for i in range(nseg)]
        t_pr = [[]for i in range(nseg)]
        tones_freqs = [[]for i in range(nseg)]
        prominence = [[]for i in range(nseg)]

    for i in range(nseg):

        pr = array([], dtype=object)

        if nseg == 1:
            peaks = peak_index
            spec = spec_db
            fr = freqs

        elif nseg > 1:
            peaks = peak_index[i]
            spec = spec_db[i, :]
            fr = freqs[i, :]

        nb_tones = len(peaks)

        # Each candidate is studied and then deleted from the list until all have been treated
        while nb_tones > 0:
            ind = int(peaks[0])

            # Find the highest tone in the critical band
            if len(peaks) > 1:
                ind, _, peaks, nb_tones = _find_highest_tone(
                    fr, spec, peaks.astype(int), nb_tones, ind
                )

            ft = fr[ind]

            # Level of the middle critical band
            f1, f2 = _critical_band(ft)
            low_limit_idx = argmin(abs(fr - f1))
            high_limit_idx = argmin(abs(fr - f2))

            spec_sum = sum(10 ** (spec[low_limit_idx:high_limit_idx] / 10))
            if spec_sum != 0:
                Lm = 10 * log10(spec_sum)
            else:
                Lm = 0

            # Level of the lower critical band
            f1, f2 = _lower_critical_band(ft)
            low_limit = argmin(abs(fr - f1))
            high_limit = argmin(abs(fr - f2))

            spec_sum = sum(10 ** (spec[low_limit:high_limit] / 10))
            if spec_sum != 0:
                Ll = 10 * log10(spec_sum)
            else:
                Ll = 0

            delta_f = f2 - f1

            # Level of the upper critical band
            f1, f2 = _upper_critical_band(ft)
            low_limit = argmin(abs(fr - f1))
            high_limit = argmin(abs(fr - f2))

            spec_sum = sum(10 ** (spec[low_limit:high_limit] / 10))
            if spec_sum != 0:
                Lu = 10 * log10(spec_sum)
            else:
                Lu = 0

            if ft <= 171.4:
                delta = 10 * log10(10 ** (0.1 * Lm)) - 10 * log10(
                    ((100 / delta_f) * 10 ** (0.1 * Ll) + 10 ** (0.1 * Lu)) * 0.5
                )

            elif ft > 171.4:
                delta = 10 * log10(10 ** (0.1 * Lm)) - 10 * log10(
                    (10 ** (0.1 * Ll) + 10 ** (0.1 * Lu)) * 0.5
                )

            if delta > 0:
                if nseg > 1:
                    tones_freqs[i] = append(tones_freqs[i], ft)
                elif nseg == 1:
                    tones_freqs = append(tones_freqs, ft)
                pr = append(pr, delta)

                # Prominent discrete tone criteria
                if ft >= 89.1 and ft <= 1000:
                    if delta >= 9 + 10 * log10(1000 / ft):
                        if nseg > 1:
                            prominence[i].append(True)

                        elif nseg == 1:
                            prominence.append(True)
                    else:
                        if nseg > 1:
                            prominence[i].append(False)

                        elif nseg == 1:
                            prominence.append(False)

                elif ft > 1000:
                    if delta >= 9:
                        if nseg > 1:
                            prominence[i].append(True)

                        elif nseg == 1:
                            prominence.append(True)
                    else:
                        if nseg > 1:
                            prominence[i].append(False)

                        elif nseg == 1:
                            prominence.append(False)

            # suppression from the list of tones of all the candidates belonging to the
            # same critical band
            sup = where((peaks >= low_limit_idx) & (peaks <= high_limit_idx))[0]
            peaks = delete(peaks, sup)
            nb_tones -= len(sup)

        if nseg > 1:
            if sum(power(10, (pr[prominence[i]] / 10))) != 0:
                t_pr[i] = 10 * \
                    log10(sum(power(10, (pr[prominence[i]] / 10))))
            else:
                t_pr[i] = 0
            PR[i] = append(PR[i], pr)

        elif nseg == 1:
            if sum(power(10, (pr[prominence] / 10))) != 0:
                t_pr = append(
                    t_pr, 10 * log10(sum(power(10, (pr[prominence] / 10)))))
            else:
                t_pr = 0
            PR = append(PR, pr)

    tones_freqs = asarray(tones_freqs, dtype=object)
    prominence = asarray(prominence, dtype=object)

    return tones_freqs, PR, prominence, t_pr
