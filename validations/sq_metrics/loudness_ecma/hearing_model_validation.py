# -*- coding: utf-8 -*-
# Optional package import
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


import numpy as np
from scipy.optimize import root_scalar

# Project Imports
from mosqito.sq_metrics import loudness_ecma
from mosqito.sq_metrics import equal_loudness_contours
from mosqito.utils.sine_wave_generator import (
    sine_wave_generator,
)


def comp_loudness_wrapper(spl, freq=1000, n_1kHz=0):
    """Return the difference between the loudness of a tone
    at <freq> Hz and <spl> dB and a tone at 1 KHz and <spl> dB

    Parameters
    ----------
    spl: float
        Test tone Sound Pressure Level [dB]
    freq: float
        Test tone frequency [Hz]
    n_1kHz: float
        Total loudness value of a 1 kHz / <spl> dB test tone

    Returns
    -------
    n_diff: float
        Difference between the test tone and the 1 kHz tone loudness

    """

    # test signal generation
    duration = 0.25
    fs = 48000.0
    signal, _ = sine_wave_generator(fs, duration, spl, freq)

    # compute loudness for the test signal
    n_specific, _ = loudness_ecma(signal)
    n_specific = np.array(n_specific)
    n_tot = np.sum(n_specific, axis=0)
    n_tot_mean = np.mean(n_tot[5:])

    # Return n_tot_mean - n_1kHz
    n_diff = n_tot_mean - n_1kHz

    return n_diff


def hearing_model_validation():
    """Validation of the ECMA loudness implementation according
    to ECMA-418-2 annex A
    """
    if plt is None:
        raise RuntimeError(
            "In order to make this validation plot you need the 'matplotlib' package."
            )

    phons = [80, 60, 40, 20]

    col_vec = ["tab:blue", "tab:red", "tab:orange", "tab:purple", "tab:green"]

    for phon, col in zip(phons, col_vec):
        print(str(phon) + " Phon equal loudness contour")

        # Get ISO 226 equal loudness contour (index 17 = 1000 Hz)
        spl_iso_vec, freq_vec = equal_loudness_contours(phon)

        # Compute ecma loudness of a 1 kHz tone
        n_1kHz = comp_loudness_wrapper(spl=phon)
        spl_ecma_vec = np.zeros(spl_iso_vec.shape)
        spl_ecma_vec[17] = phon

        # For each frequency...
        for i in np.arange(5, freq_vec.shape[0]):
            if i != 17:
                spl = spl_iso_vec[i]
                freq = freq_vec[i]
                # ... find the spl of the tone that produces the
                # same loudness as the 1 kHz tone
                spl_ecma_vec[i] = root_scalar(
                    comp_loudness_wrapper,
                    x0=spl,
                    args=(freq, n_1kHz),
                    bracket=[-5, 120],
                ).root
        # Plot the ISO 226 equal loudness contour
        plt.semilogx(freq_vec, spl_iso_vec, ":", color=col)
        # Plot the ECMA equal contour loudness
        if phon == 0:
            label = "lower treshold of hearing"
        else:
            label = str(phon) + " phon"
        plt.semilogx(freq_vec[5:], spl_ecma_vec[5:], color=col, label=label)

    plt.xlim(left=80, right=11000)
    plt.ylim((-15, 105))
    plt.ylabel("Sound Pressure Level [dB]")
    plt.xlabel("Frequency [Hz]")
    plt.grid(which="both", linestyle="-", color="grey")
    plt.legend()
    plt.savefig(
        "./validations/sq_metrics/loudness_ecma/output/"
        + "ecma_hearing_model_validation.png",
        format="png",
    )


if __name__ == "__main__":
    hearing_model_validation()
