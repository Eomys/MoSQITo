# -*- coding: utf-8 -*-
"""
@date Created on Tue Mar 24 2020
@author martin_g for Eomys
"""
import sys
sys.path.append('..')

# Local application imports
from mosqito.functions.signal.load import load
from mosqito.functions.oct3filter.comp_third_spectrum import comp_third_spec


def load2oct3(is_stationary,file, calib=1):
    """Load .wav signal and output its third-octave band spectrum
    
    Parameters
    ----------
    is_stationary: boolean
        True if the signal is stationary, False if it is time-varying
    file : string
        full path to the signal file
    calib : float
        calibration factor for the signal to be in [pa]


    Outputs
    -------
    spec : numpy.ndarray
        Third octave band spectrum of signal sig [dB re.2e-5 Pa]
    fpref : numpy.ndarray
        Corresponding preferred third octave band center frequencies
    """

    # Load the signal from its file
    signal,fs = load(is_stationary, file, calib)
    
    # Compute third-octave spectrum
    spec_third, third_axis, time_axis = comp_third_spec(is_stationary, signal, fs)

    return spec_third, third_axis, time_axis