# -*- coding: utf-8 -*-
"""
@date Created on Fri Mar 13 2020
@author martin_g for Eomys
"""

# Standard library imports
import numpy as np

# Local application imports
from mosqito.functions.oct3filter.oct3level import oct3level
from mosqito.functions.oct3filter.center_freq import center_freq


def comp_noct_spectrum(sig, fs, fmin, fmax, n=3, G=10, fr=1000, dec_factor=24):
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
        Third octave band spectrum of signal sig [dB re.2e-5 Pa]
    fpref : numpy.ndarray
        Corresponding preferred third octave band center frequencies
    """

    # Check for high fc/fs causing filter design issue [ref needed]
    if fc < fs / 200:
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc > fs / 200"""
        )

    # Check for Nyquist-Shannon criteria
    if max(fc) > 0.88 * (fs / 2):
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc <= 0.88 * (fs / 2)."""
        )

    # Calculation of the rms level of the signal in each band
    for fc in f_exact:
        spec[i, :] = oct3level(sig, fs, fc, sig_type, dec_factor)
        i += 1

    spec = 20 * np.log10((spec + 1e-12) / (2 * 10 ** -5))
    return spec, fpref
