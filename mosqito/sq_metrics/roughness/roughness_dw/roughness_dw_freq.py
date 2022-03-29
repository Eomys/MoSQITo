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
        An amplitude or complex frequency spectrum [nperseg x nseg].
    freqs : np.array
        Frequency axis [nperseg] if identical for all the blocks, [nperseg x nseg] if not.

    Outputs
    -------
    R : numpy.array
        Roughness in [asper], dim [nseg].
    R_spec : numpy.array
        Specific roughness over bark axis, dim [47 bark x nseg].
    bark_axis : numpy.array
        Frequency axis in [bark], dim [nseg].

    """

    # Check input size coherence
    if len(spectrum) != len(freqs) :
        raise ValueError('Input spectrum and frequency axis must have the same size !')
        
    if spectrum.any()<0:
        raise ValueError('Input must be an amplitude spectrum (use np.abs() on complex spectrum).')

    # 1D spectrum
    if len(spectrum.shape) == 1:
        nperseg = len(spectrum)
        nseg = 1
        fs = int(nperseg * np.mean(freqs[1:] - freqs[:-1]))

    # 2D spectrum
    elif len(spectrum.shape) > 1:
        nperseg = spectrum.shape[0]
        nseg = spectrum.shape[1]
        # one frequency axis per block
        if len(freqs.shape) > 1:
            fs = int(nperseg * np.mean(freqs[0,1:] - freqs[0,:-1]))
        # one frequency axis for all the blocks
        elif len(freqs.shape) == 1: 
            fs = int(nperseg * np.mean(freqs[1:] - freqs[:-1]))
            freqs = np.tile(freqs, (nseg,1)).T
            
    # Initialization of the weighting functions H and g
    hWeight = _H_weighting(nperseg, fs)
    # Aures modulation depth weighting function
    gzi = _gzi_weighting(np.arange(1, 48, 1) / 2)

    R = np.zeros((nseg))
    R_spec = np.zeros((47, nseg))
    
    
    if len(spectrum.shape)>1:   
        for i in range(nseg):
            R[i], R_spec[:,i], bark_axis  = _roughness_dw_main_calc(spectrum[:,i], freqs[:,i], fs, gzi, hWeight)
    else:
        R, R_spec, bark_axis = _roughness_dw_main_calc(spectrum, freqs, fs, gzi, hWeight)

    return R, R_spec, bark_axis
