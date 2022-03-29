# -*- coding: utf-8 -*-

import numpy as np

# Local functions imports
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._critical_band import _critical_band
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._screening_for_tones import _screening_for_tones
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._find_highest_tone import _find_highest_tone
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._peak_level import _peak_level


def _tnr_main_calc(spectrum_db, freq_axis):
    """
        Calculation of the tone-to noise ratio according to the method described
        in ECMA 74, annex D.
        The method to find the tonal candidates is the one described by Wade Bray
        in 'Methods for automating prominent tone evaluation and for considerin
        variations with time or other reference quantities'
        The total value calculated, T-TNR, is calculated according to ECMA TR/108

    Parameters
    ----------
    spectrum_db : array
        spectrum values in dB [nperseg x nseg].
    freq_axis : array
        frequency axis corresponding to the spectrum [nperseg x nseg].

    Output
    ------
    tones_freqs : array of float
        frequency of the tones (n blocks x number of tones)
    tnr : array of float
        TNR value calculated for each tone (n blocks x number of tones)
    prominence : array of boolean
        prominence criteria as described in ECMA 74 (n blocks x number of tones)
    t_tnr : array of float
        sum of the specific TNR (n blocks x global value)
    """

    #### Spectrum creation #######################################################


    if len(spectrum_db.shape) == 1:
        nseg = 1
        # Frequency axis of interest
        freq_index = np.where((freq_axis > 89.1) & (freq_axis < 11200))[0]
        freqs = freq_axis[freq_index]
        spec_db = spectrum_db[freq_index]
        
    elif (len(spectrum_db.shape) > 1) & (len(freq_axis.shape) > 1):
        nseg = spectrum_db.shape[1]
        freqs = [[]for i in range(nseg)]
        spec_db = [[]for i in range(nseg)]
        for i in range(nseg):
            # Frequency axis of interest
            freq_index_rows = np.where((freq_axis[:,i] > 89.1) & (freq_axis[:,i] < 11200))[0]
            freqs[i] = np.append(freqs[i],freq_axis[freq_index_rows,i])
            spec_db[i] = np.append(spec_db[i],spectrum_db[freq_index_rows,i])
        freqs = np.asarray(freqs)
        spec_db = np.asarray(spec_db)
        
    elif (len(spectrum_db.shape) > 1) & (len(freq_axis.shape) == 1):
        # Frequency axis of interest
        freq_index = np.where((freq_axis > 89.1) & (freq_axis < 11200))[0]
        # Initialization
        nfreqs = len(freq_index)    
        nseg = spectrum_db.shape[1]
        freqs = np.zeros((nseg,nfreqs))
        spec_db = np.zeros((nseg,nfreqs))
        for i in range(nseg):
            freqs[i,:] = freq_axis[freq_index]
            spec_db[i,:] = spectrum_db[freq_index,i]


    #### Screening to find the potential tonal components ########################

    peak_index = _screening_for_tones(freqs, spec_db, "smoothed", 90, 11200)

    # Initialization of the results lists
    if nseg == 1:
        TNR = []
        t_tnr = []
        tones_freqs = []
        prominence = []
    else:   
        TNR = [[]for i in range(nseg)]
        t_tnr = [[]for i in range(nseg)]
        tones_freqs = [[]for i in range(nseg)]
        prominence = [[]for i in range(nseg)]
    

    #### Evaluation of each candidate ############################################

    for i in range(nseg):
        
        tnr = []
        
        if nseg == 1:
            peaks = peak_index.astype(int)
            spec = spec_db
            fr = freqs
            frs = freq_axis
        elif nseg > 1:
            peaks = peak_index[i].astype(int)
            spec = spec_db[i,:]
            fr = freqs[i,:]
            if len(freq_axis.shape)>1:
                frs = freq_axis[:,i]
            else:
                frs = freq_axis
        
        nb_tones = len(peaks)

        # Each candidate is studied and then deleted from the list until all have been treated
        while nb_tones > 0:
            ind = peaks[0]
            if len(peaks) > 1:
                ind_p, ind_s, peaks, nb_tones = _find_highest_tone(
                    fr, spec, peaks, nb_tones, ind
                )
            else:
                ind_p = ind
                ind_s = None
    
            # multiple tones in a critical band
            if ind_s != None:
                fp = fr[ind_p]
                fs = fr[ind_s]
    
                # proximity criterion
                delta_f = 21 * 10 ** ((1.2 * (np.abs(np.log10(fp / 212))) ** 1.8))
                if np.abs(fs - fp) < delta_f:
    
                    # tone SPL
                    Lp = _peak_level(fr, spec, ind_p)
                    Ls = _peak_level(fr, spec, ind_s)
    
                    Lt = 10 * np.log10(((10 ** (Lp / 10) + 10 ** (Ls / 10))))
    
                    # total SPL in the critical band
                    f1, f2 = _critical_band(fp)
                    low_limit_idx = np.argmin(np.abs(fr - f1))
                    high_limit_idx = np.argmin(np.abs(fr - f2))
    
                    spec_sum = sum(10 ** (spec[low_limit_idx:high_limit_idx] / 10))
                    Ltot = 10 * np.log10(spec_sum)
    
                    # suppression of the second highest tone from the list of tones
                    sup = np.where(peaks == ind_s)[0]
                    peaks = np.delete(peaks, sup)
                    nb_tones -= 1
    
                    delta_ft = 2 * (frs[1] - frs[0])
    
                else:
                    # the two highest tones are not close enough to be considered as one
                    # tone SPL
                    Lt = spec[ind_p]
    
                    # total SPL in the critical band
                    f1, f2 = _critical_band(fr[ind_p])
                    low_limit_idx = np.argmin(np.abs(fr - f1))
                    high_limit_idx = np.argmin(np.abs(fr - f2))
    
                    spec_sum = sum(10 ** (spec[low_limit_idx:high_limit_idx] / 10))
                    Ltot = 10 * np.log10(spec_sum)
    
                    delta_ft = fr[1] - fr[0]
    
            # single tone in a critical band
            else:
                # tone SPL
                Lt = _peak_level(fr, spec, ind_p)
    
                # total SPL in the critical band
                f1, f2 = _critical_band(fr[ind_p])
                low_limit_idx = np.argmin(np.abs(fr - f1))
                high_limit_idx = np.argmin(np.abs(fr - f2))
    
                spec_sum = sum(10 ** (spec[low_limit_idx:high_limit_idx] / 10))
                Ltot = 10 * np.log10(spec_sum)
    
                delta_ft = fr[1] - fr[0]
    
            # SPL of the masking noise
            delta_fc = f2 - f1
            delta_ftot = frs[high_limit_idx] - frs[low_limit_idx]
            Ln = 10 * np.log10(10 ** (Ltot / 10) - 10 ** (Lt / 10)) + 10 * np.log10(
                delta_fc / (delta_ftot - delta_ft)
            )
    
            # Tone-to-noise ratio
            f = fr[ind_p]
            delta_t = Lt - Ln
            if delta_t > 0:
                if nseg > 1:
                    tones_freqs[i] = np.append(tones_freqs[i], f)
                elif nseg == 1:
                    tones_freqs = np.append(tones_freqs, f)
                tnr = np.append(tnr, delta_t)
    
                # Prominence criteria
                if f >= 89.1 and f < 1000:
                    if delta_t >= 8 + 8.33 * np.log10(1000 / f):
                        if nseg > 1:
                            prominence[i].append(True)                        
                        elif nseg == 1:
                            prominence.append(True)
                    else:
                        if nseg > 1:
                            prominence[i].append(False)
                        
                        elif nseg == 1:
                            prominence.append(False)
                elif f >= 1000 and f <= 11200:
                    if delta_t >= 8:
                        if nseg > 1:
                            prominence[i].append(True)
                        
                        elif nseg == 1:
                            prominence.append(True)
                    else:
                        if nseg > 1:
                            prominence[i].append(False)
                        
                        elif nseg == 1:
                            prominence.append(False)
    
            # suppression from the list of tones
            sup = np.where(peaks == ind_p)[0]
            peaks = np.delete(peaks, sup)
            nb_tones -= 1
    

        if nseg > 1:
            if sum(np.power(10, (tnr[prominence[i]] / 10))) != 0:
                t_tnr[i] = 10 * np.log10(sum(np.power(10, (tnr[prominence[i]] / 10))))
            else:
                t_tnr[i] =  0
            TNR[i] = np.append(TNR[i], tnr)               
                    
                    
        elif nseg == 1:
            if sum(np.power(10, (tnr[prominence] / 10))) != 0:
                t_tnr = np.append(t_tnr,10 * np.log10(sum(np.power(10, (tnr[prominence] / 10)))))
            else:
                t_tnr =  0
            TNR = np.append(TNR, tnr)
        
    tones_freqs = np.asarray(tones_freqs)
    prominence = np.asarray(prominence)

    
    return tones_freqs, TNR , prominence, t_tnr
