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
from mosqito.functions.loudness_zwicker.loudness_zwicker_stationary import (
    loudness_zwicker_stationary,
)
from mosqito.functions.loudness_zwicker.comp_loudness import comp_loudness
from mosqito.functions.shared.load import load
from validations.loudness_zwicker.validation_loudness_zwicker_stationary import (
    check_compliance,
)


@pytest.mark.loudness_zwst  # to skip or run only loudness zwicker stationary tests
def test_loudness_zwicker_3oct():
    """Test function for the script loudness_zwicker_stationary

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
    # Third octave levels as input for stationary loudness
    # (from ISO 532-1 annex B2)
    test_signal_1 = np.array(
        [
            -60,
            -60,
            78,
            79,
            89,
            72,
            80,
            89,
            75,
            87,
            85,
            79,
            86,
            80,
            71,
            70,
            72,
            71,
            72,
            74,
            69,
            65,
            67,
            77,
            68,
            58,
            45,
            30.0,
        ]
    )

    signal = {
        "data_file": "Test signal 1.txt",
        "N": 83.296,
        "N_specif_file": "tests/input/test_signal_1.csv",
    }
    N, N_specific = loudness_zwicker_stationary(test_signal_1)
    loudness = {"values": N, "specific values": N_specific}

    tst = check_compliance(loudness, signal, "./tests/output/")
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
    sig, fs = load(signal["data_file"], calib=2 * 2 ** 0.5)

    # Compute Loudness
    loudness = comp_loudness(True, sig, fs)

    # Check ISO 532-1 compliance
    assert check_compliance(loudness, signal, "./tests/output/")


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
    sig, fs = load(signal["data_file"], calib=2 * 2 ** 0.5)

    # Compute Loudness
    loudness = comp_loudness(True, sig, fs)

    # Check ISO 532-1 compliance
    assert check_compliance(loudness, signal, "./tests/output/")


# test de la fonction
if __name__ == "__main__":
    # test_loudness_zwicker_3oct()
    # test_loudness_zwicker_wav()
    test_loudness_zwicker_44100Hz()
