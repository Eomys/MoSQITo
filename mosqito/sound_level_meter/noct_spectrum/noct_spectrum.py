# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np

# Local application imports
from mosqito.sound_level_meter.noct_spectrum._filter_bandwidth import _filter_bandwidth
from mosqito.sound_level_meter.noct_spectrum._n_oct_filter import _n_oct_filter
from mosqito.sound_level_meter.noct_spectrum._center_freq import _center_freq


def noct_spectrum(sig, fs, fmin, fmax, n=3, G=10, fr=1000):
    """Compute nth-octave band spectrum

    Calculate the rms level of the signal "sig" sampled at freqency "fs"
    for each third octave band between "fc_min" and "fc_max".

    Parameters
    ----------
    sig : numpy.ndarray
        A time signal array with size (nperseg, nseg).
    fs : float
        Sampling frequency [Hz]
    fmin : float
        Min frequency band [Hz]
    fmax : float
        Max frequency band [Hz]
    n : int
        Number of bands pr octave
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
<<<<<<< HEAD
        Third octave band spectrum of signal sig (units: Pascals [Pa]).
=======
        The third octave band spectrum of signal sig with size (nfreq, nseg)
>>>>>>> ad054c17c80ccea5874344f38a135c8fe1315a12
    fpref : numpy.ndarray
        Corresponding preferred third octave band center frequencies
    """

    # 1-dimensional array to 2-dimensional array with size (nperseg, 1)
    if sig.ndim == 1:
        sig = sig[:, np.newaxis]

    # Get filters center frequencies
    fc_vec, fpref = _center_freq(fmin=fmin, fmax=fmax, n=n, G=G, fr=fr)

    # Compute the filters bandwidth
    alpha_vec = _filter_bandwidth(fc_vec, n=n)

    # Calculation of the rms level of the signal in each band
    spec = []
    for fc, alpha in zip(fc_vec, alpha_vec):
        spec.append(_n_oct_filter(sig, fs, fc, alpha))

    return np.array(spec), fpref
