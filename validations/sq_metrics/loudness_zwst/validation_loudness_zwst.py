# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:17:12 2020

@author: wantysal
"""

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )

# Third party imports
from os.path import basename, splitext
import numpy as np

# Local application imports
from mosqito.sq_metrics import loudness_zwst
from mosqito.utils import isoclose
from mosqito.utils import load
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import (
    _main_loudness,
)
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import (
    _calc_slopes,
)
from validations.sq_metrics.loudness_zwst.input.ISO_532_1.test_signal_1 import test_signal_1


def validation_loudness_zwst_3oct():
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
    # (from ISO 532-1 annex B2) : test_signal_1

    # Load ISO reference outputs
    file_path = "./validations/sq_metrics/loudness_zwst/input/ISO_532_1/test_signal_1.csv"
    N_iso = 83.296
    N_specif_iso = np.genfromtxt(
        file_path, skip_header=1
    )

    # Compute loudness
    Nm = _main_loudness(test_signal_1, field_type="free")
    N, N_specific = _calc_slopes(Nm)
    loudness = {"values": N, "specific values": N_specific}
    bark_axis = np.linspace(0.1, 24, int(24 / 0.1))

    # Test
    is_isoclose_N = isoclose(N_iso, N, rtol=5/100,
                             atol=0.1, is_plot=False, xaxis=None)
    is_isoclose_N_specific = isoclose(
        N_specif_iso, N_specific, rtol=5/100, atol=0.1, is_plot=True, tol_label='ISO 532-1 tolerance', xaxis=bark_axis)

    # Format and save validation plot
    _format_plot(is_isoclose_N, is_isoclose_N_specific, N,
                 N_iso, splitext(basename(file_path))[0])


def validation_loudness_zwst():
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

    #
    # Test signal as input for stationary loudness
    #  # (from ISO 532-1 annex B3)

    signals = [
        {
            "data_file": "./validations/sq_metrics/loudness_zwst/input/ISO_532_1/Test signal 2 (250 Hz 80 dB).wav",
            "N": 14.655,
            "N_specif_file": "./validations/sq_metrics/loudness_zwst/input/ISO_532_1/test_signal_2.csv",
        },
        {
            "data_file": "./validations/sq_metrics/loudness_zwst/input/ISO_532_1/Test signal 3 (1 kHz 60 dB).wav",
            "N": 4.019,
            "N_specif_file": "./validations/sq_metrics/loudness_zwst/input/ISO_532_1/test_signal_3.csv",
        },
        {
            "data_file": "./validations/sq_metrics/loudness_zwst/input/ISO_532_1/Test signal 4 (4 kHz 40 dB).wav",
            "N": 1.549,
            "N_specif_file": "./validations/sq_metrics/loudness_zwst/input/ISO_532_1/test_signal_4.csv",
        },
        {
            "data_file": "./validations/sq_metrics/loudness_zwst/input/ISO_532_1/Test signal 5 (pinknoise 60 dB).wav",
            "N": 10.498,
            "N_specif_file": "./validations/sq_metrics/loudness_zwst/input/ISO_532_1/test_signal_5.csv",
        },
    ]

    for signal in signals:
        # Load signal and compute third octave band spectrum
        sig, fs = load(signal["data_file"], wav_calib=2 * 2 ** 0.5)

        # Compute Loudness
        N, N_specific, bark_axis = loudness_zwst(sig, fs)

        # Load reference N'
        N_iso = signal["N"]
        N_specif_iso = np.genfromtxt(signal["N_specif_file"], skip_header=1)

        # Test
        is_isoclose_N = isoclose(N_iso, N, rtol=5/100,
                                 atol=0.1, is_plot=False, xaxis=None)
        is_isoclose_N_specific = isoclose(
            N_specif_iso, N_specific, rtol=5/100, atol=0.1, is_plot=True, tol_label='ISO 532-1 tolerance', xaxis=bark_axis)

        # Format and save validation plot
        _format_plot(is_isoclose_N, is_isoclose_N_specific, N,
                     N_iso, splitext(basename(signal["data_file"]))[0])


def _check_compliance(loudness, iso_ref, out_dir):
    """Check the compliance of loudness calc. to ISO 532-1

    Check the compliance of the input data N and N_specific
    to section 5.1 of ISO 532-1 by using the reference data
    described in dictionary iso_ref.

    Parameters
    ----------
    loudness: dict
        {
            "name": "Loudness",
            "values": N: float/numpy.array
                loudness value
            "specific values": N_specific: numpy.array
                specific loudness values
            "freqs": bark_axis: numpy.array
                frequency axis corresponding to N_specific values in bark
        }
    iso_ref: dict
        {
            "data_file": <Path to reference input signal>,
            "N": <Reference loudness value>,
            "N_specif_file": <Path to reference calculated specific loudness>
        }
        Dictionary containing link to ref. data
    out_dir: str
        path to the directory to store the results

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
        N_specific >= np.amin(
            [N_specif_iso * 0.95, N_specif_iso - 0.1], axis=0)
    ).all() and (
        N_specific <= np.amax(
            [N_specif_iso * 1.05, N_specif_iso + 0.1], axis=0)
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
    plt.title("N = " + str(N) + " sone (ISO ref. " +
              str(N_iso) + " sone)", color=clr)
    file_name = "_".join(iso_ref["data_file"].split(" "))
    plt.savefig(
        out_dir + "validation_loudness_zwst_" +
        file_name.split("/")[-1][:-4] + ".png",
        format="png",
    )
    plt.clf()
    return tst


def _format_plot(is_isoclose_N, is_isoclose_N_specific, N, N_iso, filename):
    # Format plot
    plt.xlabel('Critical band rate [Bark]')
    plt.ylabel('N\'_zwst [sone/Bark]')
    color = 'tab:green'
    if is_isoclose_N:
        txt_label = "N within tolerance (%.1f sone for an ISO value of %.1f sone)" % (
            N, N_iso)
    else:
        txt_label = "N without tolerance (%.1f sone for an ISO value of %.1f sone)" % (
            N, N_iso)
        color = 'tab:red'
    if is_isoclose_N_specific:
        txt_label += '\n N\' within tolerance'
    else:
        txt_label += '\n N\' without tolerance'
        color = 'tab:red'
    props = dict(boxstyle='round', facecolor=color, alpha=0.3)
    plt.text(
        0.5,
        0.05,
        txt_label,
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=plt.gca().transAxes,
        bbox=props,
    )
    out_dir = "./validations/sq_metrics/loudness_zwst/output/"
    plt.savefig(
        out_dir + 'validation_loudness_zwst_' +
        "_".join(filename.split(" ")) + ".png",
        format="png",
    )
    plt.close()


# test de la fonction
if __name__ == "__main__":
    validation_loudness_zwst_3oct()
    validation_loudness_zwst()
