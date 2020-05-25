# -*- coding: utf-8 -*-
"""
@date Created on Thu Mar 26 2020
@author martin_g for Eomys
"""

# Temporary for testing purpose
import sys
sys.path.append('D:/scripts/github/MoSQITo/')
from scipy.io import wavfile
import matplotlib.pyplot as plt
from mosqito.generic.oct3spec import oct3spec
import time

# Standard library imports
import math

# Third party imports
import numpy as np
from scipy import signal

# Local application imports
from mosqito.loudness.loudness_zwicker_shared import calc_main_loudness
from mosqito.loudness.loudness_zwicker_nonlinear_decay import calc_nl_loudness
from mosqito.loudness.loudness_zwicker_shared import calc_slopes
from mosqito.loudness.loudness_zwicker_temporal_weighting import loudness_zwicker_temporal_weighting

# Global variables
#Sampling rate to which third-octave-levels are downsampled
sr_level = 2000
# Sampling rate to which output/total summed loudness is downsampled
sr_loudness = 500

def loudness_from_levels(third_octave_levels, field_type):
    """TODO: descr

    Parameters
    ----------
    third_octave_levels : numpy.ndarray
        time signal sampled at 48 kHz [pa]
    coeff : numpy.ndarray
        filter coeeficients
    gain : float
        filter gain

    Outputs
    -------
    signal_filt : numpy.ndarray
        filtered time signal  
    spec_loudness : numpy.ndarray
        specific loudness
    """
    #
    # Sampling rate to which third-octave-levels are downsampled
    sample_rate_level = sr_level
    #
    # Calculate core loudness
    num_sample_level = np.shape(third_octave_levels)[1]
    core_loudness = np.zeros((21, num_sample_level))
    for i in np.arange(num_sample_level-1):
        core_loudness[:,i] = calc_main_loudness(third_octave_levels[:,i], field_type)
    #
    # Nonlinearity
    core_loudness = calc_nl_loudness(core_loudness, sample_rate_level)
    #
    # Calculation of specific loudness
    loudness = np.zeros(np.shape(core_loudness)[1])
    spec_loudness = np.zeros((240,np.shape(core_loudness)[1]))
    for i_time in np.arange(np.shape(core_loudness)[1]):
        loudness[i_time], spec_loudness[:,i_time] = calc_slopes(core_loudness[:,i_time])
    #
    # temporal weigthing
    filt_loudness = loudness_zwicker_temporal_weighting(loudness, sample_rate_level)
    #
    # Decimation and return
    dec_factor = int(sr_level/sr_loudness)
    return filt_loudness[::dec_factor], spec_loudness[:,::dec_factor]
        
def loudness_zwicker_time(signal, fs, field_type="free"):
    """Calculate Zwicker-loudness for time-varying signals

    Calculate the acoustic loudness according to Zwicker method for
    time-varying signals.
    Normatice reference:
        DIN 45631/A1:2010
        ISO 532-1:2017 (method 2)
    The code is based on C program source code published alongside
    with ISO 532-1 standard. 
    Note that for reasons of normative continuity, as defined in the
    preceeding standards, the method is in accordance with 
    ISO 226:1987 equal loudness contours (instead of ISO 226:2003)

    Parameters
    ----------
    signal : numpy.ndarray
        time signal [pa]
    fs : int
        Signal sampling frequency
    field_type : str
        Type of soundfield corresponding to signal ("free" by 
        default or "diffuse")

    Outputs
    -------
    N : float
        Calculated loudness [sones]
    N_specific : numpy.ndarray
        Specific loudness [sones/bark]
    bark_axis : numpy.ndarray
        Corresponding bark axis
    """
    dec_factor_level = int(fs / sr_level)
    # num_sample_level = sig.shape[0] / dec_factor_level
    signal = 2*2**0.5 * signal / (2**15-1)
    third_octave_levels, freq = oct3spec(signal, fs, fc_min=25, fc_max=12500, sig_type='time_varying', dec_factor=24)
    third_octave_levels = 20 * np.log10(third_octave_levels / (2*10**-5))
    loudness, spec_loudness = loudness_from_levels(third_octave_levels, field_type)
    return loudness, spec_loudness

# test de la fonction
if __name__ == "__main__":
    file = "./mosqito/tests/data/ISO_532-1/Test signal 13 (combined tone pulses 1 kHz).wav"
    fs, sig = wavfile.read(file)
    # sig = 2*2**0.5 * sig / (2**15-1) # for ISO .wav
    # sig = sig / (2**15-1) # for genesis .wav
    loudness, spec_loudness = loudness_zwicker_time(sig, fs, 'free')

    plt.subplot(211)
    plt.plot(loudness,label="MoSQITo")
    N_iso = np.genfromtxt("./mosqito/tests/data/ISO_532-1/test_signal_13.csv", skip_header=1)
    plt.plot(N_iso,label="Iso")
    plt.legend()

    plt.subplot(212)
    plt.plot(spec_loudness[84,:],label="MoSQITo")
    N_iso = np.genfromtxt("./mosqito/tests/data/ISO_532-1/test_signal_13_spec.csv", skip_header=1)
    plt.plot(N_iso[1:],label="Iso")
    plt.legend()
    
    plt.show()
