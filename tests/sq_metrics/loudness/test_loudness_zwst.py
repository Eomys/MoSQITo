# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

import numpy as np
from numpy.fft import fft, fftfreq

# Local application imports
from mosqito.utils import load, isoclose
from mosqito.sq_metrics import loudness_zwst, loudness_zwst_freq, loudness_zwst_perseg
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import _main_loudness
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import _calc_slopes
from tests.input.Test_signal_1 import test_signal_1


@pytest.fixture
def test_signal():
    sig, fs = load(
        "tests/input/Test signal 5 (pinknoise 60 dB).wav", wav_calib=2 * 2**0.5
    )
    N_specif_iso = np.genfromtxt("tests/input/test_signal_5.csv", skip_header=1)
    sig_dict = {
        "signal": sig,
        "fs": fs,
        "N_iso": 10.498,
        "N_specif_iso": N_specif_iso,
    }
    return sig_dict


@pytest.mark.loudness_zwst  # to skip or run only loudness zwicker stationary tests
def test_loudness_zwst_3oct():
    """Test function for the script loudness_zwst

    Test function for the script loudness_zwicker_stationary with
    third octave band spectrum as input. The input spectrum is
    provided by ISO 532-1 annex B2, the compliance is assessed
    according to section 5.1 of the standard. One .png compliance
    plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    # Target values
    N_iso = 83.296
    N_specif_iso = np.genfromtxt("tests/input/test_signal_1.csv", skip_header=1)

    # Compute loudness
    Nm = _main_loudness(test_signal_1, field_type="free")
    N, N_specific = _calc_slopes(Nm)

    # Assert compliance
    is_isoclose_N = isoclose(N_iso, N, rtol=5 / 100, atol=0.1)
    is_isoclose_N_specific = isoclose(N_specific, N_specif_iso, rtol=5 / 100, atol=0.1)
    assert is_isoclose_N and is_isoclose_N_specific


@pytest.mark.loudness_zwst
def test_loudness_zwst_wav(test_signal):
    """Test function for the script loudness_zwicker_stationary

    Test function for the script loudness_zwicker_stationary with
    .wav file as input. The input file is provided by ISO 532-1 annex
    B3, the compliance is assessed according to section 5.1 of the
    standard. One .png compliance plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    # Test signal as input for stationary loudness
    # (from ISO 532-1 annex B3)
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute Loudness
    N, N_specific, bark_axis = loudness_zwst(sig, fs)

    # Assert compliance
    is_isoclose_N = isoclose(N, test_signal["N_iso"], rtol=5 / 100, atol=0.1)
    is_isoclose_N_specific = isoclose(
        N_specific, test_signal["N_specif_iso"], rtol=5 / 100, atol=0.1
    )
    assert is_isoclose_N and is_isoclose_N_specific


@pytest.mark.loudness_zwst
def test_loudness_zwst_44100Hz():
    """Test function for the script loudness_zwicker_stationary
    with input .wav file sampled at 44.1 kHz
    """
    # Test signal as input for stationary loudness
    # (from ISO 532-1 annex B3) resampled
    sig, fs = load(
        "tests/input/Test signal 3 (1 kHz 60 dB)_44100Hz.wav", wav_calib=2 * 2**0.5
    )

    # Target values
    N_iso = 4.019
    N_specif_iso = np.genfromtxt("tests/input/test_signal_3.csv", skip_header=1)

    # Compute Loudness
    N, N_specific, bark_axis = loudness_zwst(sig, fs)

    # Assert compliance
    is_isoclose_N = isoclose(N, N_iso, rtol=5 / 100, atol=0.1)
    is_isoclose_N_specific = isoclose(N_specific, N_specif_iso, rtol=5 / 100, atol=0.1)
    assert is_isoclose_N and is_isoclose_N_specific


@pytest.mark.loudness_zwst
def test_loudness_zwst_perseg(test_signal):
    sig = test_signal["signal"]
    fs = test_signal["fs"]

    # Compute Loudness
    N, N_specific, bark_axis, time_axis = loudness_zwst_perseg(
        sig, fs, nperseg=8192 * 2, noverlap=4096
    )

    # Check that all values are within the desired values +/- 5%
    np.testing.assert_allclose(N, 10.498, rtol=0.05)


@pytest.mark.loudness_zwst  # to skip or run only loudness zwicker stationary tests
def test_loudness_zwst_freq(test_signal):
    """Test function for the script loudness_zwicker_stationary

    Test function for the script loudness_zwicker_stationary with
    complex spectrum file as input. The input file is provided by ISO 532-1 annex
    B3, the compliance is assessed according to section 5.1 of the
    standard. One .png compliance plot is generated.

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
    # Compute corresponding spectrum
    n = len(sig)
    spec = np.abs(2 / np.sqrt(2) / n * fft(sig)[0 : n // 2])
    freqs = fftfreq(n, 1 / fs)[0 : n // 2]
    # Compute Loudness
    N, N_specific, bark_axis = loudness_zwst_freq(spec, freqs)

    # 2D inputs
    spec = np.tile(spec, (4, 1)).T
    N1, N1_specific, bark_axis = loudness_zwst_freq(spec, freqs)

    freqs = np.tile(freqs, (4, 1)).T
    N2, N2_specific, bark_axis = loudness_zwst_freq(spec, freqs)

    # Assert compliance
    is_isoclose_N = isoclose(N, test_signal["N_iso"], rtol=5 / 100, atol=0.1)
    is_isoclose_N_specific = isoclose(
        N_specific, test_signal["N_specif_iso"], rtol=5 / 100, atol=0.1
    )
    assert is_isoclose_N and is_isoclose_N_specific


@pytest.mark.loudness_zwst
def test_loudness_zwst_gi0():
    """
    Test with a signal creating some zero values in gi variable
    of _main_loudness function (bug solved)
    """

    sig = np.load("tests/input/test_signal_gi0.npy")
    fs = 48000

    # Compute Loudness
    N, N_specific, bark_axis, time_axis = loudness_zwst_perseg(
        sig, fs, nperseg=8192 * 2, noverlap=4096
    )


# test
if __name__ == "__main__":
    # Reproduce the code from the fixture
    sig, fs = load(
        "tests/input/Test signal 5 (pinknoise 60 dB).wav", wav_calib=2 * 2**0.5
    )
    N_specif_iso = np.genfromtxt("tests/input/test_signal_5.csv", skip_header=1)
    test_signal = {
        "signal": sig,
        "fs": fs,
        "N_iso": 10.498,
        "N_specif_iso": N_specif_iso,
    }

    # test_loudness_zwst_3oct()
    # test_loudness_zwst_wav(test_signal)
    # test_loudness_zwst_44100Hz()
    # test_loudness_zwst_perseg(test_signal)
    # test_loudness_zwst_freq(test_signal)
    test_loudness_zwst_gi0()
