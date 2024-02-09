# -*- coding: utf-8 -*-

# Standard imports
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
from mosqito.sq_metrics import roughness_dw, roughness_ecma
from input.references import ref_zf, ref_ecma

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






def validation_roughness(fc):
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
    duration = 1
    fs = 48000
    level = 60
    mdepth = 1

    fm_vector = np.array([20,30,40,50,60,70,80,90,100,120,140,160,200])
    n = len(fm_vector)
    
    # Roughness calculation for each carrier frequency
    R_ecma = np.zeros((n), dtype=dict)
    R_dw = np.zeros((n), dtype=dict)
    R_refzf = np.zeros((n), dtype=dict)
    R_refecma = np.zeros((n), dtype=dict)
    
    for i in range(len(fm_vector)):
        stimulus, _ = signal_test(
            fc, fm_vector[i], mdepth, fs, duration, level
        )
        _, _, _, roughness = roughness_ecma(stimulus, fs)
        R_ecma[i] = roughness
        roughness, _, _, _ = roughness_dw(stimulus, fs, overlap=0.5)
        R_dw[i] = np.mean(roughness)
        R_refzf[i] = ref_zf(fc, fm_vector[i])
        R_refecma[i] = ref_ecma(fc, fm_vector[i])
        
    # # Check compliance
    tst = _check_compliance(fc, fm_vector, R_ecma, R_dw, R_refzf, R_refecma)

    return tst


def _check_compliance(fc, fm_vector, R_ecma, R_dw, R_refzf, R_refecma):
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
    tst = ((R_ecma < R_refzf + 0.1).all()
                and (R_ecma > R_refzf - 0.1).all())
    

    # Find the highest difference
    diff = 0
    ind = 0
    for i in range(R_ecma.size):
        d = (np.abs(R_ecma[i] - R_refecma[i]) / R_refecma[i]) * 100
        if d > diff:
            diff = d
        if d <= 30:
            ind += 1


    # Plot
    
    plt.loglog(fm_vector, R_refecma, 'P', linewidth=2, color='k',
               label='Artemis [ECMA 418-2]')

    plt.loglog(fm_vector, R_ecma, 'o', color='#69c3c5', 
               label='MoSQITo [ECMA-418-2]')
    
    plt.loglog(fm_vector, R_dw, 's', fillstyle='none', linewidth=1.5, color='C1',
               label='MoSQITo [Daniel & Weber]')
    
    
    plt.loglog(fm_vector, R_refzf, '--', linewidth=2, color='0.45',
               label='Fastl & Zwicker [interp]')
    plt.loglog(fm_vector, R_refzf+0.1, ':', linewidth=1, color='0.25',
               label='0.1 asper tolerance')
    plt.loglog(fm_vector, R_refzf-0.1, ':', linewidth=1, color='0.25')
    
    
    
    plt.legend()
    plt.grid(which='both')
    
    plt.yticks(ticks=[0.1, 0.2, 0.5, 1.],
               labels=['0.1', '0.2', '0.5', '1'])
    plt.xticks(ticks=[10, 20, 50, 100, 200, 300],
               labels=['10', '20', '50', '100', '200', '300'])
    
    plt.xlim([10, 400])
    plt.ylim([0.07, 2])
    plt.xlabel(r'Modulation Frequency $f_m$ [Hz]', fontsize=13)
    plt.ylabel('Roughness [asper]', fontsize=13)
    plt.title(rf'Roughness for AM sine wave, $f_c$={fc} Hz', fontsize=14)
    
    if tst:
        plt.text( 0.5, 0.5, "Test passed (0.1 asper tolerance not exceeded)", fontsize=13,
            horizontalalignment="center", verticalalignment="center",
            transform=plt.gca().transAxes, bbox=dict(facecolor="green", alpha=0.3))
    else:
        plt.text(0.5, 0.5, "Test not passed", fontsize=13,
                 horizontalalignment="center", verticalalignment="center",
                 transform=plt.gca().transAxes, bbox=dict(facecolor="red", alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('validation_roughness_ecma_fc' + f'{fc}' + 'Hz.png')
    plt.clf()
    return tst


# test de la fonction
if __name__ == "__main__":
    fc_vector = np.array([125, 250, 500, 1000, 2000, 4000, 8000])
    for fc in fc_vector:
        validation_roughness(fc)
