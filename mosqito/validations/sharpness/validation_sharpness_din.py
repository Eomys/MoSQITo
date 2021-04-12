# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:36:37 2020

@author: wantysal
"""

# Third party imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.functions.sharpness.comp_sharpness import comp_sharpness
from mosqito.functions.shared.load import load

# Signals and results from DIN 45692_2009E, chapter 6
broadband = np.zeros((20), dtype=dict)

broadband[0] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_250.wav",
    "type": "Broad-band",
    "S": 2.70,
}
broadband[1] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_350.wav",
    "S": 2.74,
}
broadband[2] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_450.wav",
    "S": 2.78,
}
broadband[3] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_570.wav",
    "S": 2.85,
}
broadband[4] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_700.wav",
    "S": 2.91,
}
broadband[5] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_840.wav",
    "S": 2.96,
}
broadband[6] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_1000.wav",
    "S": 3.05,
}
broadband[7] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_1170.wav",
    "S": 3.12,
}
broadband[8] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_1370.wav",
    "S": 3.20,
}
broadband[9] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_1600.wav",
    "S": 3.30,
}
broadband[10] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_1850.wav",
    "S": 3.42,
}
broadband[11] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_2150.wav",
    "S": 3.53,
}
broadband[12] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_2500.wav",
    "S": 3.69,
}
broadband[13] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_2900.wav",
    "S": 3.89,
}
broadband[14] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_3400.wav",
    "S": 4.12,
}
broadband[15] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_4000.wav",
    "S": 4.49,
}
broadband[16] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_4800.wav",
    "S": 5.04,
}
broadband[17] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_5800.wav",
    "S": 5.69,
}
broadband[18] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_7000.wav",
    "S": 6.47,
}
broadband[19] = {
    "data_file": r".\mosqito\validations\sharpness\data\broadband_8500.wav",
    "S": 7.46,
}

# Test signal as input for sharpness (from DIN 45692)

narrowband = np.zeros((21), dtype=dict)

narrowband[0] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_250.wav",
    "type": "Narrow-band",
    "S": 0.38,
}
narrowband[1] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_350.wav",
    "S": 0.49,
}
narrowband[2] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_450.wav",
    "S": 0.6,
}
narrowband[3] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_570.wav",
    "S": 0.71,
}
narrowband[4] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_700.wav",
    "S": 0.82,
}
narrowband[5] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_840.wav",
    "S": 0.93,
}
narrowband[6] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_1000.wav",
    "S": 1.00,
}
narrowband[7] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_1170.wav",
    "S": 1.13,
}
narrowband[8] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_1370.wav",
    "S": 1.26,
}
narrowband[9] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_1600.wav",
    "S": 1.35,
}
narrowband[10] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_1850.wav",
    "S": 1.49,
}
narrowband[11] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_2150.wav",
    "S": 1.64,
}
narrowband[12] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_2500.wav",
    "S": 1.78,
}
narrowband[13] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_2900.wav",
    "S": 2.06,
}
narrowband[14] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_3400.wav",
    "S": 2.40,
}
narrowband[15] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_4000.wav",
    "S": 2.82,
}
narrowband[16] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_4800.wav",
    "S": 3.48,
}
narrowband[17] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_5800.wav",
    "S": 4.43,
}
narrowband[18] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_7000.wav",
    "S": 5.52,
}
narrowband[19] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_8500.wav",
    "S": 6.81,
}
narrowband[20] = {
    "data_file": r".\mosqito\validations\sharpness\data\narrowband_10500.wav",
    "S": 8.55,
}


def validation_sharpness(noise):
    """Test function for the script sharpness_din

    Test function for the script sharpness_din with .wav filesas input.
    The input files are provided by DIN 45692_2009E
    The compliance is assessed according to chapter 6 of the standard.
    One .png compliance plot is generated.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    sharpness = np.zeros((len(noise)))
    reference = np.zeros((len(noise)))

    for i in range(len(noise)):
        # Load signal
        sig, fs = load(True, noise[i]["data_file"], calib=1)

        # Compute sharpness
        S = comp_sharpness(True, sig, fs, method="din")
        sharpness[i] = S["values"]

        # Load reference value
        reference[i] = noise[i]["S"]

    noise_type = noise[0]["type"]

    check_compliance(sharpness, reference, noise_type)


def check_compliance(sharpness, reference, noise_type):
    """Check the compliance of sharpness calc. to DIN 45692

    The compliance is assessed according to chapter 6 of the
    standard DIN 45692_2009E.
    One .png compliance plot is generated.


    Parameters
    ----------
    sharpness : numpy.array
        computed sharpness values
    reference : numpy.array
        reference sharpness values


    Outputs
    -------
    tst : bool
        Compliance to the reference data
    """
    plt.figure()

    # Frequency bark axis
    barks = np.arange(2.5, len(sharpness) + 2.5, 1)

    # Test for DIN 45692_2009E comformance (chapter 6)
    S = sharpness
    tstS = (S >= np.amin([reference * 0.95, reference - 0.05], axis=0)).all() and (
        S <= np.amax([reference * 1.05, reference + 0.05], axis=0)
    ).all()

    # Tolerance curves definition
    tol_low = np.amin([reference * 0.95, reference - 0.05], axis=0)
    tol_high = np.amax([reference * 1.05, reference + 0.05], axis=0)

    # Plot tolerance curves
    plt.plot(
        barks, tol_low, color="red", linestyle="solid", label="tolerance", linewidth=1
    )
    plt.plot(barks, tol_high, color="red", linestyle="solid", linewidth=1)

    if tstS:
        plt.text(
            0.5,
            0.5,
            "Test passed ",
            horizontalalignment="center",
            verticalalignment="center",
            transform=plt.gca().transAxes,
            bbox=dict(facecolor="green", alpha=0.3),
        )

    else:
        plt.text(
            0.5,
            0.5,
            "Test not passed",
            horizontalalignment="center",
            verticalalignment="center",
            transform=plt.gca().transAxes,
            bbox=dict(facecolor="red", alpha=0.3),
        )

    # Plot the calculated sharpness
    plt.plot(barks, sharpness, label="MOSQITO")
    plt.title("Sharpness of " + noise_type + " noises", fontsize=10)
    plt.legend()
    plt.xlabel("Center frequency [bark]")
    plt.ylabel("Sharpness, [acum]")

    plt.savefig(
        "./mosqito/validations/sharpness/output/"
        + "validation_sharpness_"
        + noise_type
        + "_noise"
        + ".png",
        format="png",
    )
    plt.clf()


# test de la fonction
if __name__ == "__main__":

    # generate compliance plot for broadband noise
    validation_sharpness(broadband)
    validation_sharpness(narrowband)
