# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:34:04 2020

@author: wantysal
"""

import sys
sys.path.append('../..')

# Standard imports
import numpy as np
from numpy.fft import fft
import math

# Local imports
from mosqito.roughness_danielweber.roughness_main_calc import roughness_main_calc
from mosqito.roughness_danielweber.weighting_function_gzi import gzi_definition
from mosqito.roughness_danielweber.H_function import H_function
from mosqito.roughness_danielweber.a0_zwicker import a0tab
from mosqito.conversion import freq2bark

def roughness(signal,fs,overlap):
    """ Roughness calculation of a signal sampled at 48kHz.

    The code is based on the algorithm described in "Psychoacoustical roughness:
    implementation of an optimized model" by Daniel and Weber in 1997.
    The roughness model consists of a parallel processing structure that is made up 
    of successive stages and calculates intermediate specific roughnesses R_spec, 
    which are summed up to determine the total roughness R.
    
    Parameters
    ----------
    signal : numpy.array
        signal amplitude values along time
    fs : integer
        sampling frequency
    overlap : float
        overlapping coefficient for the time windows of 200ms 

    Outputs
    -------
    R : numpy.array
        roughness
    R_spec : numpy.array
           specific roughness value within each critical band    
    
    """            

#  Creation of overlapping 200 ms frames of the sampled input signal 

    # Number of sample points within each frame
    N = int(0.2*fs)
    
    # Signal cutting according to the time resolution of 0.2s
    # with the given overlap proportion (number of rows = number of frames)
    row = math.floor(signal.size/((1-overlap)*N))-1  
    reshaped_signal = np.zeros((row,N))     
    for i_row in range(row):        
        reshaped_signal[i_row,:] = signal[i_row*int(N*(1-overlap)):i_row*int(N*(1-overlap))+N]      
    
# Creation of the spectrum by FFT with a Blackman window
    fourier = fft(reshaped_signal* np.blackman(N)*2/(np.sum(np.blackman(N))))

    # Zwicker transmission factor
    
    a0 = np.power(10,0.05*a0tab(freq2bark(np.concatenate((np.arange(0,4800,1)*fs/N,np.arange(4800,0,-1)*fs/N)))))
    fourier = fourier * a0
    
# Definition of the frequency frame of interest
    # lower limit of the hearing domain is 20Hz
    low_limit	= round(20*N/fs)
    # upper limit of the hearing domain is 2 kHz
    high_limit	= int(20000*N/fs)+1
    
    # Audible frequencies axis
    audible_freq_index =	np.arange(low_limit,high_limit,1)
    audible_freq_axis	=	(audible_freq_index)*fs/N
    audible_bark_axis = freq2bark(audible_freq_axis)
    
    
    
# Weighting functions initialization
    # modelization of the band pass characteristics of roughness on frequency modulation
    H = H_function(int(N/2))
    # Aures modulation depth weighting function
    center_freq = np.arange(1,48,1)/2
    gzi = gzi_definition(center_freq)

# Roughness calculation
    R = np.zeros((row))
    R_spec = np.zeros((row,47))
    print('Roughness is being calculated')
    for i_time in range (row):
        R[i_time], R_spec[i_time,:] =	roughness_main_calc(fourier[i_time,:],H,gzi, N, fs,low_limit,audible_freq_index,audible_freq_axis,audible_bark_axis)
        
    return R, R_spec