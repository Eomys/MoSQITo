# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:12:18 2020

@author: wantysal
"""

import numpy as np

# from scipy.signal import welch, periodogram

# Local functions imports
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._critical_band import (
    _critical_band,
    _lower_critical_band,
    _upper_critical_band,
)
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._screening_for_tones import (
    _screening_for_tones,
)
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._find_highest_tone import (
    _find_highest_tone,
)


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


    if len(spectrum_db.shape) == 1:
        n = 1
        # Frequency axis of interest
        freq_index = np.where((freq_axis > 89.1) & (freq_axis < 11200))[0]
        freqs = freq_axis[freq_index]
        spec_db = spectrum_db[freq_index]
        
    elif len(spectrum_db.shape) > 1:
        n = spectrum_db.shape[0]
        freqs = [[]for i in range(n)]
        spec_db = [[]for i in range(n)]
        for i in range(n):
            freq_index_cols = np.where((freq_axis[0,:] > 89.1) & (freq_axis[0,:] < 11200))[0]
            freqs[i] = np.append(freqs[i],freq_axis[i,freq_index_cols])
            spec_db[i] = np.append(spec_db[i],spectrum_db[i,freq_index_cols])
        freqs = np.asarray(freqs)
        spec_db = np.asarray(spec_db)

    #### Screening to find the potential tonal components ########################

    peak_index = _screening_for_tones(freqs, spec_db, "smoothed", 90, 11200)

    #### Evaluation of each candidate ############################################

    # Initialization of the results lists
    if n == 1:
        PR = []
        t_pr = []
        tones_freqs = []
        prominence = []
    else:   
        PR = [[]for i in range(n)]
        t_pr = [[]for i in range(n)]
        tones_freqs = [[]for i in range(n)]
        prominence = [[]for i in range(n)]



    for i in range(n):
        
        pr = np.array([])
        
        if n == 1:
            peaks = peak_index.astype(int)
            spec = spec_db
            fr = freqs

        elif n > 1:
            peaks = peak_index[i].astype(int)
            spec = spec_db[i,:]
            fr = freqs[i,:]
        
        nb_tones = len(peaks)

        # Each candidate is studied and then deleted from the list until all have been treated
        while nb_tones > 0:
            ind = peaks[0]
    
            # Find the highest tone in the critical band
            if len(peaks) > 1:
                ind, _, peaks, nb_tones = _find_highest_tone(
                    fr, spec, peaks, nb_tones, ind
                )
    
            ft = fr[ind]
    
            # Level of the middle critical band
            f1, f2 = _critical_band(ft)
            low_limit_idx = np.argmin(np.abs(fr - f1))
            high_limit_idx = np.argmin(np.abs(fr - f2))
    
            spec_sum = sum(10 ** (spec[low_limit_idx:high_limit_idx] / 10))
            if spec_sum != 0:
                Lm = 10 * np.log10(spec_sum)
            else:
                Lm = 0
    
            # Level of the lower critical band
            f1, f2 = _lower_critical_band(ft)
            low_limit = np.argmin(np.abs(fr - f1))
            high_limit = np.argmin(np.abs(fr - f2))
    
            spec_sum = sum(10 ** (spec[low_limit:high_limit] / 10))
            if spec_sum != 0:
                Ll = 10 * np.log10(spec_sum)
            else:
                Ll = 0
    
            delta_f = f2 - f1
    
            # Level of the upper critical band
            f1, f2 = _upper_critical_band(ft)
            low_limit = np.argmin(np.abs(fr - f1))
            high_limit = np.argmin(np.abs(fr - f2))
    
            spec_sum = sum(10 ** (spec[low_limit:high_limit] / 10))
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
                if n > 1:
                    tones_freqs[i] = np.append(tones_freqs[i], ft)
                elif n == 1:
                    tones_freqs = np.append(tones_freqs, ft)
                pr = np.append(pr, delta)

    
                # Prominent discrete tone criteria
                if ft >= 89.1 and ft <= 1000:
                    if delta >= 9 + 10 * np.log10(1000 / ft):
                        if n > 1:
                            prominence[i].append(True)
                       
                        elif n == 1:
                            prominence.append(True)
                    else:
                        if n > 1:
                            prominence[i].append(False)
                        
                        elif n == 1:
                            prominence.append(False)
                            
                elif ft > 1000:
                    if delta >= 9:
                        if n > 1:
                            prominence[i].append(True)
                        
                        elif n == 1:
                            prominence.append(True)
                    else:
                        if n > 1:
                            prominence[i].append(False)
                        
                        elif n == 1:
                            prominence.append(False)
    
            # suppression from the list of tones of all the candidates belonging to the
            # same critical band
            sup = np.where((peaks >= low_limit_idx) & (peaks <= high_limit_idx))[
                0
            ]
            peaks = np.delete(peaks, sup)
            nb_tones -= len(sup)

        if sum(np.power(10, (pr / 10))) != 0:
                if n > 1:
                    t_pr[i] = 10 * np.log10(sum(np.power(10, (pr / 10))))
                elif n == 1:
                    t_pr = 10 * np.log10(sum(np.power(10, (pr / 10))))
        else:
            if n > 1:
                t_pr[i] = np.append(t_pr[i], 0)
            elif n == 1:
                t_pr = np.append(t_pr, 0)
                
                
        if n > 1:
            PR[i] = np.append(PR[i], pr)
            
        elif n == 1:
            PR = np.append(PR, pr)
    
    tones_freqs = np.asarray(tones_freqs)
    prominence = np.asarray(prominence)

    return tones_freqs, PR, prominence, t_pr
