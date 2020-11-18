# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 17:00:31 2020

@author: wantysal
"""
import sys
sys.path.append('../../..')

#Standard imports
import numpy as np
import matplotlib.pyplot as plt
import pytest

# Local application imports
from mosqito.Classes.Audio_signal import Audio_signal


# a 1kHz pure tone has a sharpness of 1 acum
file = r"C:\Users\pc\Documents\Salomé\MoSQITo_oo\mosqito\functions\sharpness\1000Hz.wav"
# file = r"C:\Users\pc\Documents\Salomé\MoSQITo_oo\mosqito\tests\loudness\data\ISO_532-1\Test signal 5 (pinknoise 60 dB).wav"

audio = Audio_signal()
audio.load_wav(True, file, calib = 1)
audio.comp_third_oct()
audio.comp_loudness()
audio.comp_sharpness()
audio.plot_sharpness()
  


# pytest.mark.parametrize allows to execute a test for different data : see http://doc.pytest.org/en/latest/parametrize.html
@pytest.mark.sharpness  # to skip or run only loudness zwicker stationary tests
@pytest.mark.parametrize(
    "signal",
    [
        {
            "data_file": "mosqito/tests/sharpness/data/",
            "S": 1.00,
        },
        {
            "data_file": ,
            "S": ,
        },
        {
            "data_file": "mosqito/tests/sharpness/data/",
            "S": ,
        },
        {
            "data_file": "mosqito/tests/sharpness/data/",
            "S": ,
        },
    ],
)

@pytest.mark.loudness_zwst  # to skip or run only loudness zwicker stationary tests
def test_sharpness_din_wav(signal):
    """Test function for the script calc_sharpness_din
    
    Test function for the script sharpness_din with
    .wav file as input. The input file is provided by DIN 45692 annex 
    B3, the compliance is assessed according to section 5.1 of the 
    standard. 

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    # Test signal as input for sharpness
    # (from ISO 532-1 annex B3)
    audio = Audio_signal()
    # Load signal and compute third octave band spectrum
    audio.load_wav(True, signal["data_file"], calib=2 * 2 ** 0.5)
    audio.comp_third_oct()
    # Compute Loudness
    audio.comp_loudness()
    N = audio.N
    N_specific = audio.N_specific
    # Compute sharpness
    audio.comp_sharpness()
    S = audio.S_din
    # Check DIN 45692 compliance
    assert check_compliance(N, N_specific, S, signal)


def check_compliance(N, N_specific,S, iso_ref):
    """Check the compliance of loudness calc. to ISO 532-1

    Check the compliance of the input data N and N_specific
    to section 5.1 of ISO 532-1 by using the reference data
    described in dictionary iso_ref.

    Parameters
    ----------
    N : float
        Calculated loudness [sones]
    N_specific : numpy.ndarray
        Specific loudness [sones/bark]
    S : float
        Calculated sharpness [acum]
    iso_ref : dict
        {
            "data_file": <Path to reference input signal>,
            "S": <Reference sharpness value>,
        }
        Dictionary containing link to ref. data

    Outputs
    -------
    tst : bool
        Compliance to the reference data
    """
    # Load ISO reference outputs
    S_iso = iso_ref["S"]
  
    
    # Test for DIN 45692 comformance (section 5.1)   
    tst = (
        S >= S_iso * 0.95
        and S <= S_iso * 1.05
        and S >= S_iso - 0.05
        and S <= S_iso + 0.05
    )
       
        
    # Compliance print
    if tst:
        print("S = " + str(S) + " acum, DIN ref. " + str(S_iso) + " acum)")
        print('Test passed (5% relative tolerance and 0.05 absolute tolerance not exceeded)')
    else:
        print("S = " + str(S) + " acum, DIN ref. " + str(S_iso) + " acum)")
        print('Test not passed')
    
    
    return tst


# test de la fonction
if __name__ == "__main__":
    test_sharpness_din_wav()