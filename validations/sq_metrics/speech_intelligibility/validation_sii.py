# -*- coding: utf-8 -*-

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise RuntimeError(
        "In order to perform this validation you need the 'matplotlib' package."
    )

# Third party imports
from numpy import array, empty, amin, amax, zeros, log10, maximum, float64

# Local application imports
from mosqito.sq_metrics.speech_intelligibility._band_procedure_data import  _get_third_octave_band_data
from mosqito.sq_metrics.speech_intelligibility._main_sii import _main_sii

# Reference values from ANSI S3.5 standard
reference = empty(2, dtype=dict)

reference[0] = {"noise_spectrum": array([70, 65, 45, 25, 1, -15]),
    "speech_spectrum": array([50, 40, 40, 30, 20, 0]),         
    "freq_axis": array([250, 500, 1000, 2000, 4000, 8000]),
    "method": "octave",
    "SII": 0.504,
    "SII_spec": array([0, 0, 0.08, 0.17, 0.21, 0.04]),
}


reference[1] = {"noise_spectrum": array([
        40,
        30,
        20,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0    ]
), 
    "speech_spectrum": array([
        54,
        54,
        54,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0    ]
),         
    "freq_axis": array(        [
        160,
        200,
        250,
        315,
        400,
        500,
        630,
        800,
        1000,
        1250,
        1600,
        2000,
        2500,
        3150,
        4000,
        5000,
        6300,
        8000
        ]
),
    "method": "third_octave",
    "SII_spec": array([40,34.66,25.04]),
}


def validation_sii_octave(reference):
    """Test function for the script _main_sii with octave band procedure

    Test function for the script sii_freq with reference arrays as input.
    The input files are provided by ANSI S3.5-1997.
    The compliance is assessed according with a 1% tolerance.
    One .png compliance plot is generated.

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
    
def validation_sii_third_octave(reference):
    """Test function for the script _main_sii with third octave band procedure

    Test function for the script sii_freq with reference arrays as input.
    The input files are provided by ANSI S3.5-1997.
    The compliance is assessed according with a 1% tolerance.
    One .png compliance plot is generated.

    """
    
    noise_spectrum = reference["noise_spectrum"]
    speech_spectrum = reference["speech_spectrum"]
    
    # Get band data for third-octave procedure
    CENTER_FREQUENCIES, _, _, BANDWIDTH_ADJUSTEMENT, _, _, _ = _get_third_octave_band_data()
    nbands = len(CENTER_FREQUENCIES)
    
    T = zeros((nbands))
        
    # STEP 3
    V = speech_spectrum - 24
    B = maximum(noise_spectrum, V)
    C = -80 + 0.6 * (B + 10*log10(CENTER_FREQUENCIES)-6.353)
    Z = zeros((nbands))
    for i in range(nbands): 
        s = 0
        for k in range(i):
            s += 10**(0.1*(B[k] + 3.32 * C[k] * log10(0.89 * CENTER_FREQUENCIES[i] / CENTER_FREQUENCIES[k])))
        Z[i] = 10 * log10(10**(0.1*noise_spectrum[i]) + s)
    # 4.3.2.4
    Z[0] = B[0]
    
    plt.figure()
    
    # Frequency bark axis
    freqs = reference["freq_axis"]

    tstS = (Z[:3] >= amin([reference["SII_spec"] * 0.99, reference["SII_spec"] - 0.01], axis=0)).all() and (
       Z[:3] <= amax([reference["SII_spec"] * 1.01, reference["SII_spec"] + 0.01], axis=0)
    ).all()

    # Tolerance curves definition
    tol_low = amin([reference["SII_spec"] * 0.99, reference["SII_spec"] - 0.01], axis=0)
    tol_high = amax([reference["SII_spec"] * 1.01, reference["SII_spec"] + 0.01], axis=0)

    # Plot tolerance curves
    plt.plot(
        freqs[:3], tol_low, color="red", linestyle="solid", label="tolerance", linewidth=1
    )
    plt.plot(freqs[:3], tol_high, color="red", linestyle="solid", linewidth=1)

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
    plt.plot(freqs[:3], Z[:3], label="MOSQITO")
    plt.title("Equivalent noise spectrum \n Third-octave band procedure", fontsize=10)
    plt.legend()
    plt.xlabel("Center frequency [Hz]")
    plt.ylabel("Amplitude [dB]")
    plt.savefig(
        "validations/sq_metrics/speech_intelligibility/output/"
        + "validation_equivalent_noise_spectrum.png",
        format="png",
    )
    plt.clf()


# test de la fonction
if __name__ == "__main__":
    # generate compliance plot 
    validation_sii_octave(reference[0])
    validation_sii_third_octave(reference[1])
