# -*- coding: utf-8 -*-

# Local functions imports
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc


def tnr_ecma_st(signal, fs, prominence=True):
    """Computation of tone-to-noise ration according to ECMA-74, annex D.9
    for a stationary signal.
        The T-TNR value is calculated according to ECMA-TR/108

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
    t_tnr : array of float
        global TNR value, along time if is_stationary = False
    tnr : array of float
        TNR values for each detected tone
    promi : array of bool
        prominence criterion for each detected tone
    tones_freqs : array of float
        frequency of the detected tones
    """

    # Compute db spectrum
    spectrum_db, freq_axis = spectrum(signal, fs, db=True)

    # Compute tnr values
    tones_freqs, tnr, prom, t_tnr = _tnr_main_calc(spectrum_db, freq_axis)
    prom = prom.astype(bool)

    if prominence == False:
        return t_tnr, tnr, prom, tones_freqs
    else:
        return t_tnr, tnr[prom], prom[prom], tones_freqs[prom]
