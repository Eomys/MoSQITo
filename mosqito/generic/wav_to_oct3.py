# -*- coding: utf-8 -*-
"""
@date Created on Tue Mar 24 2020
@author martin_g for Eomys
"""

# Standard library imports

# Third party imports
import numpy as np
from scipy.io import wavfile

# Local application imports
from mosqito.generic.oct3spec import oct3spec
from mosqito.generic.calc_third_octave_levels import calc_third_octave_levels


def wav_to_oct3(file, calib=1, out_type='overall'):
    """Load .wav signal and output its third-octave band spectrum

    Parameters
    ----------
    file : string
        full path to the signal file
    calib : float
        calibration factor for the signal to be in [pa]
    out_type : str
        determine the format of the output
        - overall: overall rms value per third octave band
        - time: rms value per third octave versus time (temporal
            resolution = 0.5ms)
        - time_iso: squared and smoothed value per third octave 
            versus time, ISO 532-1 implementation (temporal
            resolution = 0.5ms)

    Outputs
    -------
    spec : numpy.ndarray
        Third octave band spectrum of signal sig [pa, rms]
    fpref : numpy.ndarray
        Corresponding preferred third octave band center frequencies
    """

    # TODO: Manage float32 wav file format
    # TODO: Manage fs != 48000 Hz

    fs, sig = wavfile.read(file)
    if isinstance(sig[0], np.int16):
        sig = calib * sig / (2 ** 15 - 1)
    elif isinstance(sig[0], np.int32):
        sig = calib * sig / (2 ** 31 - 1)
    if out_type ==  'overall':
        spec, freq = oct3spec(sig, fs, 25, 12500, sig_type='stationary')
    elif out_type == 'time':
        dec_factor = int(fs / 2000)
        spec, freq = oct3spec(sig, fs, 25, 12500, sig_type='time_varying', dec_factor=24)
    elif out_type == 'time_iso':
        dec_factor = int(fs / 2000)
        spec = calc_third_octave_levels(sig,dec_factor)
        freq = np.array(
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
    return spec, freq
