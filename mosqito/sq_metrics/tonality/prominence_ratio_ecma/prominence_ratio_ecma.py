# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 14:25:04 2020

@author: wantysal
"""

# Standard library import
import numpy as np

# Local imports
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sq_metrics.tonality.prominence_ratio_ecma._pr_main_calc import (
    _pr_main_calc,
)


def prominence_ratio_ecma(is_stationary, signal, fs=None, freqs=[], prominence=True, overlap=0):
    """Computation of prominence ratio according to ECMA-74, annex D.10
        The T-PR value is calculated according to ECMA-TR/108

    Parameters
    ----------
    is_stationary : boolean
        True if the signal is stationary
    signal :numpy.array
        time signal values or frequency spectrum in dB
    fs : integer
        sampling frequency if signal given in time domain. Default is None
    freqs : np.array
        if signal is given in frequency domain, freqs is the correcponding frequency axis. Default is []
    prominence : boolean
        if True, the algorithm only returns the prominent tones, if False it returns all tones detected

    Output
    ------
    tones_freqs : array of float
        frequency of the detected tones
    PR : array of float
        PR values for each detected tone
    promi : array of bool
        prominence criterion for each detected tone
    t_PR : array of float
        global PR value, along time if is_stationary = False
    time  : array of float, only if is_stationary = False
        time axis
    """
    
    # if the input is a time signal, the spectrum computation is needed
    if len(freqs) == 0:
        if is_stationary == True:
            # compute db spectrum
            spectrum_db, freq_axis = spectrum(signal, fs, db=True)
        if is_stationary == False:
            if len(signal.shape) == 1:
                # Signal cut in frames of 500 ms along the time axis
                
                # Number of points within each frame according to the time resolution of 500ms
                n = int(0.5 * fs)
                # Overlappinf segment length
                noverlap = int(overlap *n)               
                # reshaping of the signal according to the overlap and time proportions
                sig, time = time_segmentation(signal, fs, nperseg=n, noverlap=noverlap, is_ecma=False)
                sig = sig.T
                nb_frame = sig.shape[0]
                spectrum_db, freq_axis = spectrum(sig, fs, db=True)
            else:
                nb_frame = signal.shape[0]
                time = np.linspace(0, signal.shape[1]/fs, num=nb_frame)
                
                spectrum_db, freq_axis = spectrum(sig, fs, db=True)
    else:
        if signal.shape != freqs.shape :
            raise ValueError('Input spectrum and frequency axis must have the same shape')
        else :
            spectrum_db = signal
            freq_axis = freqs
            
            
    # compute tnr values
    tones_freqs, pr, prom, t_pr = _pr_main_calc(spectrum_db, freq_axis)
 
            
    if (type(pr[0])== np.ndarray) & (is_stationary == False):
        if len(freqs) == 0:
            # Retore the results in a time vs frequency array
            freqs = np.logspace(np.log10(90), np.log10(11200), num=1000)
            PR = np.empty((len(freqs), nb_frame))
            PR.fill(np.nan)
            promi = np.empty((len(freqs), nb_frame), dtype=bool)
            promi.fill(False)
            
            for t in range(nb_frame):
                for f in range(len(tones_freqs[t])):
                    ind = np.argmin(np.abs(freqs - tones_freqs[t][f]))
                    if prominence == False:
                        PR[ind, t] = pr[t][f]
                        promi[ind, t] = prom[t][f]
                    if prominence == True:
                        if prom[t][f] == True:
                            PR[ind, t] = pr[t][f]
                            promi[ind, t] = prom[t][f]

            t_pr = np.ravel(t_pr)

        return tones_freqs, PR, promi, t_pr, time 
    
    else:
        if prominence == False:
            return tones_freqs, pr, prom, t_pr
        else:
            return tones_freqs[prom], pr[prom], prom[prom], t_pr
