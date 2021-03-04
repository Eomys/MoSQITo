# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 10:41:09 2021

@author: wantysal
"""

import pytest

# Local application imports
from mosqito.functions.shared.load import load
from mosqito.functions.tonality_tnr_pr.comp_pr import comp_pr


@pytest.mark.pr  # to skip or run PR test
def test_pr():
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
        pr = comp_pr(signal[i]["is_stationary"], audio, fs, prominence=True)
