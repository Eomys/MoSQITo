# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:51:19 2020

@author: wantysal
"""


# Standard library import
import numpy as np

# Local functions imports
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc


def tone_to_noise_ecma(is_stationary, signal, fs=None, freqs=[], prominence=True, overlap=0):
    """Computation of tone-to-noise ration according to ECMA-74, annex D.9
        The T-TNR value is calculated according to ECMA-TR/108

    Parameters
    ----------
    is_stationary : boolean
        True if the signal is stationary
    signal :numpy.array
        time signal values or frequency spectrum in dB
    fs : integer
        sampling frequency if signal given in time domain. Default is None.
    freqs : np.array
        if signal is given in frequency domain, freqs is the correcponding frequency axis. Default is []
    prominence : boolean
        if True, the algorithm only returns the prominent tones, if False it returns all tones detected

    Output
    ------
    tones_freqs : array of float
        frequency of the detected tones
    TNR : array of float
        TNR values for each detected tone
    promi : array of bool
        prominence criterion for each detected tone
    t_tnr : array of float
        global TNR value, along time if is_stationary = False
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
            
                spectrum_db, freq_axis = spectrum(signal, fs, db=True)
            

    else:
        if signal.shape != freqs.shape :
            raise ValueError('Input spectrum and frequency axis must have the same shape')
        else :
            spectrum_db = signal
            freq_axis = freqs
            
            
    # compute tnr values
    tones_freqs, tnr, prom, t_tnr = _tnr_main_calc(spectrum_db, freq_axis)

            
    if (type(tnr[0])== np.ndarray) & (is_stationary == False):
        if len(freqs) == 0:
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
        if prominence == False:
            return tones_freqs, tnr, prom, t_tnr
        else:
            return tones_freqs[prom], tnr[prom], prom[prom], t_tnr
