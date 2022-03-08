# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 10:41:09 2021

@author: wantysal
"""

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
        )


# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import prominence_ratio_ecma


@pytest.mark.pr  # to skip or run PR test
def test_pr_ecma():
    """Test function for the prominence ratio calculation of an audio signal

    Validation function for the Audio_signal class "tone_to_noise_ecma" method with signal array
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
            "data_file": "tests/input/white_noise_442_1768_Hz_stationary.wav",
        }
    )

    signal.append(
        {
            "is_stationary": False,
            "data_file": "tests/input/white_noise_442_1768_Hz_varying.wav",
        }
    )

    for i in range(len(signal)):
        # Load signal
        audio, fs = load(signal[i]["data_file"])
        # Compute tone-to-noise ratio
        pr = prominence_ratio_ecma(
            signal[i]["is_stationary"], audio, fs, prominence=True
        )


if __name__ == "__main__":
    test_pr_ecma()
