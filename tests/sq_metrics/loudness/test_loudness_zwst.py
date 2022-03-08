# -*- coding: utf-8 -*-
"""
@date Created on Mon Mar 23 2020
@author martin_g for Eomys
"""

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
        )


import numpy as np

# Local application imports
from mosqito.utils import load
from mosqito.sq_metrics import loudness_zwst
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import (
    _main_loudness,
)
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import (
    _calc_slopes,
)
from validations.sq_metrics.loudness_zwst.validation_loudness_zwst import (
    _check_compliance,
)
from tests.input.Test_signal_1 import test_signal_1


@pytest.mark.loudness_zwst  # to skip or run only loudness zwicker stationary tests
def test_loudness_zwicker_3oct():
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
    target = {
        "data_file": "Test signal 1.txt",
        "N": 83.296,
        "N_specif_file": "tests/input/test_signal_1.csv",
    }

    #
    # Compute loudness
    Nm = _main_loudness(test_signal_1, field_type="free")
    N, N_specific = _calc_slopes(Nm)
    loudness = {"values": N, "specific values": N_specific}
    #
    # Asser complaiance
    tst = _check_compliance(loudness, target, "./tests/output/")
    assert tst


@pytest.mark.loudness_zwst  # to skip or run only loudness zwicker stationary tests
def test_loudness_zwicker_wav():
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
    signal = {
        "data_file": "tests/input/Test signal 3 (1 kHz 60 dB).wav",
        "N": 4.019,
        "N_specif_file": "tests/input/test_signal_3.csv",
    }

    # Load signal and compute third octave band spectrum
    sig, fs = load(signal["data_file"], wav_calib=2 * 2 ** 0.5)

    # Compute Loudness
    N, N_specific, bark_axis = loudness_zwst(sig, fs)
    loudness = {
        "name": "Loudness",
        "values": N,
        "specific values": N_specific,
        "freqs": bark_axis,
    }

    # Check ISO 532-1 compliance
    assert _check_compliance(loudness, signal, "./tests/output/")


@pytest.mark.loudness_zwst  # to skip or run only loudness zwicker stationary tests
def test_loudness_zwicker_44100Hz():
    """Test function for the script loudness_zwicker_stationary
    with input .wav file sampled at 44.1 kHz
    """
    # Test signal as input for stationary loudness
    # (from ISO 532-1 annex B3) resampled
    signal = {
        "data_file": "tests/input/Test signal 3 (1 kHz 60 dB)_44100Hz.wav",
        "N": 4.019,
        "N_specif_file": "tests/input/test_signal_3.csv",
    }

    # Load signal and compute third octave band spectrum
    sig, fs = load(signal["data_file"], wav_calib=2 * 2 ** 0.5)

    # Compute Loudness
    N, N_specific, bark_axis = loudness_zwst(sig, fs)
    loudness = {
        "name": "Loudness",
        "values": N,
        "specific values": N_specific,
        "freqs": bark_axis,
    }

    # Check ISO 532-1 compliance
    assert _check_compliance(loudness, signal, "./tests/output/")


# test de la fonction
if __name__ == "__main__":
    # test_loudness_zwicker_3oct()
    test_loudness_zwicker_wav()
    # test_loudness_zwicker_44100Hz()
