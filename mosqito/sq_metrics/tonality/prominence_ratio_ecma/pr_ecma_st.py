# -*- coding: utf-8 -*-

# Local imports
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sq_metrics.tonality.prominence_ratio_ecma._pr_main_calc import (
    _pr_main_calc,
)


def pr_ecma_st(signal, fs, prominence=True):
    """Computation of prominence ratio according to ECMA-74, annex D.10
    for a stationary signal.
        The T-PR value is calculated according to ECMA-TR/108

    Parameters
    ----------
    signal :numpy.array
        A stationary signal in [Pa].
    fs : integer
        Sampling frequency.
    prominence : boolean
        If True, the algorithm only returns the prominent tones, if False it returns all tones detected.
        Default is True.

    Output
    ------
    t_pr : array of float
        Global PR value along time.
    pr : array of float
        PR values for each detected tone.
    promi : array of bool
        Prominence criterion for each detected tone.
    tones_freqs : array of float
        Frequency list of the detected tones.
    """

    # Compute db spectrum
    spectrum_db, freq_axis = spectrum(signal, fs, db=True)

    # Compute PR values
    tones_freqs, pr, prom, t_pr = _pr_main_calc(spectrum_db, freq_axis)
    prom = prom.astype(bool)

    if prominence == False:
        return t_pr, pr, prom, tones_freqs
    else:
        return t_pr, pr[prom], prom[prom], tones_freqs[prom]
