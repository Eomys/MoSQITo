# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.sq_metrics import roughness_ecma
from mosqito.utils.am_sine_generator import am_sine_generator
from input.references import ref_zf, ref_ecma

from mosqito import COLORS as clr

def validation_roughness_ecma(fc):
    """Validation function for the roughness calculation of an audio signal
    according to ECMA 418-2 (2nd edition, 2022).

    Validation function for the function roughness_ecma. The input signals are generated
    according to the annex C of ECMA 418-2 (2nd edition, 2022). One .png compliance plot 
    is generated to compare the results with the standard's references.

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
    time = np.linspace(0, duration, int(duration*fs))
    level = 60
    mdepth = 1

    fm_vector = np.array([20,30,40,50,60,70,80,90,100,120,140,160,200, 250])
    n = len(fm_vector)
    
    # Roughness calculation for each carrier frequency
    R_ecma = np.zeros((n), dtype=dict)
    R_ref_zf = np.zeros((n), dtype=dict)
    R_ref_ecma = np.zeros((n), dtype=dict)
    
    for i, f_mod in enumerate(fm_vector):
        xmod = np.sin(2 * np.pi * fm_vector[i] * time)
        stimulus, _ = am_sine_generator(xmod, fs, fc, level)
        R_ecma[i], _, _, _, _ = roughness_ecma(stimulus, fs)
        R_ref_zf[i] = ref_zf(fc, f_mod)
        R_ref_ecma[i] = ref_ecma(fc, f_mod)
        
    # # Check compliance
    tst = _check_compliance(fc, fm_vector, R_ecma, R_ref_zf, R_ref_ecma)

    return tst


def _check_compliance(fc, fm_vector, R_ecma, R_ref_zf, R_ref_ecma):
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

    # Test for comformance (0.1 absolute tolerance with zwicker and fastl and 10% relative tolerance with ecma
    tst = ((R_ecma < R_ref_zf + 0.1).all()
                and (R_ecma > R_ref_zf - 0.1).all())
    

    # Find the highest difference
    diff = 0
    ind = 0
    for i in range(R_ecma.size):
        d = (np.abs(R_ecma[i] - R_ref_ecma[i]) / R_ref_ecma[i]) * 100
        if d > diff:
            diff = d
        if d <= 30:
            ind += 1

    # Comparison plot
    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    
    ax.loglog(fm_vector, R_ref_zf, '--', linewidth=2, color=clr[2],
               label='Fastl & Zwicker [interp]')
    ax.loglog(fm_vector, R_ref_zf+0.1, ':', linewidth=1, color=clr[2],
               label='0.1 asper tolerance')
    ax.loglog(fm_vector, R_ref_zf-0.1, ':', linewidth=1, color=clr[2])
    ax.loglog(fm_vector, R_ecma, 'o', color=clr[0], markersize=7,
               label='MoSQITo [ECMA-418-2]')
    ax.loglog(fm_vector, R_ref_ecma, 's', fillstyle='none', linewidth=1.5, color='#666666',
               label='Reference from standard [ECMA-418-2]')
    
    ax.legend()
    ax.grid(which='both')
    
    ax.set_yticks(ticks=[0.1, 0.2, 0.5, 1.],
               labels=['0.1', '0.2', '0.5', '1'])
    ax.set_xticks(ticks=[10, 20, 50, 100, 200, 400],
               labels=['10', '20', '50', '100', '200', '400'])
    
    ax.set_xlim([10, 300])
    ax.set_ylim([0.07, 1.2])
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
        "./validations/sq_metrics/roughness_ecma/output/"
        + "validation_roughness_ecma_fc"
        +  f'{fc}'
        + "Hz"
        + ".png",
        format="png",
    )
    plt.clf()
    
    return tst


# test de la fonction
if __name__ == "__main__":
    fc_vector = np.array([125, 250, 500, 1000, 2000, 4000, 8000])
    for fc in fc_vector:
        validation_roughness_ecma(fc)
