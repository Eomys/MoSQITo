# -*- coding: utf-8 -*-

# External import
import numpy as np
# Local functions imports
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc
from mosqito.utils.conversion import amp2db

def tnr_ecma_freq(spectrum, freqs,  prominence=True):
    """Computation of tone-to-noise ration according to ECMA-74, annex D.9
    for an amplitude or complex spectrum.
        The T-TNR value is calculated according to ECMA-TR/108

    Parameters
    ----------
    spectrum :numpy.array
        Amplitude or complex frequency spectrum [nperseg x nseg].
    freqs : np.array
        Frequency axis [nperseg x nseg] or [nperseg]. 
    prominence : boolean
        If True, the algorithm only returns the prominent tones, if False it returns all tones detected.
        Default is True.

    Output
    ------
    t_tnr : array of float
        Global TNR value.
    tnr : array of float
        TNR values for each detected tone.
    promi : array of bool
        Prominence criterion for each detected tone.
    tones_freqs : array of float
        Frequency list of the detected tones.
    """
             
    if len(spectrum) != len(freqs) :
        raise ValueError('Input spectrum and frequency axis must have the same size')
    
    # Compute spectrum dB values
    spectrum_db = amp2db(np.abs(spectrum), ref=2e-5)
            
    # compute TNR values
    tones_freqs, tnr, prom, t_tnr = _tnr_main_calc(spectrum_db, freqs)
  
    if prominence == False:
        return t_tnr, tnr, prom, tones_freqs
    else:
        return t_tnr, tnr[prom], prom[prom], tones_freqs[prom]
