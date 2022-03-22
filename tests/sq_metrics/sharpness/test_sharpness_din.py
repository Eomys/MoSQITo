# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 09:20:41 2020

@author: wantysal
"""

import numpy as np

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")


# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import sharpness_din


@pytest.mark.sharpness_din  # to skip or run sharpness test
def test_sharpness_din():
    """Test function for the sharpness calculation of an audio signal

    Test function for the function "comp_roughness" with 'din' method.
    The input signals come from DIN 45692_2009E. The compliance is assessed
    according to chapter 6 of the standard.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    # Input signal from DIN 45692_2009E
    signal = {"data_file": "tests/input/1KHZ60DB.wav", "S": 1}

    # Load signal
    sig, fs = load(signal["data_file"], wav_calib=1)

    # Compute sharpness
    sharpness = sharpness_din(sig, fs, weighting="din")

    # Check that the value is within the desired values +/- 5%
    # as per DIN 45692_2009E (chapter 6)
    np.testing.assert_allclose(sharpness, 1, rtol=0.05)


@pytest.mark.sharpness_din  # to skip or run sharpness test
def test_sharpness_din_per_blocks():
    """Test function for the sharpness calculation of an audio signal

    Test function for the function "comp_roughness" with 'din' method.
    The input signals come from DIN 45692_2009E. The compliance is assessed
    according to chapter 6 of the standard.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    # Input signal from DIN 45692_2009E
    signal = {"data_file": "tests/input/1KHZ60DB.wav", "S": 1}

    # Load signal
    sig, fs = load(signal["data_file"], wav_calib=1)

    # Compute sharpness
    sharpness = sharpness_din(sig, fs, weighting="din")

    # Check that the value is within the desired values +/- 5%
    # as per DIN 45692_2009E (chapter 6)
    np.testing.assert_allclose(sharpness, 1, rtol=0.05)


# test de la fonction
if __name__ == "__main__":
    test_sharpness_din()
