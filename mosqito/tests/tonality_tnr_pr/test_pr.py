# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 10:41:09 2021

@author: wantysal
"""

import sys
sys.path.append('../../..')

#Standard imports
import numpy as np
import pytest

# Local application imports
from mosqito.functions.shared.load import load
from mosqito.functions.tonality_tnr_pr.comp_pr import comp_pr



@pytest.mark.pr  # to skip or run PR test
def test_pr():
    """Test function for the prominence ratio calculation of an audio signal

    Validation function for the Audio_signal class "comp_tnr" method with signal array 
    as input. The input signals are generated using audacity.

    Parameters
    ----------
    None            

    Outputs
    -------
    None
    """ 
    # Test signal as input for prominence ratio calculation
    # signals generated using audacity : white noise + tones at 200 and 2000 Hz
    # the first one is stationary, the second is time-varying
    signal = np.zeros((2), dtype = dict)
         
    signal[0] = {
        "is_stationary" : True,
        "tones freq" : [200,2000],
        "data_file" : r"mosqito\tests\tonality_tnr_pr\white_noise_200_2000_Hz_stationary.wav",
        }

    signal[1] = {
        "is_stationary" : False,
        "data_file": r"mosqito\tests\tonality_tnr_pr\white_noise_200_2000_Hz_varying.wav",
        } 

    for i in range(len(signal)):
        # Load signal
        audio, fs = load(signal[i]["is_stationary"],signal[i]["data_file"])
        # Compute tone-to-noise ratio     
        pr = comp_pr(signal[i]["is_stationary"], audio, fs, prominence=True, plot=True)        
        # Check compliance
        tst = check_compliance(pr, signal[i])
    
    return tst
    

def check_compliance(pr, signal):
    """Check the compliance of roughness calc. to Daniel and Weber article
    "Psychoacoustical roughness: implementation of an optimized model", 1997.

    Check the compliance of the input data R to figure 3 of the article 
    using the reference data described in the dictionary article_ref.

    Parameter
    ---------
    tnr: dict
        output from 'comp_tnr'
    signal : dict
                
    Output
    ------
    tst : bool
        Compliance to the reference data
    """
    if signal['is_stationary'] == True:
        ref = signal['tones freq']     

        # Test for comformance
        tst = (pr['freqs'] == ref )
    
    else :
        tst = (pr['values'].any() != 0)
    
    return tst
