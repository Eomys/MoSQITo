# -*- coding: utf-8 -*-
"""
@date Created on Mon Mar 23 2020
@author martin_g for Eomys
"""

# Third party imports
import numpy as np
import matplotlib.pyplot as plt
import pytest

# Local application imports
from mosqito.functions.loudness_zwicker.loudness_zwicker_stationary import (
    loudness_zwicker_stationary,
)
from mosqito.functions.shared.load import load2oct3


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
        "N_specif_file": "mosqito/tests/loudness/data/ISO_532-1/test_signal_1.csv",
    }
    N, N_specific = loudness_zwicker_stationary(test_signal_1)

    tst = check_compliance(N, N_specific, signal)

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
        "data_file": "mosqito/tests/loudness/data/ISO_532-1/Test signal 3 (1 kHz 60 dB).wav",
        "N": 4.019,
        "N_specif_file": "mosqito/tests/loudness/data/ISO_532-1/test_signal_3.csv",
    }

    # Load signal and compute third octave band spectrum
    third_spec = load2oct3(True, signal["data_file"], calib=2 * 2 ** 0.5)

    # Compute Loudness
    N, N_specific = loudness_zwicker_stationary(third_spec["values"])

    # Check ISO 532-1 compliance
    assert check_compliance(N, N_specific, signal)


def check_compliance(N, N_specific, iso_ref):
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
        N_specific >= np.amin([N_specif_iso * 0.95, N_specif_iso - 0.1], axis=0)
    ).all() and (
        N_specific <= np.amax([N_specif_iso * 1.05, N_specif_iso + 0.1], axis=0)
    ).all()
    tst = tst_N and tst_specif

    # Define and plot the tolerance curves
    bark_axis = np.linspace(0.1, 24, int(24 / 0.1))
    tol_curve_min = np.amin([N_specif_iso * 0.95, N_specif_iso - 0.1], axis=0)
    tol_curve_min[tol_curve_min < 0] = 0
    tol_curve_max = np.amax([N_specif_iso * 1.05, N_specif_iso + 0.1], axis=0)
    plt.plot(
        bark_axis,
        tol_curve_min,
        color="red",
        linestyle="solid",
        label="5% tolerance",
        linewidth=1,
    )
    plt.plot(
        bark_axis, tol_curve_max, color="red", linestyle="solid", label="", linewidth=1
    )
    plt.legend()

    # Compliance plot

    plt.plot(bark_axis, N_specific, label="MOSQITO")
    if tst_specif:
        plt.text(
            0.5,
            0.5,
            "Test passed (5% tolerance not exceeded)",
            horizontalalignment="center",
            verticalalignment="center",
            transform=plt.gca().transAxes,
            bbox=dict(facecolor="green", alpha=0.3),
        )
    else:
        tst = 0
        plt.text(
            0.5,
            0.5,
            "Test not passed",
            horizontalalignment="center",
            verticalalignment="center",
            transform=plt.gca().transAxes,
            bbox=dict(facecolor="red", alpha=0.3),
        )

    if tst_N:
        clr = "green"
    else:
        clr = "red"
    plt.title("N = " + str(N) + " sone (ISO ref. " + str(N_iso) + " sone)", color=clr)
    file_name = "_".join(iso_ref["data_file"].split(" "))
    plt.savefig(
        "mosqito/tests/loudness/output/test_loudness_zwicker_wav_"
        + file_name.split("/")[-1][:-4]
        + ".png",
        format="png",
    )
    plt.clf()
    return tst


# test de la fonction
if __name__ == "__main__":
    test_loudness_zwicker_3oct()
