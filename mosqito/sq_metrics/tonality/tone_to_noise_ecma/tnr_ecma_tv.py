# -*- coding: utf-8 -*-

# Standard library import
import numpy as np

# Local functions imports
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc


def tnr_ecma_tv(signal, fs, prominence=False, overlap=0):
    """Computation of tone-to-noise ration according to ECMA-74, annex D.9
    for a time varying signal.
        The T-TNR value is calculated according to ECMA-TR/108

    Parameters
    ----------
    signal :numpy.array
        A time varying signal in [Pa].
    fs : integer
        Sampling frequency.
    prominence : boolean
        If True, the algorithm only returns the prominent tones, if False it returns all tones detected.
        Default is True.
    overlap : float
        Overlapping parameter for the time frames of 500ms. Default is 0.5.

    Output
    ------
    t_tnr : array of float
        global TNR value, along time if is_stationary = False
    tnr : array of float
        TNR values for each detected tone
    promi : array of bool
        prominence criterion for each detected tone
    tones_freqs : array of float
        frequency of the detected tones
    time  : array of float, only if is_stationary = False
        time axis
    """
    
    if len(signal.shape) == 1:
      
        # Number of points within each frame according to the time resolution of 500ms
        nperseg = int(0.5 * fs)
        # Overlappinf segment length
        noverlap = int(overlap * nperseg)               
        # Time segmentation of the signal
        sig, time = time_segmentation(signal, fs, nperseg=nperseg, noverlap=noverlap, is_ecma=False)
        # Number of segments
        nseg = sig.shape[1] 
        # Spectrum computation
        spectrum_db, freq_axis = spectrum(sig, fs, db=True)
      
    else:
        nseg = signal.shape[1]
        time = np.linspace(0, signal.shape[0]/fs, num=nseg)
        
        # Compute spectrum
        spectrum_db, freq_axis = spectrum(sig, fs, db=True)
            
            
    # compute tnr values
    tones_freqs, tnr_, prom, t_tnr = _tnr_main_calc(spectrum_db, freq_axis)
 
            
    # Retore the results in a time vs frequency array
    freqs = np.logspace(np.log10(90), np.log10(11200), num=1000)
    tnr = np.empty((len(freqs), nseg))
    tnr.fill(np.nan)
    promi = np.empty((len(freqs), nseg), dtype=bool)
    promi.fill(False)
    
    for t in range(nseg):
        for f in range(len(tones_freqs[t])):
            ind = np.argmin(np.abs(freqs - tones_freqs[t][f]))
            if prominence == False:
                tnr[ind, t] = tnr_[t][f]
                promi[ind, t] = prom[t][f]
            if prominence == True:
                if prom[t][f] == True:
                    tnr[ind, t] = tnr_[t][f]
                    promi[ind, t] = prom[t][f]

    t_tnr = np.ravel(t_tnr)

    return t_tnr, tnr, promi, freqs, time     
