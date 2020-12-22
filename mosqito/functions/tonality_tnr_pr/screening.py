# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 20:23:01 2020

@author: Salomé
"""
# Standard library imports
import numpy as np
import matplotlib.pyplot as plt

# Mosqito functions import
from mosqito.functions.shared.spectrum_smoothing import spectrum_smoothing
from mosqito.functions.tonality_tnr_pr.LTH import LTH

        
def screening_for_tones(freqs, spec_db, method, low_freq, high_freq):
    """
        Screening function to find the tonal candidates in a spectrum
         
        The 'smoothed' method is the one described by Bray W and Caspary G in :
        Automating prominent tone evaluations and accounting for time-varying 
        conditions, Sound Quality Symposium, SQS 2008, Detroit, 2008.
        
        The 'not-smoothed' method is the one used by Aures and Terhardt

    Parameters
    ----------
    freqs : numpy.array
        frequency axis
    spec_db : numpy.array
        spectrum in dB
    method : string
        the method chosen to find the tones 'Sottek'
    low_freq : float
        lowest frequency of interest
    high_freq : float
        highest frequency of interest


    Returns
    -------
    index : list
        list of index corresponding to the potential tonal components

    """

    if method == 'smoothed':
    
        # Criteria 1 : the level of the spectral line is higher than the level of 
        # the two neighboring lines
        maxima = (np.diff(np.sign(np.diff(spec_db))) < 0).nonzero()[0] + 1 
        # plt.plot(freqs[maxima], spec_db[maxima], "x")
    
        # Criteria 2 : the level of the spectral line exceeds the corresponding lines 
        # of the 1/24 octave smoothed spectrum by at least 6 dB
        smooth_spec = spectrum_smoothing(freqs, spec_db, 24, low_freq, high_freq, freqs)
        plt.plot(freqs, smooth_spec)
        indexx = np.where(spec_db[maxima] > smooth_spec[maxima] + 6)[0]
        # plt.plot(freqs[maxima][indexx], spec_db[maxima][indexx], "o")
        
     
        # Criteria 3 : the level of the spectral line exceeds the threshold of hearing
        threshold = LTH(freqs)
        # plt.plot(freqs, threshold + 10)
        audible = np.where(spec_db[maxima][indexx] > threshold[maxima][indexx] + 10)[0]
        # plt.plot(freqs[maxima][indexx][audible], spec_db[maxima][indexx][audible], "s")
        
        index = np.arange(0,len(spec_db))[maxima][indexx][audible]

    if method == 'not-smoothed':
        # Criteria 1 : the level of the spectral line is higher than the level of 
        # the two neighboring lines
        maxima = (np.diff(np.sign(np.diff(spec_db[2:len(spec_db)-2]))) < 0).nonzero()[0] + 1 # local max 
        plt.plot(freqs[2:len(spec_db)-2][maxima], spec_db[2:len(spec_db)-2][maxima], "x")
    
        # Criteria 2 : the level of the spectral line is at least 7 dB higher than its
        # +/- 2,3 neighbors
        indexx = np.where((spec_db[maxima] > (spec_db[maxima + 2] + 7))\
                          & (spec_db[maxima] > (spec_db[maxima - 2] + 7))\
                              & (spec_db[maxima] > (spec_db[maxima + 3] + 7))\
                                  & (spec_db[maxima] > (spec_db[maxima -3] + 7)))[0]
        plt.plot(freqs[maxima][indexx], spec_db[maxima][indexx], "o")
              
        # Criteria 3 : the level of the spectral line exceeds the threshold of hearing
        threshold = LTH(freqs)
        plt.plot(freqs, threshold + 10)
        audible = np.where(spec_db[maxima][indexx] > threshold[maxima][indexx] + 10)[0]
        # plt.plot(freqs[maxima][indexx][audible], spec_db[maxima][indexx][audible], "s")
        
        index = np.arange(0,len(spec_db))[maxima][indexx][audible]

                   
    return index
        
