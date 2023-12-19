# -*- coding: utf-8 -*-

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )

# Third party imports
from numpy import array, empty, amin, amax

# Local application imports
from mosqito.sq_metrics.speech_intelligibility._main_sii import _main_sii

# Reference values from ANSI S3.5 standard
reference = {"noise_spectrum": array([70, 65, 45, 25, 1, -15]),
    "speech_spectrum": array([50, 40, 40, 30, 20, 0]),         
    "freq_axis": array([250, 500, 1000, 2000, 4000, 8000]),
    "method": "octave",
    "SII": 0.504,
    "SII_spec": array([0, 0, 0.08, 0.17, 0.21, 0.04]),
}


def validation_sii(reference):
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
    # Compute SII
    SII, SII_spec, _ = _main_sii(reference["method"], reference["speech_spectrum"], reference["noise_spectrum"], threshold=None)

    plt.figure()

    # Frequency bark axis
    freqs = reference["freq_axis"]

    tstS = (SII_spec >= amin([reference["SII_spec"] * 0.99, reference["SII_spec"] - 0.01], axis=0)).all() and (
        SII_spec <= amax([reference["SII_spec"] * 1.01, reference["SII_spec"] + 0.01], axis=0)
    ).all()

    # Tolerance curves definition
    tol_low = amin([reference["SII_spec"] * 0.99, reference["SII_spec"] - 0.01], axis=0)
    tol_high = amax([reference["SII_spec"] * 1.01, reference["SII_spec"] + 0.01], axis=0)

    # Plot tolerance curves
    plt.plot(
        freqs, tol_low, color="red", linestyle="solid", label="tolerance", linewidth=1
    )
    plt.plot(freqs, tol_high, color="red", linestyle="solid", linewidth=1)

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
    plt.plot(freqs, SII_spec, label="MOSQITO")
    plt.title("Speech intelligibility index = "+f"{SII:.3f}"+"\n Octave band procedure", fontsize=10)
    plt.legend()
    plt.xlabel("Center frequency [Hz]")
    plt.ylabel("Specific SII")
    plt.savefig(
        "validations/sq_metrics/speech_intelligibility/output/"
        + "validation_sii.png",
        format="png",
    )
    plt.clf()


# test de la fonction
if __name__ == "__main__":
    # generate compliance plot 
    validation_sii(reference)
