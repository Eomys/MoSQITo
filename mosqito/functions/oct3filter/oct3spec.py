# -*- coding: utf-8 -*-
"""
@date Created on Fri Mar 13 2020
@author martin_g for Eomys
"""

# Standard library imports
import numpy as np

# Local application imports
from mosqito.functions.oct3filter.oct3level import oct3level


def oct3spec(sig, fs, fc_min=20, fc_max=20000, sig_type="stationary", dec_factor=24):
    """Calculate third-octave band spectrum

    Calculate the rms level of the signal "sig" sampled at freqency "fs"
    for each third octave band between "fc_min" and "fc_max".

    Parameters
    ----------
    sig : numpy.ndarray
        time signal [Pa]
    fs : float
        Sampling frequency [Hz]
    fc_min : float
        Filter center frequency of the lowest 1/3 oct. band [Hz]
    fc_max : float
        Filter center frequency of the highest 1/3 oct. band [Hz]
    out_format : str
        Format of the output data ("rms" by default or "time")
        corresponding respectively to a vector of overall rms values
        per third octave band or a matrix (dim [freq, time]) filtered
        time signals per third octave band
    sig_type : str
        Type of signal ('stationary' or 'time-varying'), influences the
        format of the output data corresponding respectively to a vector
        of overall rms values per third octave band or a matrix
        (dim [freq, time]) filtered time signals per third octave band
    fs_level : int
        RMS vs. time (pseudo-)sampling frequency.

    Outputs
    -------
    spec : numpy.ndarray
        Third octave band spectrum of signal sig [dB re.2e-5 Pa]
    fpref : numpy.ndarray
        Corresponding preferred third octave band center frequencies
    """

    # TODO: control that fc_min and fc_max are in the right range
    # TODO: smarter management of the frequencies by using the ANSI
    #       definitions (with base 10 and base 2 options)

    # Définition of the range of preferred filter center frequency
    fpref = np.array(
        [
            25,
            31.5,
            40,
            50,
            63,
            80,
            100,
            125,
            160,
            200,
            250,
            315,
            400,
            500,
            630,
            800,
            1000,
            1250,
            1600,
            2000,
            2500,
            3150,
            4000,
            5000,
            6300,
            8000,
            10000,
            12500,
        ]
    )

    fexact = np.array(
        [
            25.119,
            31.623,
            39.811,
            50.119,
            63.096,
            79.433,
            100,
            125.89,
            158.49,
            199.53,
            251.19,
            316.23,
            398.11,
            501.19,
            630.96,
            794.33,
            1000,
            1258.9,
            1584.9,
            1995.3,
            2511.9,
            3162.3,
            3981.1,
            5011.9,
            6309.6,
            7943,
            10000,
            12589,
        ]
    )

    fexact = fexact[fpref >= fc_min]
    fpref = fpref[fpref >= fc_min]
    fexact = fexact[fpref <= fc_max]
    fpref = fpref[fpref <= fc_max]

    # Calculation of the rms level of the signal in each band
    if sig_type == "stationary":
        spec = np.zeros((len(fexact), 1))
    else:
        n_level = int(np.ceil(sig.shape[0] / dec_factor))
        spec = np.zeros((len(fexact), n_level))
    i = 0
    for fc in fexact:
        spec[i, :] = oct3level(sig, fs, fc, sig_type, dec_factor)
        i += 1

    spec = 20 * np.log10((spec + 1e-12) / (2 * 10 ** -5))
    return spec, fpref
