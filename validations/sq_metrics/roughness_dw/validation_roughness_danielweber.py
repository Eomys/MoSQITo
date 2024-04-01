# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.sq_metrics import roughness_dw
from mosqito.utils.am_sine_wave_generator import am_sine_wave_generator
from input.references import ref_zf, ref_dw

from mosqito import COLORS as clr


# # Test signal parameters as input for roughness calculation
# # (reference values from 'ref' script)
# signal = np.zeros((20), dtype=dict)

# signal[0] = {
#     "fmod": 20,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 20 Hz",
#     "R": np.array([0.232, 0.246, 0.243, 0.24, 0.219, 0.168, 0.108]),
# }
# signal[1] = {
#     "fmod": 30,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 30 Hz",
#     "R": np.array([0.334, 0.4, 0.408, 0.431, 0.385, 0.3, 0.192]),
# }
# signal[2] = {
#     "fmod": 40,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 40 Hz",
#     "R": np.array([0.327, 0.481, 0.584, 0.65, 0.55, 0.431, 0.275]),
# }
# signal[3] = {
#     "fmod": 50,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 50 Hz",
#     "R": np.array([0.253, 0.471, 0.672, 0.846, 0.717, 0.553, 0.358]),
# }
# signal[4] = {
#     "fmod": 60,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 60 Hz",
#     "R": np.array([0.193, 0.394, 0.67, 0.958, 0.81, 0.628, 0.421]),
# }
# signal[5] = {
#     "fmod": 70,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 70 Hz",
#     "R": np.array([0.151, 0.314, 0.609, 0.991, 0.84, 0.652, 0.436]),
# }
# signal[6] = {
#     "fmod": 80,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 80 Hz",
#     "R": np.array([0.115, 0.248, 0.51, 0.955, 0.809, 0.625, 0.415]),
# }
# signal[7] = {
#     "fmod": 90,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 90 Hz",
#     "R": np.array([0.093, 0.199, 0.42, 0.868, 0.743, 0.563, 0.376]),
# }
# signal[8] = {
#     "fmod": 100,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 100 Hz",
#     "R": np.array([0.078, 0.169, 0.356, 0.754, 0.633, 0.487, 0.327]),
# }
# signal[9] = {
#     "fmod": 110,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 110 Hz",
#     "R": np.array([0.067, 0.144, 0.302, 0.646, 0.545, 0.422, 0.28]),
# }
# signal[10] = {
#     "fmod": 120,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 120 Hz",
#     "R": np.array([0.059, 0.126, 0.264, 0.564, 0.47, 0.359, 0.243]),
# }
# signal[11] = {
#     "fmod": 130,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 130 Hz",
#     "R": np.array([0.051, 0.108, 0.234, 0.493, 0.414, 0.317, 0.214]),
# }
# signal[12] = {
#     "fmod": 140,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 140 Hz",
#     "R": np.array([0.041, 0.096, 0.205, 0.429, 0.362, 0.281, 0.189]),
# }
# signal[13] = {
#     "fmod": 150,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 150 Hz",
#     "R": np.array([0.04, 0.085, 0.176, 0.387, 0.327, 0.25, 0.169]),
# }
# signal[14] = {
#     "fmod": 160,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 160 Hz",
#     "R": np.array([0.036, 0.075, 0.164, 0.344, 0.296, 0.227, 0.154]),
# }
# signal[15] = {
#     "fmod": 180,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 180 Hz",
#     "R": np.array([0.029, 0.061, 0.142, 0.288, 0.239, 0.183, 0.122]),
# }
# signal[16] = {
#     "fmod": 200,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 200 Hz",
#     "R": np.array([0.024, 0.05, 0.119, 0.238, 0.201, 0.153, 0.102]),
# }
# signal[17] = {
#     "fmod": 220,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 220 Hz",
#     "R": np.array([0.02, 0.043, 0.096, 0.2, 0.171, 0.13, 0.085]),
# }
# signal[18] = {
#     "fmod": 240,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 240 Hz",
#     "R": np.array([0.018, 0.037, 0.08, 0.174, 0.147, 0.111, 0.074]),
# }
# signal[19] = {
#     "fmod": 260,
#     "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
#     "tab": "Test for modulation frequency = 260 Hz",
#     "R": np.array([0.017, 0.033, 0.069, 0.153, 0.129, 0.098, 0.063]),
# }


