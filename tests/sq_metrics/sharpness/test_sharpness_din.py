# -*- coding: utf-8 -*-

import numpy as np
from scipy.fft import fft, fftfreq

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import (
    sharpness_din_st,
    sharpness_din_tv,
    sharpness_din_freq,
    sharpness_din_perseg,
)
from mosqito.sound_level_meter.comp_spectrum import comp_spectrum


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
def test_sharpness_din_st(test_signal):
    """Test function for the sharpness calculation of an audio signal
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
    sharpness = sharpness_din_st(sig, fs, weighting="din")

    # Check that the value is within the desired values +/- 5%
    # as per DIN 45692_2009E (chapter 6)
    np.testing.assert_allclose(sharpness, test_signal["S_din"], rtol=0.05)


@pytest.mark.sharpness_din  # to skip or run sharpness test
def test_sharpness_din_tv():
    """Test function for the sharpness calculation of an time-varying audio signal.

    Parameters
    ----------
    None
    Outputs
    -------
    None
    """

    # Input signal
    sig, fs = load("tests/input/white_noise_442_1768_Hz_varying.wav", wav_calib=0.01)

    # Compute sharpness
    sharpness, time = sharpness_din_tv(sig, fs, weighting="din", skip=0.2)


@pytest.mark.sharpness_din
def test_sharpness_din_aures(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness = sharpness_din_st(sig, fs, weighting="aures")


@pytest.mark.sharpness_din
def test_sharpness_din_bismarck(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness = sharpness_din_st(sig, fs, weighting="bismarck")


@pytest.mark.sharpness_din
def test_sharpness_din_fastl(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness = sharpness_din_st(sig, fs, weighting="fastl")


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
    sharpness, _ = sharpness_din_perseg(sig, fs, nperseg=2**14, weighting="aures")
    sharpness, _ = sharpness_din_perseg(sig, fs, nperseg=2**14, weighting="bismarck")
    sharpness, _ = sharpness_din_perseg(sig, fs, nperseg=2**14, weighting="fastl")
    sharpness, time_axis = sharpness_din_perseg(sig, fs, nperseg=2**14, weighting="din")

    # Check that the value is within the desired values +/- 5%
    # as per DIN 45692_2009E (chapter 6)
    np.testing.assert_allclose(sharpness, test_signal["S_din"], rtol=0.05)


@pytest.mark.sharpness_din
def test_sharpness_din_perseg_aures(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness, _ = sharpness_din_perseg(sig, fs, nperseg=2**14, weighting="aures")


@pytest.mark.sharpness_din
def test_sharpness_din_perseg_bismarck(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness, _ = sharpness_din_perseg(sig, fs, nperseg=2**14, weighting="bismarck")


@pytest.mark.sharpness_din
def test_sharpness_din_perseg_fastl(test_signal):
    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute sharpness
    sharpness, _ = sharpness_din_perseg(sig, fs, nperseg=2**14, weighting="fastl")


@pytest.mark.sharpness_din  # to skip or run sharpness test
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
    signal = {"data_file": "tests/input/broadband_570.wav", "S": test_signal["S_din"]}

    # Input signal
    sig = test_signal["signal"]
    fs = test_signal["fs"]
    # Compute corresponding spectrum
    spec, freqs = comp_spectrum(sig, fs, nfft="default", window="blackman", db=False)

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
    test_sharpness_din_st(test_signal)
    test_sharpness_din_tv()
    test_sharpness_din_freq(test_signal)
    test_sharpness_din_perseg(test_signal)
