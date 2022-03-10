# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np

# Local application imports
from mosqito.sound_level_meter.noct_spectrum._filter_bandwidth import _filter_bandwidth
from mosqito.sound_level_meter.noct_spectrum._n_oct_time_filter import _n_oct_time_filter
from mosqito.sound_level_meter.noct_spectrum._n_oct_freq_filter import _n_oct_freq_filter
from mosqito.sound_level_meter.noct_spectrum._center_freq import _center_freq


def noct_spectrum(sig, fs, fmin, fmax, freqs=[], n=3, G=10, fr=1000):
    """Compute nth-octave band spectrum

    Calculate the rms level of the signal "sig" sampled at freqency "fs"
    for each third octave band between "fc_min" and "fc_max".

    Parameters
    ----------
    sig : numpy.ndarray
        given signal either in time or frequency (complex) domain (dim [nb points, nb blocks])
    fs : float
        Sampling frequency [Hz]
    fmin : float
        Min frequency band [Hz]
    fmax : float
        Max frequency band [Hz]
    freqs : list
        List of input frequency if signal is a spectrum. Default is [].
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
    if len(sig.shape) > 1:
        spec = np.array([[] for i in range(sig.shape[0])])
    else :
        spec = [[]]
    for fc, alpha in zip(fc_vec, alpha_vec):
        if len(freqs) == 0:
            spec = np.c_[spec, _n_oct_time_filter(sig, fs, fc, alpha)]
        else:
            spec = np.c_[spec, _n_oct_freq_filter(sig, fs, fc, alpha)]
    
    spec = np.array(spec)
    if spec.shape[0] == 1:
        spec = spec[0,:]

    return spec, fpref
