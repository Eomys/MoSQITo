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
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import _main_loudness
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import _calc_slopes
from input.ISO_532_1.test_signal_1 import test_signal_1


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
    file_path = "input/ISO_532_1/test_signal_1.csv"
    N_iso = 83.296
    N_specif_iso = np.genfromtxt(file_path, skip_header=1)

    # Compute loudness
    Nm = _main_loudness(test_signal_1, field_type="free")
    N, N_specific = _calc_slopes(Nm)
    loudness = {"values": N, "specific values": N_specific}
    bark_axis = np.linspace(0.1, 24, int(24 / 0.1))

    # Test
    is_isoclose_N = isoclose(
        N, N_iso, rtol=5 / 100, atol=0.1, is_plot=False, xaxis=None
    )
    is_isoclose_N_specific = isoclose(
        N_specific,
        N_specif_iso,
        rtol=5 / 100,
        atol=0.1,
        is_plot=True,
        tol_label="ISO 532-1 tolerance",
        xaxis=bark_axis,
    )

    # Format and save validation plot
    _format_plot(
        is_isoclose_N,
        is_isoclose_N_specific,
        N,
        N_iso,
        splitext(basename(file_path))[0],
    )


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
            "data_file": "input/ISO_532_1/Test signal 2 (250 Hz 80 dB).wav",
            "N": 14.655,
            "N_specif_file": "input/ISO_532_1/test_signal_2.csv",
        },
        {
            "data_file": "input/ISO_532_1/Test signal 3 (1 kHz 60 dB).wav",
            "N": 4.019,
            "N_specif_file": "input/ISO_532_1/test_signal_3.csv",
        },
        {
            "data_file": "input/ISO_532_1/Test signal 4 (4 kHz 40 dB).wav",
            "N": 1.549,
            "N_specif_file": "input/ISO_532_1/test_signal_4.csv",
        },
        {
            "data_file": "input/ISO_532_1/Test signal 5 (pinknoise 60 dB).wav",
            "N": 10.498,
            "N_specif_file": "input/ISO_532_1/test_signal_5.csv",
        },
    ]

    for signal in signals:
        # Load signal and compute third octave band spectrum
        sig, fs = load(signal["data_file"], wav_calib=2 * 2**0.5)

        # Compute Loudness
        N, N_specific, bark_axis = loudness_zwst(sig, fs)

        # Load reference N'
        N_iso = signal["N"]
        N_specif_iso = np.genfromtxt(signal["N_specif_file"], skip_header=1)

        # Test
        is_isoclose_N = isoclose(
            N, N_iso, rtol=5 / 100, atol=0.1, is_plot=False, xaxis=None
        )
        is_isoclose_N_specific = isoclose(
            N_specific,
            N_specif_iso,
            rtol=5 / 100,
            atol=0.1,
            is_plot=True,
            tol_label="ISO 532-1 tolerance",
            xaxis=bark_axis,
        )

        # Format and save validation plot
        _format_plot(
            is_isoclose_N,
            is_isoclose_N_specific,
            N,
            N_iso,
            splitext(basename(signal["data_file"]))[0],
        )


def _format_plot(is_isoclose_N, is_isoclose_N_specific, N, N_iso, filename):
    # Format plot
    plt.xlabel("Critical band rate [Bark]")
    plt.ylabel("N'_zwst [sone/Bark]")
    color = "tab:green"
    if is_isoclose_N:
        txt_label = "N within tolerance (%.1f sone for an ISO value of %.1f sone)" % (
            N,
            N_iso,
        )
    else:
        txt_label = "N without tolerance (%.1f sone for an ISO value of %.1f sone)" % (
            N,
            N_iso,
        )
        color = "tab:red"
    if is_isoclose_N_specific:
        txt_label += "\n N' within tolerance"
    else:
        txt_label += "\n N' without tolerance"
        color = "tab:red"
    props = dict(boxstyle="round", facecolor=color, alpha=0.3)
    plt.text(
        0.5,
        0.05,
        txt_label,
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=plt.gca().transAxes,
        bbox=props,
    )
    out_dir = "output/"
    plt.savefig(
        out_dir + "validation_loudness_zwst_" + "_".join(filename.split(" ")) + ".png",
        format="png",
    )
    plt.close()


# test de la fonction
if __name__ == "__main__":
    validation_loudness_zwst_3oct()
    validation_loudness_zwst()
