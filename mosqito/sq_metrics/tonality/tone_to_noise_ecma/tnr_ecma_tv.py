# -*- coding: utf-8 -*-

# Standard library import
import numpy as np

# Local functions imports
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc


def tnr_ecma_tv(signal, fs, prominence=True, overlap=0.5):
    """Computation of tone-to-noise ration according to ECMA-74, annex D.9
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
    
    if len(signal.shape) == 1:
   
        # Number of points within each segment according to the time resolution of 500ms
        nperseg = int(0.5 * fs)
        # Overlapping segment length
        noverlap = int(overlap *nperseg)               
        # reshaping of the signal according to the overlap and time proportions
        sig, time = time_segmentation(signal, fs, nperseg=nperseg, noverlap=noverlap, is_ecma=False)
        sig = sig.T
        nseg = sig.shape[0]
    
    else:
        nseg = signal.shape[0]
        time = np.linspace(0, signal.shape[1]/fs, num=nseg)

    
    # Spectrum computation
    spectrum_db, freq_axis = spectrum(sig, fs, db=True)
        
    # Compute tnr values
    tones_freqs, tnr, prom, t_tnr = _tnr_main_calc(spectrum_db, freq_axis)

            
    # Retore the results in a time vs frequency array
    freqs = np.logspace(np.log10(90), np.log10(11200), num=1000)
    TNR = np.empty((len(freqs), nseg))
    TNR.fill(np.nan)
    promi = np.empty((len(freqs), nseg), dtype=bool)
    promi.fill(np.nan)

    for t in range(nseg):
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
    
