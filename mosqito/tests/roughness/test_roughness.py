# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 13:41:37 2020

@author: wantysal
"""

import sys
sys.path.append('../../..')

#Standard imports
import numpy as np
import matplotlib.pyplot as plt
import pytest

# Local application imports
from mosqito.functions.roughness_danielweber.comp_roughness import comp_roughness
from mosqito.tests.roughness.test_signals_generation import test_signal


@pytest.mark.roughness_dw  # to skip or run only Daniel and Weber roughness tests
@pytest.mark.parametrize(
    # Test signal parameters as input for roughness
    # (reference values from 'ref' script)
    "signal",
    [
        {
            "fmod": 20,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 20 Hz",
            "R": np.array([0.232, 0.241, 0.243, 0.240, 0.202, 0.160, 0.107]),
        },
        {
            "fmod": 30,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 30 Hz",
            "R": np.array([0.335, 0.399, 0.421, 0.431, 0.364, 0.283, 0.193]),
        }, 
        {
            "fmod": 40,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 40 Hz",
            "R": np.array([0.327, 0.485, 0.589, 0.650, 0.545, 0.425, 0.288]),
        },
        {
            "fmod": 50,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 50 Hz",
            "R": np.array([0.252, 0.468, 0.672, 0.846, 0.717, 0.553, 0.372]),
        },
        {
            "fmod": 60,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 60 Hz",
            "R": np.array([0.215, 0.396, 0.67, 0.958, 0.81, 0.628, 0.421]),
        },
        {
            "fmod": 70,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 70 Hz",
            "R": np.array([0.181, 0.31, 0.609, 0.991, 0.84, 0.652, 0.436]),
        },
        {
            "fmod": 80,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 80 Hz",
            "R": np.array([0.146, 0.269, 0.51, 0.955, 0.811, 0.625, 0.415]),
        },
        {
            "fmod": 90,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 90 Hz",
            "R": np.array([0.112, 0.244, 0.42, 0.868, 0.731, 0.563, 0.376]),
        },
        {
            "fmod": 100,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 100 Hz",
            "R": np.array([0.078, 0.219, 0.356, 0.754, 0.633, 0.487, 0.327]),
        },
        {
            "fmod": 110,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 110 Hz",
            "R": np.array([0.075, 0.194, 0.302, 0.646, 0.545, 0.422, 0.28]),
        },
        {
            "fmod": 120,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 120 Hz",
            "R": np.array([0.075, 0.17, 0.264, 0.564, 0.47, 0.359, 0.243]),
        },
        {
            "fmod": 130,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 130 Hz",
            "R": np.array([0.075, 0.145, 0.234, 0.493, 0.414, 0.317, 0.214]),
        },
        {
            "fmod": 140,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 140 Hz",
            "R": np.array([0.075, 0.12, 0.205, 0.429, 0.362, 0.281, 0.189]),
        },
        {
            "fmod": 150,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 150 Hz",
            "R": np.array([0.075, 0.096, 0.176, 0.387, 0.327, 0.25, 0.169]),
        },
        {
            "fmod": 160,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 160 Hz",
            "R": np.array([0.075, 0.077, 0.164, 0.344, 0.296, 0.227, 0.154]),
        },
        {
            "fmod": 180,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 180 Hz",
            "R": np.array([0.075, 0.077, 0.142, 0.288, 0.239, 0.183, 0.122]),
        },
        {
            "fmod": 200,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 200 Hz",
            "R": np.array([0.075, 0.077, 0.119, 0.238, 0.201, 0.153, 0.102]),
        },
        {
            "fmod": 220,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 220 Hz",
            "R": np.array([0.075, 0.077, 0.096, 0.2, 0.171, 0.13, 0.085]),
        },
        {
            "fmod": 240,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 240 Hz",
            "R": np.array([0.075, 0.077, 0.087, 0.174, 0.147, 0.111, 0.085]),
        },
        {
            "fmod": 260,
            "fc": [125, 250, 500, 1000, 2000, 4000, 8000],
            "tab": "Test for modulation frequency = 260 Hz",
            "R": np.array([0.075, 0.077, 0.087, 0.153, 0.129, 0.098, 0.085]),
        },


    ],
    )
   
@pytest.mark.roughness_dw  # to skip or run only Daniel and Weber roughness tests
def test_roughness(signal):
    """Test function for the roughness calculation of a audio signal

    Test function for the Audio_signal class "comp_roughness" method with signal array 
    as input. The input signals are chosen according to the article "Psychoacoustical 
    roughness: implementation of an optimized model" by Daniel and Weber in 1997.
    The figure 3 is used to compare amplitude-modulated signals created according to 
    their carrier frequency and modulation frequency to the article results.
    The test are done with 50% overlapping time windows as described in the article.
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
    R = np.zeros((len(signal['fc'])))           
    for ind_fc in range(len(signal['fc'])):     
        stimulus = test_signal(signal['fc'][ind_fc], signal['fmod'], mdepth, fs, duration, level)
        R[ind_fc],_ = comp_roughness(stimulus, fs, overlap)
            
    # Check compliance
    tst = check_compliance(R, signal)
    
    assert tst
    

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

    ref = signal['R']     

    # Test for comformance (17% tolerance)

    tst = (   (R >= ref * 0.83).all() 
          and (R <= ref * 1.17).all()   )
           
    
    # Define and plot the tolerance curves 
    fc = signal['fc']
    tol_curve_min = ref * 0.83    
    tol_curve_max = ref * 1.17
    plt.plot(fc, tol_curve_min, color='red', linestyle = 'solid', label='17% tolerance', linewidth=1)  
    plt.plot(fc, tol_curve_max, color='red', linestyle = 'solid', label='', linewidth=1) 
    plt.legend()
    
    # Compliance plot   
    plt.plot(fc, R, label="MoSQITo")    
    if tst:
        plt.text(0.5, 0.5, 'Test passed (17% tolerance not exceeded)', horizontalalignment='center',
        verticalalignment='center', transform=plt.gca().transAxes,
        bbox=dict(facecolor='green', alpha=0.3))
    else:
        tst = 0
        plt.text(0.5, 0.5, 'Test not passed', horizontalalignment='center',
        verticalalignment='center', transform=plt.gca().transAxes, 
        bbox=dict(facecolor='red', alpha=0.3))
                
    if tst:
        clr = "green"
    else:
        clr = "red"
    plt.title("Roughness for modulation frequency = " + str(signal['fmod']) + " Hz", color=clr)
    plt.xlabel("Carrier frequency [Hertz]")
    plt.ylabel("Roughness, [Asper]")
    plt.savefig(
        r"mosqito\tests\roughness\output"
        + "\\test_roughness_dw_fmod" + str(signal['fmod']) + "Hz"
        + ".png",
        format="png",)
    plt.clf()
    return tst


# test de la fonction
if __name__ == "__main__":
    test_roughness(signal)