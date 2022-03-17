# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 11:02:18 2022

@author: wantysal
"""

# Standard library import
import numpy as np

# Local application imports
from mosqito.sound_level_meter.noct_spectrum._filter_bandwidth import _filter_bandwidth
from mosqito.sound_level_meter.noct_spectrum._n_oct_freq_filter import _n_oct_freq_filter
from mosqito.sound_level_meter.noct_spectrum._center_freq import _center_freq


def noct_synthesis(spectrum, freqs, fs, fmin, fmax, n=3, G=10, fr=1000):
    """Adapt input spectrum to nth-octave band spectrum

    Convert the input spectrum to third-octave band spectrum
    between "fc_min" and "fc_max".

    Parameters
    ----------
    spectrum : numpy.ndarray
        input complex spectrum (dim [nb blocks, nb points])
    freqs : list
        list of input frequency 
    fmin : float
        Min frequency band [Hz]
    fmax : float
        Max frequency band [Hz]
    n : int
        number of bands pr octave
    G : int
        System for specifying the exact geometric mean frequencies.
        Can be base 2 or base 10
    fr : int
        Reference frequency. Shall be set to 1 kHz for audible frequency
        range, to 1 Hz for infrasonic range (f < 20 Hz) and to 1 MHz for
        ultrasonic range (f > 31.5 kHz)

    Outputs
    -------
    spec : numpy.ndarray
        Third octave band spectrum of signal sig [dB re.2e-5 Pa]
    fpref : numpy.ndarray
        Corresponding preferred third octave band center frequencies
    """

    # Get filters center frequencies
    fc_vec, fpref = _center_freq(fmin=fmin, fmax=fmax, n=n, G=G, fr=fr)

    # Compute the filters bandwidth
    alpha_vec = _filter_bandwidth(fc_vec, n=n)

    # Calculation of the rms level of the time signal in each band
    if len(spectrum.shape) > 1:
        spec = np.array([[] for i in range(spectrum.shape[0])])
    else :
        spec = [[]]
    for fc, alpha in zip(fc_vec, alpha_vec):
        spec = np.c_[spec, _n_oct_freq_filter(spectrum, fs, fc, alpha)]
    
    spec = np.array(spec)
    if spec.shape[0] == 1:
        spec = spec[0,:]

    return spec, fpref
