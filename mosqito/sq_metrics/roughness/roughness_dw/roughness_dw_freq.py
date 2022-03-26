# -*- coding: utf-8 -*-

# Standard imports
import numpy as np

# Local imports
from mosqito.sq_metrics.roughness.roughness_dw._roughness_dw_main_calc import _roughness_dw_main_calc 
from mosqito.sq_metrics.roughness.roughness_dw._gzi_weighting import _gzi_weighting
from mosqito.sq_metrics.roughness.roughness_dw._H_weighting import _H_weighting


def roughness_dw_freq(spectrum, freqs):
    """Roughness calculation of a spectrum sampled at 48kHz.

    The code is based on the algorithm described in "Psychoacoustical roughness:
    implementation of an optimized model" by Daniel and Weber in 1997.
    The roughness model consists of a parallel processing structure that is made up
    of successive stages and calculates intermediate specific roughnesses R_spec,
    which are summed up to determine the total roughness R.

    Parameters
    ----------
    spectrum :numpy.array
        A complex frequency spectrum.
    freqs : np.array
        Frequency axis.

    Outputs
    -------
    R : numpy.array
        Roughness in [asper].
    R_spec : numpy.array
        Specific roughness over bark axis.
    bark_axis : numpy.array
        Frequency axis in [bark].

    """

    # Check input size coherence
    if spectrum.shape != freqs.shape :
        raise ValueError('Input spectrum and frequency axis must have the same shape')


    if len(spectrum.shape)>1:
        n = spectrum.shape[1]
        nb_frame = spectrum.shape[0]
        fs = int(n * np.mean(freqs[0,1:] - freqs[0,:-1]))

    else:
        n = len(spectrum)
        nb_frame = 1
        fs = int(n * np.mean(freqs[1:] - freqs[:-1]))
            
    # Initialization of the weighting functions H and g
    hWeight = _H_weighting(n, fs)
    # Aures modulation depth weighting function
    gzi = _gzi_weighting(np.arange(1, 48, 1) / 2)

    R = np.zeros((nb_frame))
    R_spec = np.zeros((nb_frame, 47))
    if len(spectrum.shape)>1:   
        for i_frame in range(nb_frame):
            R[i_frame], R_spec[i_frame,:], bark_axis  = _roughness_dw_main_calc(spectrum[i_frame,:], freqs, fs, gzi, hWeight)
    else:
        R, R_spec, bark_axis = _roughness_dw_main_calc(spectrum, freqs, fs, gzi, hWeight)

    return R, R_spec, bark_axis
