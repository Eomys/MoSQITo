# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np

# Local application imports
from mosqito.functions.noct_spectrum.filter_bandwidth import filter_bandwidth
from mosqito.functions.noct_spectrum.n_oct_filter import n_oct_filter
from mosqito.functions.noct_spectrum.center_freq import center_freq


def comp_noct_spectrum(sig, fs, fmin, fmax, n=3, G=10, fr=1000):
    """Compute nth-octave band spectrum

    Calculate the rms level of the signal "sig" sampled at freqency "fs"
    for each third octave band between "fc_min" and "fc_max".

    Parameters
    ----------
    sig : numpy.ndarray
        time signal (dim [nb points, nb blocks])
    fs : float
        Sampling frequency [Hz]
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
        Third octave band spectrum of signal sig (units: Pascals [Pa]).
    fpref : numpy.ndarray
        Corresponding preferred third octave band center frequencies
    """

    # Get filters center frequencies
    fc_vec, fpref = center_freq(fmin=fmin, fmax=fmax, n=n, G=G, fr=fr)

    # Compute the filters bandwidth
    alpha_vec = filter_bandwidth(fc_vec, n=n)

    # Calculation of the rms level of the signal in each band
    spec = []
    for fc, alpha in zip(fc_vec, alpha_vec):
        spec.append(n_oct_filter(sig, fs, fc, alpha))

    return np.array(spec), fpref