def validation_roughness_dw(fc):
    """Validation function for the roughness calculation of an audio signal

    Validation function for the function roughness_dw. The input signals are
    chosen according to the article "Psychoacoustical roughness: 
    implementation of an optimized model" by Daniel and Weber in 1997.
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
    duration = 1.5
    fs = 48000
    level = 60
    mdepth = 1
    
    fm_vector = np.array([30,40,50,60,70,80,90,100,120,140,160])
    n = len(fm_vector)

    # Overlapping definition for roughness calculation
    overlap = 0
    
    # Roughness calculation for each carrier frequency
    R_dw = np.zeros((n))
    R_ref_zf = np.zeros((n))
    R_ref_dw = np.zeros((n)) 
    
    for i, f_mod in enumerate(fm_vector):
        stimulus = am_sine_wave_generator(duration, fs, fc, f_mod, mdepth , level)
        roughness, _, _, _ = roughness_dw(stimulus, fs, overlap)
        R_dw[i] = roughness[0]
        R_ref_zf[i] = ref_zf(fc, f_mod)
        R_ref_dw[i] = ref_dw(fc, f_mod)


    # Check compliance
    tst = _check_compliance(fc, fm_vector, R_dw, R_ref_zf, R_ref_dw)

    return tst


def _check_compliance(fc, fm_vector, R_dw, R_ref_zf, R_ref_dw):
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

    # Test for comformance (17% tolerance)

    tst = (R_dw >= R_ref_zf -0.1).all() and (R_dw <= R_ref_zf +0.1).all()

    # Find the highest difference
    diff = 0
    ind = 0
    for i in range(R_dw.size):
        d = (np.abs(R_dw[i] - R_ref_dw[i]) / R_ref_dw[i]) * 100
        if d > diff:
            diff = d
        if d <= 30:
            ind += 1

    # Give indication about the difference
    prop = round(ind / len(R_ref_zf) * 100)

    # Comparison plot
    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    
    ax.loglog(fm_vector, R_ref_zf, '--', linewidth=2, color=clr[2],
               label='Fastl & Zwicker [interp]')
    ax.loglog(fm_vector, R_ref_zf-0.1, ':', linewidth=1, color=clr[2],
               label='17% tolerance')
    ax.loglog(fm_vector, R_ref_zf+0.1, ':', linewidth=1, color=clr[2])
    ax.loglog(fm_vector, R_dw, 'o', color=clr[0], markersize=7,
               label='MoSQITo [Daniel and Weber]')
    ax.loglog(fm_vector, R_ref_dw, 's', fillstyle='none', linewidth=1.5, color='#666666',
               label='Reference from the article')
    
    ax.legend()
    ax.grid(which='both')
    
    ax.set_yticks(ticks=[0.1, 0.2, 0.5, 1.],
               labels=['0.1', '0.2', '0.5', '1'])
    ax.set_xticks(ticks=[10, 20, 50, 100, 200, 400],
               labels=['10', '20', '50', '100', '200', '400'])
    
    ax.set_xlim([10, 200])
    ax.set_ylim([0.01, 1.2])
    ax.set_xlabel(r'Modulation Frequency $f_m$ [Hz]', fontsize=13)
    ax.set_ylabel('Roughness [asper]', fontsize=13)
    ax.set_title(rf'Roughness for AM sine wave, $f_c$={fc} Hz', fontsize=14)
    
    if tst:
        plt.text( 0.5, 0.5, "Test passed (0.1 asper tolerance not exceeded)", fontsize=13,
            horizontalalignment="center", verticalalignment="center",
            transform=plt.gca().transAxes, bbox=dict(facecolor=clr[5], alpha=0.3))
    else:
        plt.text(0.5, 0.5, "Test not passed", fontsize=13,
                 horizontalalignment="center", verticalalignment="center",
                 transform=plt.gca().transAxes, bbox=dict(facecolor=clr[1], alpha=0.3))    
    
    plt.tight_layout()
    plt.savefig(
        "./validations/sq_metrics/roughness_dw/output/"
        + "validation_roughness_dw_fc"
        +  f'{fc}'
        + "Hz"
        + ".png",
        format="png",
    )
    # plt.show(block=True)
    plt.clf()
    
    return tst





# test de la fonction
if __name__ == "__main__":
    fc_vector = np.array([125, 250, 500, 1000, 2000, 4000, 8000])
    for fc in fc_vector:
        validation_roughness_dw(fc)
