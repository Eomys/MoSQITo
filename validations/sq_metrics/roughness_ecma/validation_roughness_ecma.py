# -*- coding: utf-8 -*-

# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.sq_metrics import roughness_ecma


def signal_test(fc, fmod, mdepth, fs, d, dB):
    """Creation of stationary amplitude modulated signals for the roughness
    validation procedure (signal created according to equation 1 in
    "Psychoacoustical roughness:implementation of an optimized model"
    by Daniel and Weber in 1997.

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer
        modulation frequency
    mdepth: float
        modulation depth
    fs: integer
        sampling frequency
    d: float
        signal duration [s]
    dB: integer
        SPL dB level of the carrier signal
    """

    # time axis definition
    dt = 1 / fs
    time = np.arange(0, d, dt)

    signal = (
        0.5
        * (1 + mdepth * (np.sin(2 * np.pi * fmod * time)))
        * np.sin(2 * np.pi * fc * time)
    )    
    
    rms = np.sqrt(np.mean(np.power(signal, 2)))
    ampl = 0.00002 * np.power(10, dB / 20) / rms
    signal = signal * ampl
    return signal, time




# Test signal parameters as input for roughness calculation
# (reference values from 'ref' script)
signal = np.zeros((20), dtype=dict)

signal[0] = {
    "fmod": 20,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 20 Hz",
    "R": np.array([0.234, 0.211, 0.197, 0.234, 0.186, 0.184, 0.0909]),
}
signal[1] = {
    "fmod": 30,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 30 Hz",
    "R": np.array([0.305, 0.38, 0.375, 0.46, 0.348, 0.327, 0.168]),
}
signal[2] = {
    "fmod": 40,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 40 Hz",
    "R": np.array([0.285, 0.471, 0.536, 0.701, 0.52, 0.477, 0.248]),
}
signal[3] = {
    "fmod": 50,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 50 Hz",
    "R": np.array([0.232, 0.461, 0.636, 0.898, 0.668, 0.605, 0.319]),
}
signal[4] = {
    "fmod": 60,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 60 Hz",
    "R": np.array([0.174, 0.384, 0.633, 0.977, 0.744, 0.675, 0.359]),
}
signal[5] = {
    "fmod": 70,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 70 Hz",
    "R": np.array([0.138, 0.321, 0.594, 1, 0.787, 0.721, 0.386]),
}
signal[6] = {
    "fmod": 80,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 80 Hz",
    "R": np.array([0.105, 0.258, 0.514, 0.92, 0.754, 0.698, 0.372]),
}
signal[7] = {
    "fmod": 90,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 90 Hz",
    "R": np.array([0.0808, 0.209, 0.434, 0.801, 0.678, 0.629, 0.324]),
}
signal[8] = {
    "fmod": 100,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 100 Hz",
    "R": np.array([0.0631, 0.172, 0.366, 0.685, 0.599, 0.551, 0.272]),
}
signal[9] = {
    "fmod": 120,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 120 Hz",
    "R": np.array([0.0406, 0.12, 0.27, 0.501, 0.464, 0.426, 0.193]),
}
signal[10] = {
    "fmod": 140,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 140 Hz",
    "R": np.array([0.0325, 0.0802, 0.208, 0.376, 0.371, 0.342, 0.145]),
}
signal[11] = {
    "fmod": 160,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 160 Hz",
    "R": np.array([0.0297, 0.0573, 0.155, 0.289, 0.302, 0.28, 0.112]),
}
signal[12] = {
    "fmod": 200,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 200 Hz",
    "R": np.array([0.0469, 0.0365, 0.0925, 0.196, 0.212, 0.207, 0.0771]),
}
signal[13] = {
    "fmod": 300,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 300 Hz",
    "R": np.array([0.174, 0.0296, 0.0305, 0.0912, 0.103, 0.111, 0.0383]),
}
signal[14] = {
    "fmod": 400,
    "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
    "tab": "Test for modulation frequency = 400 Hz",
    "R": np.array([0.0437, 0.0527, 0.0147, 0.0419, 0.0536, 0.0648, 0.021]),
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
    fs = 48000
    level = 70
    mdepth = 1


    # Roughness calculation for each carrier frequency
    R = np.zeros((len(signal["fc"])), dtype=dict)
    for ind_fc in range(len(signal["fc"])):
        f_c = signal["fc"][ind_fc]
        f_mod = signal["fmod"]
        stimulus, _ = signal_test(
            f_c, f_mod, mdepth, fs, duration, level
        )
        _, _, roughness = roughness_ecma(stimulus, fs)
        R[ind_fc] = roughness

    # Check compliance
    tst = _check_compliance(R, signal)

    return tst


def _check_compliance(R, signal):
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
    plt.plot(fc, tol_curve_max, color="red",
             linestyle="solid", label="", linewidth=1)
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
        "./validations/sq_metrics/roughness_ecma/output/"
        + "validation_roughness_ecma_fmod"
        + str(signal["fmod"])
        + "Hz"
        + ".png",
        format="png",
    )
    plt.clf()
    return tst


# test de la fonction
if __name__ == "__main__":
    for i in range(15):
        validation_roughness(signal[i])
