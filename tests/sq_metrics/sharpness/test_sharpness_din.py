# -*- coding: utf-8 -*-

import numpy as np
from scipy.fft import fft, fftfreq

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package.")


# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import sharpness_din, sharpness_din_freq, sharpness_din_perseg


@pytest.fixture
def test_signal():
    # Input signal from DIN 45692_2009E
    sig, fs = load("tests/input/broadband_570.wav", wav_calib=1)
    sig_dict = {
        "signal": sig,
        "fs": fs,
        "S_din": 2.85,
    }
    return sig_dict


@pytest.mark.sharpness_din  # to skip or run sharpness test
def test_sharpness_din(test_signal):
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

    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness = sharpness_din(sig, fs, weighting="din")

    # Check that the value is within the desired values +/- 5%
    # as per DIN 45692_2009E (chapter 6)
    np.testing.assert_allclose(sharpness, test_signal["S_din"], rtol=0.05)


@pytest.mark.sharpness_din
def test_sharpness_din_aures(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness = sharpness_din(sig, fs, weighting="aures")


@pytest.mark.sharpness_din
def test_sharpness_din_bismarck(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness = sharpness_din(sig, fs, weighting="bismarck")


@pytest.mark.sharpness_din
def test_sharpness_din_fastl(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness = sharpness_din(sig, fs, weighting="fastl")


@pytest.mark.sharpness_din  # to skip or run sharpness test
def test_sharpness_din_perseg(test_signal):
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

    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness, _ = sharpness_din_perseg(
        sig, fs, nperseg=2 ** 14, weighting="aures")
    sharpness, _ = sharpness_din_perseg(
        sig, fs, nperseg=2 ** 14, weighting="bismarck")
    sharpness, _ = sharpness_din_perseg(
        sig, fs, nperseg=2 ** 14, weighting="fastl")
    sharpness, time_axis = sharpness_din_perseg(
        sig, fs, nperseg=2 ** 14, weighting="din"
    )

    # Check that the value is within the desired values +/- 5%
    # as per DIN 45692_2009E (chapter 6)
    np.testing.assert_allclose(sharpness, test_signal["S_din"], rtol=0.05)


@pytest.mark.sharpness_din
def test_sharpness_din_perseg_aures(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness, _ = sharpness_din_perseg(
        sig, fs, nperseg=2 ** 14, weighting="aures")


@ pytest.mark.sharpness_din
def test_sharpness_din_perseg_bismarck(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness, _ = sharpness_din_perseg(
        sig, fs, nperseg=2 ** 14, weighting="bismarck")


@ pytest.mark.sharpness_din
def test_sharpness_din_perseg_fastl(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness, _ = sharpness_din_perseg(
        sig, fs, nperseg=2 ** 14, weighting="fastl")


@ pytest.mark.sharpness_din  # to skip or run sharpness test
def test_sharpness_din_freq(test_signal):
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
    signal = {"data_file": "tests/input/broadband_570.wav",
              "S": test_signal["S_din"]}

    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]
    # Compute corresponding spectrum
    n = len(sig)
    spec = 2 / np.sqrt(2) / n * fft(sig)[0:n//2]
    freqs = fftfreq(n, 1/fs)[0:n//2]

    # Compute sharpness
    sharpness = sharpness_din_freq(spec, freqs, weighting="din")

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
    # Reproduce the code from the fixture
    # Input signal from DIN 45692_2009E
    sig, fs = load("tests/input/broadband_570.wav", wav_calib=1)
    test_signal = {
        "signal": sig,
        "fs": fs,
        "S_din": 2.85,
    }
    test_sharpness_din(test_signal)
    test_sharpness_din_freq(test_signal)
    test_sharpness_din_perseg(test_signal)
