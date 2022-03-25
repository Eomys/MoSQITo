# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 09:20:41 2020

@author: wantysal
"""

import numpy as np
from scipy.fft import fft

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


@pytest.mark.sharpness_din  # to skip or run sharpness test
def test_sharpness_din_spec():
    """Test function for the sharpness calculation of an audio signal

    Test function for the function "comp_roughness" with 'din' method.
    The input signals come from DIN 45692_2009E. The compliance is assessed
    according to chapter 6 of the standard.
    One .png compliance plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    # Input signal from DIN 45692_2009E
    signal = {"data_file": "tests/input/broadband_570.wav", "S": 1}

    # Load signal
    sig, fs = load(signal["data_file"], wav_calib=1)

    # Compute corresponding spectrum
    n = len(sig)
    spec = fft(sig * np.blackman(n) / np.sum(np.blackman(n)))[0 : n // 2]
    freqs = np.arange(0, n // 2, 1) * (fs / n)

    # Compute sharpness
    sharpness = sharpness_din(spec, fs, freqs=freqs, weighting="din")

    assert check_compliance(sharpness, signal)


def check_compliance(S, signal):
    """Check the comppiance of loudness calc. to ISO 532-1

    The compliance is assessed according to chapter 6 of the
    standard DIN 45692_2009E.

    Parameters
    ----------
    S : float
        computed sharpness value
    signal : dict
        {"data file" : <path to the standard file >
         "S" : <sharpness reference value>
         }

    Outputs
    -------
    tst : bool
        Compliance to the reference data
    """

    # Load reference value
    ref = signal["S"]

    # Test for DIN 45692_2009E comformance (chapter 6)
    tst = (S >= np.amax([ref * 0.95, ref - 0.05], axis=0)).all() and (
        S <= np.amin([ref * 1.05, ref + 0.05], axis=0)
    ).all()

    return tst


# test de la fonction
if __name__ == "__main__":
    test_sharpness_din()
    test_sharpness_din_spec()
    test_sharpness_din_perseg()
