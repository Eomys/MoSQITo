# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:17:12 2020

@author: wantysal
"""


# Third party imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.functions.loudness_zwicker.comp_loudness import comp_loudness
from mosqito.functions.loudness_zwicker.loudness_zwicker_stationary import (
    loudness_zwicker_stationary,
)
from mosqito.functions.shared.load import load


def validation_loudness_zwicker_3oct():
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
        "N_specif_file": "./mosqito/validations/loudness_zwicker/data/ISO_532-1/test_signal_1.csv",
    }

    N, N_specific = loudness_zwicker_stationary(test_signal_1)
    loudness = {"values": N, "specific values": N_specific}
    tst = check_compliance(loudness, signal)
    assert tst

    # Test signal as input for stationary loudness
    # (from ISO 532-1 annex B3)


signal = np.zeros((4), dtype=dict)

signal[0] = {
    "data_file": "./mosqito/validations/loudness_zwicker/data/ISO_532-1/Test signal 2 (250 Hz 80 dB).wav",
    "N": 14.655,
    "N_specif_file": "./mosqito/validations/loudness_zwicker/data/ISO_532-1/test_signal_2.csv",
}
signal[1] = {
    "data_file": "./mosqito/validations/loudness_zwicker/data/ISO_532-1/Test signal 3 (1 kHz 60 dB).wav",
    "N": 4.019,
    "N_specif_file": "./mosqito/validations/loudness_zwicker/data/ISO_532-1/test_signal_3.csv",
}
signal[2] = {
    "data_file": "./mosqito/validations/loudness_zwicker/data/ISO_532-1/Test signal 4 (4 kHz 40 dB).wav",
    "N": 1.549,
    "N_specif_file": "./mosqito/validations/loudness_zwicker/data/ISO_532-1/test_signal_4.csv",
}
signal[3] = {
    "data_file": "./mosqito/validations/loudness_zwicker/data/ISO_532-1/Test signal 5 (pinknoise 60 dB).wav",
    "N": 10.498,
    "N_specif_file": "./mosqito/validations/loudness_zwicker/data/ISO_532-1/test_signal_5.csv",
}


def validation_loudness_zwicker_wav(signal):
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

    # Load signal and compute third octave band spectrum
    sig, fs = load(True, signal["data_file"], calib=2 * 2 ** 0.5)

    # Compute Loudness
    loudness = comp_loudness(True, sig, fs)

    # Check ISO 532-1 compliance
    assert check_compliance(loudness, signal)


def check_compliance(loudness, iso_ref):
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

    # Extract mosqito calculated values
    N = loudness["values"]
    N_specific = loudness["specific values"]

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
        "./mosqito/validations/loudness_zwicker/output/"
        + "validation_loudness_zwicker_stationary_"
        + file_name.split("/")[-1][:-4]
        + ".png",
        format="png",
    )
    plt.clf()
    return tst


# test de la fonction
if __name__ == "__main__":
    validation_loudness_zwicker_3oct()
    for i in range(4):
        validation_loudness_zwicker_wav(signal[i])
