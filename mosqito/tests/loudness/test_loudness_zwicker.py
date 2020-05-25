# -*- coding: utf-8 -*-
"""
@date Created on Mon Mar 23 2020
@author martin_g for Eomys
"""

# Standard library imports

# Third party imports
import numpy as np
import matplotlib.pyplot as plt
import pytest

# Local application imports
from mosqito.loudness.loudness_zwicker_stationary import loudness_zwicker_stationary
from mosqito.generic.wav_to_oct3 import wav_to_oct3


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
        "N_specif_file": "mosqito/tests/data/ISO_532-1/test_signal_1.csv",
    }
    N, N_specific, bark_axis = loudness_zwicker_stationary(test_signal_1)
    tst = check_compliance(N, N_specific, bark_axis, signal)
    assert tst


# pytest.mark.parametrize allows to execute a test for different data : see http://doc.pytest.org/en/latest/parametrize.html
@pytest.mark.loudness_zwst  # to skip or run only loudness zwicker stationary tests
@pytest.mark.parametrize(
    "signal",
    [
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Test signal 2 (250 Hz 80 dB).wav",
            "N": 14.655,
            "N_specif_file": "mosqito/tests/data/ISO_532-1/test_signal_2.csv",
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Test signal 3 (1 kHz 60 dB).wav",
            "N": 4.019,
            "N_specif_file": "mosqito/tests/data/ISO_532-1/test_signal_3.csv",
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Test signal 4 (4 kHz 40 dB).wav",
            "N": 1.549,
            "N_specif_file": "mosqito/tests/data/ISO_532-1/test_signal_4.csv",
        },
        {
            "data_file": "mosqito/tests/data/ISO_532-1/Test signal 5 (pinknoise 60 dB).wav",
            "N": 10.498,
            "N_specif_file": "mosqito/tests/data/ISO_532-1/test_signal_5.csv",
        },
    ],
)

@pytest.mark.loudness_zwst  # to skip or run only loudness zwicker stationary tests
def test_loudness_zwicker_wav(signal):
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

    # Load signal and compute third octave band spectrum
    spec, _ = wav_to_oct3(signal["data_file"], calib=2 * 2 ** 0.5)
    # Compute Loudness
    N, N_specific, bark_axis = loudness_zwicker_stationary(
        20 * np.log10(np.squeeze(spec) / (2 * 10 ** -5))
    )
    # Check ISO 532-1 compliance
    assert check_compliance(N, N_specific, bark_axis, signal)


def check_compliance(N, N_specific, bark_axis, iso_ref):
    """Check the comppiance of loudness calc. to ISO 532-1

    Check the compliance of the input data N and N_specific
    to section 5.1 of ISO 532-1 by using the reference data
    described in dictionary iso_ref.

    Parameters
    ----------
    N : float
        Calculated loudness [sones]
    N_specific : numpy.ndarray
        Specific loudness [sones/bark]
    bark_axis : numpy.ndarray
        Corresponding bark axis
    iso_ref : dict
        {
            "data_file": <Path to reference input signal>,
            "N": <Reference loudness value>,
            "N_specif_file": <Path to reference calculated specific loudness>    
        }
        Dictionary containing link to ref. data

    Outputs
    -------
    tst : bool
        Compliance to the reference data
    """
    # Load ISO reference outputs
    N_iso = iso_ref["N"]
    N_specif_iso = np.genfromtxt(iso_ref["N_specif_file"], skip_header=1)
    # Test for ISO 532-1 comformance (section 5.1)
    tst_N = (
        N >= N_iso * 0.95
        and N <= N_iso * 1.05
        and N >= N_iso - 0.1
        and N <= N_iso + 0.1
    )
    tst_specif = (
        (N_specific >= np.amin([N_specif_iso * 0.95, N_specif_iso - 0.1], axis=0)).all()
        and (
            N_specific <= np.amax([N_specif_iso * 1.05, N_specif_iso + 0.1], axis=0)
        ).all()
    )
    tst = tst_N and tst_specif
    # Generate compliance plot
    if tst_specif:
        clr = "green"
    else:
        clr = "red"
    plt.plot(bark_axis, N_specific, label="MoSQITo", color=clr)
    plt.fill_between(
        bark_axis,
        np.amin([N_specif_iso * 0.95, N_specif_iso - 0.1], axis=0),
        np.amax([N_specif_iso * 1.05, N_specif_iso + 0.1], axis=0),
        alpha=0.4,
        color="gray",
        label="ISO 532-1 compliance",
    )
    plt.legend()
    plt.xlabel("Critical band rate [Bark]")
    plt.ylabel("Specific loudness, [sones/Bark]")
    if tst_N:
        clr = "green"
    else:
        clr = "red"
    plt.title("N = " + str(N) + " sone (ISO ref. " + str(N_iso) + " sone)", color=clr)
    file_name = "_".join(iso_ref["data_file"].split(" "))
    plt.savefig(
        "mosqito/tests/output/test_loudness_zwicker_wav_"
        + file_name.split("/")[-1][:-4]
        + ".png",
        format="png",
    )
    plt.clf()
    return tst


# test de la fonction
if __name__ == "__main__":
    test_loudness_zwicker_3oct()
