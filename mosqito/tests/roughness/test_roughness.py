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
from mosqito.roughness_daniel_weber import comp_roughness
from mosqito.tests.roughness.test_signals_generation import test_signal
from mosqito.tests.roughness.ref import ref_roughness

@pytest.mark.roughness  # to skip or run only roughness tests
def test_roughness():
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
   
   # Parameters definition for signals generation 
    fs = 48000
    carrier  = np.array([125, 250, 500, 1000, 2000, 4000, 8000])
    fmod     = np.array([10, 20, 30, 40, 50, 60, 70, 80, 100, 150, 200, 400])
    mdepth = 1   
    duration = 2
    dB = 60

    
   # Overlapping definition for roughness calculation
    overlap = 0.5

            
    # Each carrier frequency is considered separately
    for ind_fc in range(carrier.size):
        # Roughness reference values
        R_ref = ref_roughness(carrier[ind_fc], fmod)
        R = np.zeros([fmod.size])
        # Roughness calculation for each modulation frequency
        for ind_fmod in range(fmod.size):     
            signal = test_signal(carrier[ind_fc], fmod[ind_fmod], mdepth, fs, duration, dB)
            R,_ = comp_roughness(signal, fs, overlap)
            R[ind_fmod] = R[2]
        
        
    tst = check_compliance(R, R_ref)
    assert tst
    

def check_compliance(R, R_ref):
    """Check the compliance of roughness calc. to Daniel and Weber article
    "Psychoacoustical roughness: implementation of an optimized model", 1997.

    Check the compliance of the input data R to figure 3 of the article 
    using the reference data described in the dictionary article_ref.

    Parameters
    ----------
    R : float
        Calculated roughness [asper]
    article_ref : dict
        {   "carrier_frequency": <Path to reference input signal>,
            "R_file": <Path to reference calculated roughness>  }
        
        Dictionary containing link to ref. data
        
        
    Outputs
    -------
    tst : bool
        Compliance to the reference data
    """
    
    # Load reference inputs
    R_article = np.genfromtxt(article_ref["R_file"], skip_header=1)
    
    # Test for comformance (1% tolerance)

    tst = (   R.all() >= R_article.all() * 0.83
          and R.all() <= R_article.all() * 1.17   )
           
    
    # Define and plot the tolerance curves 
    fmod_axis = np.linspace(0,160,33)
    tol_curve_min = R_article * 0.83    
    tol_curve_max = R_article * 1.17
    plt.plot(bark_axis, tol_curve_min, color='red', linestyle = 'solid', label='17% tolerance', linewidth=1)  
    plt.plot(bark_axis, tol_curve_max, color='red', linestyle = 'solid', label='', linewidth=1) 
    plt.legend()
    
    # Compliance plot
    
    plt.plot(fmod_axis, R, label="MoSQITo")    
    if tst_specif:
        plt.text(0.5, 0.5, 'Test passed (17% tolerance not exceeded)', horizontalalignment='center',
        verticalalignment='center', transform=plt.gca().transAxes,
        bbox=dict(facecolor='green', alpha=0.3))
    else:
        tst = 0
        plt.text(0.5, 0.5, 'Test not passed', horizontalalignment='center',
        verticalalignment='center', transform=plt.gca().transAxes, 
        bbox=dict(facecolor='red', alpha=0.3))
                
    if tst_N:
        clr = "green"
    else:
        clr = "red"
    plt.title("R = " + str(R) + " asper (Daniel and Weber ref. " + str(R_article) + " asper)", color=clr)
    file_name = "_".join(article_ref["R_file"].split(" "))   
    plt.xlabel("Modulation frequency [Hertz]")
    plt.ylabel("Roughness, [Asper]")
    file_name = "_".join(iso_ref["data_file"].split(" "))
    plt.savefig(
        r"mosqito\tests\roughness\output\test_roughness"
        + file_name.split("/")[-1][:-4]
        + ".png",
        format="png",)
    plt.clf()
    return tst


# test de la fonction
if __name__ == "__main__":
    test_roughness()