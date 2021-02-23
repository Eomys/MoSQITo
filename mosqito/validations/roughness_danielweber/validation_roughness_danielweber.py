# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 13:41:37 2020

@author: wantysal
"""


# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.functions.roughness_danielweber.comp_roughness import comp_roughness
from mosqito.tests.roughness.signals_test_generation import signal_test


# Test signal parameters as input for roughness calculation
# (reference values from 'ref' script)
signal = np.zeros((20), dtype=dict)

signal[0] = {
    "fmod": 20,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 20 Hz",
    "R": np.array([0.232, 0.246, 0.243, 0.24, 0.219, 0.168, 0.108]),
}
signal[1] = {
    "fmod": 30,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 30 Hz",
    "R": np.array([0.334, 0.4, 0.408, 0.431, 0.385, 0.3, 0.192]),
}
signal[2] = {
    "fmod": 40,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 40 Hz",
    "R": np.array([0.327, 0.481, 0.584, 0.65, 0.55, 0.431, 0.275]),
}
signal[3] = {
    "fmod": 50,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 50 Hz",
    "R": np.array([0.253, 0.471, 0.672, 0.846, 0.717, 0.553, 0.358]),
}
signal[4] = {
    "fmod": 60,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 60 Hz",
    "R": np.array([0.193, 0.394, 0.67, 0.958, 0.81, 0.628, 0.421]),
}
signal[5] = {
    "fmod": 70,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 70 Hz",
    "R": np.array([0.151, 0.314, 0.609, 0.991, 0.84, 0.652, 0.436]),
}
signal[6] = {
    "fmod": 80,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 80 Hz",
    "R": np.array([0.115, 0.248, 0.51, 0.955, 0.809, 0.625, 0.415]),
}
signal[7] = {
    "fmod": 90,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 90 Hz",
    "R": np.array([0.093, 0.199, 0.42, 0.868, 0.743, 0.563, 0.376]),
}
signal[8] = {
    "fmod": 100,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 100 Hz",
    "R": np.array([0.078, 0.169, 0.356, 0.754, 0.633, 0.487, 0.327]),
}
signal[9] = {
    "fmod": 110,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 110 Hz",
    "R": np.array([0.067, 0.144, 0.302, 0.646, 0.545, 0.422, 0.28]),
}
signal[10] = {
    "fmod": 120,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 120 Hz",
    "R": np.array([0.059, 0.126, 0.264, 0.564, 0.47, 0.359, 0.243]),
}
signal[11] = {
    "fmod": 130,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 130 Hz",
    "R": np.array([0.051, 0.108, 0.234, 0.493, 0.414, 0.317, 0.214]),
}
signal[12] = {
    "fmod": 140,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 140 Hz",
    "R": np.array([0.041, 0.096, 0.205, 0.429, 0.362, 0.281, 0.189]),
}
signal[13] = {
    "fmod": 150,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 150 Hz",
    "R": np.array([0.04, 0.085, 0.176, 0.387, 0.327, 0.25, 0.169]),
}
signal[14] = {
    "fmod": 160,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 160 Hz",
    "R": np.array([0.036, 0.075, 0.164, 0.344, 0.296, 0.227, 0.154]),
}
signal[15] = {
    "fmod": 180,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 180 Hz",
    "R": np.array([0.029, 0.061, 0.142, 0.288, 0.239, 0.183, 0.122]),
}
signal[16] = {
    "fmod": 200,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 200 Hz",
    "R": np.array([0.024, 0.05, 0.119, 0.238, 0.201, 0.153, 0.102]),
}
signal[17] = {
    "fmod": 220,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 220 Hz",
    "R": np.array([0.02, 0.043, 0.096, 0.2, 0.171, 0.13, 0.085]),
}
signal[18] = {
    "fmod": 240,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 240 Hz",
    "R": np.array([0.018, 0.037, 0.08, 0.174, 0.147, 0.111, 0.074]),
}
signal[19] = {
    "fmod": 260,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 260 Hz",
    "R": np.array([0.017, 0.033, 0.069, 0.153, 0.129, 0.098, 0.063]),
}


def validation_roughness(signal):
    """Validation function for the roughness calculation of an audio signal

    Validation function for the Audio_signal class "comp_roughness" method with signal array
    as input. The input signals are chosen according to the article "Psychoacoustical
    roughness: implementation of an optimized model" by Daniel and Weber in 1997.
    The figure 3 is used to compare amplitude-modulated signals created according to
    their carrier frequency and modulation frequency to the article results.
    One .png compliance plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """
    # Stimulus parameters
    duration = 0.2
    fs = 44100
    level = 60
    mdepth = 1

    # Overlapping definition for roughness calculation
    overlap = 0

    # Roughness calculation for each carrier frequency
    R = np.zeros((len(signal["fc"])), dtype=dict)
    for ind_fc in range(len(signal["fc"])):
        stimulus = signal_test(
            signal["fc"][ind_fc], signal["fmod"], mdepth, fs, duration, level
        )
        roughness = comp_roughness(stimulus, fs, overlap)
        R[ind_fc] = roughness["values"][0]

    # Check compliance
    tst = check_compliance(R, signal)

    return tst


def check_compliance(R, signal):
    """Check the compliance of roughness calc. to Daniel and Weber article
    "Psychoacoustical roughness: implementation of an optimized model", 1997.

    Check the compliance of the input data R to figure 3 of the article
    using the reference data described in the dictionary article_ref.

    Parameter
    ---------
    R: numpy.array
        Calculated roughnesses [asper]

    Output
    ------
    tst : bool
        Compliance to the reference data
    """

    ref = signal["R"]

    # Test for comformance (17% tolerance)

    tst = (R >= ref * 0.83).all() and (R <= ref * 1.17).all()

    # Find the highest difference
    diff = 0
    ind = 0
    for i in range(R.size):
        d = (np.abs(R[i] - ref[i]) / ref[i]) * 100
        if d > diff:
            diff = d
        if d <= 30:
            ind += 1

    # Give indication about the difference

    prop = round(ind / len(ref) * 100)

    # Define and plot the tolerance curves
    fc = signal["fc"]
    tol_curve_min = ref * 0.83
    tol_curve_max = ref * 1.17
    plt.plot(
        fc,
        tol_curve_min,
        color="red",
        linestyle="solid",
        label="17% tolerance",
        linewidth=1,
    )
    plt.plot(fc, tol_curve_max, color="red", linestyle="solid", label="", linewidth=1)
    plt.legend()

    # Compliance plot
    plt.plot(fc, R, label="MOSQITO")
    plt.text(
        0.5,
        0.05,
        "Maximum difference: " + str(round(diff)) + " %",
        horizontalalignment="center",
        verticalalignment="center",
        transform=plt.gca().transAxes,
    )
    plt.text(
        0.5,
        0.15,
        "Difference under 30 % in " + str(prop) + " % of cases",
        horizontalalignment="center",
        verticalalignment="center",
        transform=plt.gca().transAxes,
    )
    if tst:
        plt.text(
            0.5,
            0.5,
            "Test passed (17% tolerance not exceeded)",
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

    if tst:
        clr = "green"
    else:
        clr = "red"
    plt.title(
        "Roughness for modulation frequency = " + str(signal["fmod"]) + " Hz", color=clr
    )
    plt.xlabel("Carrier frequency [Hertz]")
    plt.ylabel("Roughness, [Asper]")
    plt.savefig(
        "validation_roughness_dw_fmod" + str(signal["fmod"]) + "Hz" + ".png",
        format="png",
    )
    plt.clf()
    return tst


# test de la fonction
if __name__ == "__main__":
    for i in range(20):
        validation_roughness(signal[i])
