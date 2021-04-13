# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 10:39:49 2021

@author: wantysal
"""

import pytest

# Local application imports
from mosqito.functions.shared.load import load
from mosqito.functions.tonality_tnr_pr.comp_tnr import comp_tnr


@pytest.mark.tnr  # to skip or run PR test
def test_tnr():
    """Test function for the prominence ratio calculation of an audio signal

    Validation function for the Audio_signal class "comp_tnr" method with signal array
    as input. The input signals are generated using audacity.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    # Test signal as input for prominence ratio calculation
    # signals generated using audacity : white noise + tones at 200 and 2000 Hz
    # the first one is stationary, the second is time-varying
    signal = []

    signal.append(
        {
            "is_stationary": True,
            "tones freq": [200, 2000],
            "data_file": r"mosqito\tests\tonality_tnr_pr\white_noise_442_1768_Hz_stationary.wav",
        }
    )

    signal.append(
        {
            "is_stationary": False,
            "data_file": r"mosqito\tests\tonality_tnr_pr\white_noise_442_1768_Hz_varying.wav",
        }
    )

    for i in range(len(signal)):
        # Load signal
        audio, fs = load(signal[i]["is_stationary"], signal[i]["data_file"])
        # Compute tone-to-noise ratio
        tnr = comp_tnr(signal[i]["is_stationary"], audio, fs, prominence=True)
