# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:51:19 2020

@author: wantysal
"""

import sys
sys.path.append('../../..')

# Standard library imports
import numpy as np
import math

# Local functions imports
from mosqito.functions.tonality_tnr_pr.tnr_main_calc import tnr_main_calc

def comp_TNR(is_stationary, signal, fs):
    """ Computation of tone-to-noise ration according to ECMA-74, annex D.9 
    
    Parameters
    ----------
    is_stationary : boolean
        True if the signal is stationary    
    signal :numpy.array
        time signal values       
    fs : integer
        sampling frequency
    
    Output
    ------
    output = dict
    {    "name" : "tone-to-noise ratio",
         "time" : np.linspace(0, len(signal)/fs, num=nb_frame),
         "freqs" : <frequency of the tones>
         "values" : <TNR calculated value for each tone>
         "prominence" : <True or False according to ECMA criteria>
         "global value" : <sum of the specific TNR values>       
            }
    
    
    """
        
    if is_stationary == True:
        tones_freqs, tnr, prominence, total_tnr = tnr_main_calc(signal, fs)
        
        output = {
        "name" : "tone-to-noise ratio",
        "freqs" : tones_freqs,
        "values" : tnr,
        "prominence" : prominence,
        "global value" : total_tnr       
        }   
        
    if is_stationary == False:
        # Signal cut in frames of 200 ms along the time axis
        n = 0.5*fs
        nb_frame = math.floor(signal.size / n)
        tones_freqs = np.zeros((nb_frame), dtype = list)
        tnr = np.zeros((nb_frame), dtype = list)
        prominence = np.zeros((nb_frame), dtype = list)
        total_tnr = np.zeros((nb_frame))
        
        
        for i_frame in range(nb_frame):         
            segment = signal[int(i_frame*n):int(i_frame*n+n)]      
            tones_freqs[i_frame], tnr[i_frame], prominence[i_frame], total_tnr[i_frame] = tnr_main_calc(segment, fs)
        
        output = {
            "name" : "tone-to-noise ratio",
            "time" : np.linspace(0, len(signal)/fs, num=nb_frame),
            "freqs" : tones_freqs,
            "values" : tnr,
            "prominence" : prominence,
            "global value" : total_tnr       
        }  
    
    
    return output
