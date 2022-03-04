# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:51:19 2020

@author: wantysal
"""


# Standard library imports
import numpy as np
import math

# Local functions imports
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc


def tone_to_noise_ecma(is_stationary, signal, fs, freqs=None, prominence=True):
    """Computation of tone-to-noise ration according to ECMA-74, annex D.9
        The T-TNR value is calculated according to ECMA-TR/108

    Parameters
    ----------
    is_stationary : boolean
        True if the signal is stationary
    signal :numpy.array
        time signal values or frequency spectrum in dB
    fs : integer
        sampling frequency
    freqs : np.array
        if signal is given in frequency domain, freqs is the correcponding frequency axis. Default is None
    prominence : boolean
        if True, the algorithm only returns the prominent tones, if False it returns all tones detected

    Output
    ------
    output = dict
    {    "name" : "tone-to-noise ratio",
         "time" : np.linspace(0, len(signal)/fs, num=nb_frame),
         "freqs" : <frequency of the tones>
         "values" : <TNR calculated value for each tone>
         "prominence" : <True or False according to ECMA criteria>
         "global value" : <sum of the specific TNR values>
            }


    """
    
    # if the input is a time signal, the spectrum computation is needed
    if freqs == None:
        if is_stationary == True:
            # compute db spectrum
            spectrum_db, freq_axis = spectrum(signal, fs, db=True)
        if is_stationary == False:
            # Signal cut in frames of 200 ms along the time axis
            n = 0.5 * fs
            nb_frame = math.floor(signal.size / n)
            len_seg = len(signal)//nb_frame
            time = np.linspace(0, len(signal) / fs, num=nb_frame)
            time = np.around(time, 1)

            signal = signal.reshape((nb_frame,len_seg))
            spectrum_db, freq_axis = spectrum(signal, fs, db=True)
    else:
        if signal.shape != freqs.shape :
            raise ValueError('Input spectrum and frequency axis must have the same shape')
        else :
            spectrum_db = signal
            freq_axis = freqs
            
            
    # compute tnr values
    tones_freqs, tnr, prom, t_tnr = _tnr_main_calc(spectrum_db, freq_axis)

            
    if type(tnr[0])== np.ndarray:
        if freqs == None:
            # Retore the results in a time vs frequency array
            freqs = np.logspace(np.log10(90), np.log10(11200), num=1000)
            TNR = np.empty((len(freqs), nb_frame))
            TNR.fill(np.nan)
            promi = np.empty((len(freqs), nb_frame), dtype=bool)
            promi.fill(np.nan)

            for t in range(nb_frame):
                for f in range(len(tones_freqs[t])):
                    ind = np.argmin(np.abs(freqs - tones_freqs[t][f]))
                    if prominence == False:
                        TNR[ind, t] = tnr[t][f]
                        promi[ind, t] = prom[t][f]
                    if prominence == True:
                        if prom[t][f] == True:
                            TNR[ind, t] = tnr[t][f]
                            promi[ind, t] = prom[t][f]


            t_tnr = np.ravel(t_tnr)

        return tones_freqs, TNR, promi, t_tnr, time 
    
    else:
        return tones_freqs, tnr, prom, t_tnr
