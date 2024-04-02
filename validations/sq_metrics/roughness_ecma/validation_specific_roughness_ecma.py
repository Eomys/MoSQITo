
# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.sq_metrics import roughness_ecma
from mosqito.sq_metrics.loudness.loudness_ecma._auditory_filters_centre_freq import _auditory_filters_centre_freq

from mosqito.utils.am_sine_wave_generator import am_sine_wave_generator

from input.references_specific import ref_artemis

from mosqito import COLORS as clr

def validation_specific_roughness_ecma(fc, fmod, ref_file):
    """Validation function for the roughness calculation of an audio signal
    according to ECMA 418-2 (2nd edition, 2022).

    Validation function for the function roughness_ecma. The input signals are generated
    according to the annex C of ECMA 418-2 (2nd edition, 2022). One .png compliance plot 
    is generated to compare the results with the references computed with the Artemis suite.
    """
    
    # Stimulus parameters
    duration = 1.5
    fs = 48000
    level = 65
    mdepth = 1

    # Stimulus generation
    stimulus = am_sine_wave_generator(duration, fs, fc, fmod, mdepth , level)
    
    # Roughness calculation 
    R_ecma, _, R_spec, _, _ = roughness_ecma(stimulus, fs)
    R_spec_ref, _ = ref_artemis(ref_file, fc, fmod)
        
    # Check compliance
    tst = _check_compliance(fc, fmod, R_spec, np.squeeze(np.array(R_spec_ref)))    

    return tst


def _check_compliance(fc, fmod, R_spec, ref):
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

    R_spec_ref = ref[:,1]

    # Test for comformance (0.1 absolute tolerance with zwicker and fastl and 10% relative tolerance with ecma
    tst = ((R_spec < R_spec_ref*1.1).all()
                and (R_spec > R_spec_ref*0.9).all())

    # Comparison plot
    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    
    x_axis = _auditory_filters_centre_freq()
    
    ax.step(x_axis, R_spec_ref, '--', linewidth=2, color=clr[2],
               label='Reference from Artemis')
    ax.step(x_axis, R_spec_ref*1.1, ':', linewidth=1, color=clr[2],
               label='10% tolerance')
    ax.step(x_axis, R_spec_ref*0.9, ':', linewidth=1, color=clr[2])
    ax.step(x_axis, R_spec, color=clr[0], label='MOSQITO [ECMA-418-2]')
    
    ax.legend()
    ax.grid(which='both')    
    ax.set_xlim(0,3000)
    ax.set_xlabel('Frequency [Hz]', fontsize=13)
    ax.set_ylabel('Specific roughness [asper/bark]', fontsize=13)
    ax.set_title(r'Roughness for AM sine wave, $f_c$=' +f'{fc}' + r"Hz, $f_{mod}$=" + f'{fmod}' +'Hz ', fontsize=14)
        
    plt.tight_layout()
    plt.savefig(
        "./validations/sq_metrics/roughness_ecma/output/"
        + "validation_roughness_ecma_fc"
        +  f'{fc}'+ "Hz" 
        + f'{fmod}'+ "Hz" 
        + ".png",
        format="png",
    )
    plt.clf()
    
    
    return tst






# test de la fonction
if __name__ == "__main__":
    
    ref_file = r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_ecma\input\validation_specific_roughness_ecma.xlsx"
    fc = 1000
    fm_vector = np.array([40,70,120])
    for fmod in fm_vector:
        validation_specific_roughness_ecma(1000, fmod, ref_file)
        
        