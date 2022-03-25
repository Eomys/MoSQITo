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
from mosqito.sq_metrics import sharpness_din_perseg


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
    sig, fs = load("tests/input/broadband_570.wav", wav_calib=1)

    # Compute sharpness
    sharpness = sharpness_din(sig, fs, weighting="aures")
    sharpness = sharpness_din(sig, fs, weighting="bismarck")
    sharpness = sharpness_din(sig, fs, weighting="fastl")
    sharpness = sharpness_din(sig, fs, weighting="din")

    # Check that the value is within the desired values +/- 5%
    # as per DIN 45692_2009E (chapter 6)
    np.testing.assert_allclose(sharpness, 2.85, rtol=0.05)


@pytest.mark.sharpness_din  # to skip or run sharpness test
def test_sharpness_din_perseg():
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
    sig, fs = load("tests/input/broadband_570.wav", wav_calib=1)

    # Compute sharpness
    sharpness, _ = sharpness_din_perseg(sig, fs, nperseg=2 ** 14, weighting="aures")
    sharpness, _ = sharpness_din_perseg(sig, fs, nperseg=2 ** 14, weighting="bismarck")
    sharpness, _ = sharpness_din_perseg(sig, fs, nperseg=2 ** 14, weighting="fastl")
    sharpness, time_axis = sharpness_din_perseg(
        sig, fs, nperseg=2 ** 14, weighting="din"
    )

    # Check that the value is within the desired values +/- 5%
    # as per DIN 45692_2009E (chapter 6)
    np.testing.assert_allclose(sharpness, 2.85, rtol=0.05)


# test de la fonction
if __name__ == "__main__":
    test_sharpness_din()
    test_sharpness_din_perseg()
