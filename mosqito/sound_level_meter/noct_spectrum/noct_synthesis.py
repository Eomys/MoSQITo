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


def noct_synthesis(spectrum, freqs, fmin, fmax, n=3, G=10, fr=1000):
    """Adapt input spectrum to nth-octave band spectrum

    Convert the input spectrum to third-octave band spectrum
    between "fc_min" and "fc_max".

    Parameters
    ----------
    spectrum : numpy.ndarray
        amplitude rms of the one-sided spectrum of the signal
        (dim [nseg, nperseg])
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

    nband = len(fpref)

    if len(spectrum.shape) > 1:
        nseg = spectrum.shape[0]
        spec = np.zeros((nseg, nband))
    else:
        nseg = 1
        spec = np.zeros((nband))

    # Frequency resolution
    # df = freqs[1:] - freqs[:-1]
    # df = np.concatenate((df, [df[-1]]))

    # Get upper and lower frequencies
    fu = fc_vec * 2**(1/(2*n))
    fl = fc_vec / 2**(1/(2*n))

    for s in range(nseg):
        for i in range(nband):
            # index of the frequencies within the band
            idx = np.where((freqs >= fl[i]) & (freqs < fu[i]))

            if len(spectrum.shape) > 1:
                spec[s, i] = np.sqrt(
                    np.sum(np.power(np.abs(spectrum[i, idx]), 2)))
            else:
                spec[i] = np.sqrt(np.sum(spectrum[idx]**2))

    return spec, fpref
