# -*- coding: utf-8 -*-

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )

# Third party imports
import numpy as np

# Local application imports
from mosqito.sq_metrics import sii_freq


# Reference values from ANSI S3.5 standard
reference = np.empty((3))

reference[0] = {"spectrum": "input/broadband_250.wav",
    "method": "critica",
    "speech_level": "normal",
    "SII": 0.67,
}


def validation_sii(noise):
    """Test function for the script sii_freq

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

    SII = np.zeros((len(noise)))
    reference = np.zeros((len(noise)))

    for i in range(len(noise)):
        # Compute SII
        SII[i], _, _ = sii_freq(reference[i]["spectrum"], reference[i]["method"], reference[i]["speech_level"] )

        # Load reference value
        reference[i] = reference[i]["SII"]


    _check_compliance(SII, reference)


def _check_compliance(sharpness, reference):
    """Check the compliance of sharpness calc. to ANSI S3.5

    The compliance is assessed with an absolute 1% tolerance.
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
    tstS = (S >= np.amin([reference * 0.99, reference - 0.01], axis=0)).all() and (
        S <= np.amax([reference * 1.01, reference + 0.01], axis=0)
    ).all()

    # Tolerance curves definition
    tol_low = np.amin([reference * 0.99, reference - 0.01], axis=0)
    tol_high = np.amax([reference * 1.01, reference + 0.01], axis=0)

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
    plt.title("Speech intelligibility index for the 3 test signals", fontsize=10)
    plt.legend()
    plt.xlabel("Center frequency [bark]")
    plt.ylabel("Sharpness, [acum]")

    plt.savefig(
        "output/"
        + "validation_sii_"
        + ".png",
        format="png",
    )
    plt.clf()


# test de la fonction
if __name__ == "__main__":
    # generate compliance plot 
    validation_sii()
