# -*- coding: utf-8 -*-

# Local functions imports
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc
from mosqito.utils.conversion import db2amp

def tnr_ecma_freq(spectrum, freqs, prominence=True):
    """Computation of tone-to-noise ration according to ECMA-74, annex D.9
        The T-TNR value is calculated according to ECMA-TR/108

    Parameters
    ----------
    spectrum :numpy.array
        A complex frequency spectrum in dB.
    freqs : np.array
        Frequency axis. 
    prominence : boolean
        If True, the algorithm only returns the prominent tones, if False it returns all tones detected.
        Default is True.

    Output
    ------
    tones_freqs : array of float
        Frequency list of the detected tones.
    TNR : array of float
        TNR values for each detected tone.
    promi : array of bool
        Prominence criterion for each detected tone.
    t_tnr : array of float
        Global TNR value.
    """
             

    if spectrum.shape != freqs.shape :
        raise ValueError('Input spectrum and frequency axis must have the same shape')

    # Compute spectrum dB values
    spectrum_db = db2amp(spectrum, ref=2e-5)
            
    # compute TNR values
    tones_freqs, tnr, prom, t_tnr = _tnr_main_calc(spectrum_db, freqs)
  
    if prominence == False:
        return tones_freqs, tnr, prom, t_tnr
    else:
        return tones_freqs[prom], tnr[prom], prom[prom], t_tnr