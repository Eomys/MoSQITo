# -*- coding: utf-8 -*-

# Local imports
from mosqito.sq_metrics.tonality.prominence_ratio_ecma._pr_main_calc import _pr_main_calc
from mosqito.utils.conversion import db2amp


def pr_ecma_freq(spectrum, freqs, prominence=True):
    """Computation of prominence ratio according to ECMA-74, annex D.10
        The T-PR value is calculated according to ECMA-TR/108

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
    PR : array of float
        PR values for each detected tone.
    promi : array of bool
        Prominence criterion for each detected tone.
    t_PR : array of float
        Global PR value.
    """
    

    if spectrum.shape != freqs.shape :
        raise ValueError('Input spectrum and frequency axis must have the same shape')

    # Compute spectrum dB values
    spectrum_db = db2amp(spectrum, ref=2e-5)
                  
    # Compute PR values
    tones_freqs, pr, prom, t_pr = _pr_main_calc(spectrum_db, freqs)
 
    if prominence == False:
        return tones_freqs, pr, prom, t_pr
    else:
        return tones_freqs[prom], pr[prom], prom[prom], t_pr
