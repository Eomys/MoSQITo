# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:34:04 2020
@author: wantysal
"""

import sys
sys.path.append('../../..')

# Standard imports
import numpy as np
from numpy.fft import fft, ifft
import math

# Local imports
from functions.roughness_danielweber.excitation_pattern import excitation_pattern
from functions.roughness_danielweber.weighting_function_gzi import gzi_definition
from functions.roughness_danielweber.H_test import H_function
from functions.roughness_danielweber.a0_zwicker import a0tab
from functions.conversion import freq2bark, amp2db
from functions.roughness_danielweber.LTQ import LTQ

def comp_roughness(signal,fs,overlap):
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

    print('Roughness is being calculated')
        
#  Creation of overlapping 200 ms frames of the sampled input signal 

    # Number of sample points within each frame
    N = int(0.2*fs)    
    # Signal cutting according to the time resolution of 0.2s
    # with the given overlap proportion (number of rows = number of frames)
    row = math.floor(signal.size/((1-overlap)*N))-1  
    reshaped_signal = np.zeros((row,N))     
    for i_row in range(row):        
        reshaped_signal[i_row,:] = signal[i_row*int(N*(1-overlap)):i_row*int(N*(1-overlap))+N]      
    # time axis for the windows of 200ms
    time = np.linspace(0,len(signal)/fs,num = row)
    
# Creation of the spectrum by FFT with a Blackman window
    fourier = fft(reshaped_signal*np.blackman(N))
    fourier = fourier*2/(N*np.mean(np.blackman(N)))
    # Zwicker transmission factor   
    a0 = np.power(10,0.05*a0tab(freq2bark(np.concatenate((np.arange(0,4800,1)*fs/N,np.arange(4800,0,-1)*fs/N)))))
    fourier = fourier * a0
    
# Definition of the frequency frame of interest
    # lower limit of the hearing domain is 20Hz
    low_limit	= round(20*N/fs)
    # upper limit of the hearing domain is 2 kHz
    high_limit	= int(20000*N/fs)+1
    
    # Audible frequencies axis
    audible_freq_index = np.arange(low_limit,high_limit,1)
    audible_freq_axis =	(audible_freq_index)*fs/N
    audible_bark_axis = freq2bark(audible_freq_axis)
    
    
    
# Weighting functions initialization
    # modelization of the band pass characteristics of roughness on frequency modulation
    H = H_function(N,fs)
    # Aures modulation depth weighting function
    center_freq = np.arange(1,48,1)/2
    gzi = gzi_definition(center_freq)

# Roughness calculation
    R = np.zeros((row))
    R_spec = np.zeros((row,47))


    for i_time in range (row):
        
        # Selection of the time window spectrum
        spectrum = fourier[i_time,:]        
        # Spectrum module
        module	= np.abs(spectrum[audible_freq_index])
        # Spectrum conversion in dB (ref 2e-5) 
        LdB	= amp2db(module) 
                
        # Selection of the frequency index where the level is superior to the auditory threshold
        # the LTQ values come from E. Zwicker, H. Fastl: Psychoacoustics, 1990
        audible_index = np.where(LdB > LTQ(audible_bark_axis))[0]
        # Number of significant frequencies
        sizL = audible_index.size  
            
#------------------------------1st stage---------------------------------------
#----------------Creation of the specific excitations functions----------------
    
        # Transfomation of the spectrum according to triangular excitation pattern
        etmp = excitation_pattern(N,sizL,spectrum,module,LdB,low_limit, audible_index, audible_freq_axis,audible_bark_axis)
    
        # The temporal specific excitation functions are obtained by IFFT
        ei = np.real(ifft(etmp * N ))


#-------------------------------2d stage---------------------------------------
#---------------------modulation depth calculation-----------------------------                 

        # The fluctuations of the envelope are contained in the low frequency part 
        # of the spectrum of specific excitations in absolute value 
        h0		=	np.mean(np.abs(ei),axis=1) 
        ei_abs = np.zeros((47,N))
        for k in range(47):
            ei_abs[k,:] = np.abs(ei[k,:])-h0[k]
            
        Fei	= fft(ei_abs)
            
        # This spectrum is appropriately weighted in order to model 
        # the low-frequency  bandpass characteristic of the roughness
        # on modulation frequency
        
        Fei_weighted = Fei*H
 
        # The time functions of the bandpass filtered envelopes hBPi(t) 
        # are calculated via inverse Fourier transform :          
        hBPi	= 2* np.real(ifft(Fei_weighted))
        hBPrms	=	np.sqrt(np.mean(np.power(hBPi,2),axis=1))
                
        # Modulation depth estimation is given by envelope RMS values 
        # and excitation functions time average : 
        mdept = np.zeros((47))
        for k in range(47):    
            if h0[k]>0 :
                mdept[k]=hBPrms[k]/h0[k]
                if mdept[k]>1:
                    mdept[k]=1        
                
#-------------------------------3rd stage--------------------------------------
#----------------roughness calculation with cross correlation------------------
    
        # Crosscorrelation coefficients ki2 between the envelopes of the channels i-2 and i
        # and ki calculated from channels i and i+2 with dz= 1 bark    
        ki2 = np.zeros((47))
        ki = np.zeros((47))
            
        for i in range(2,47):
            if hBPi[i-2].all()!=0 and hBPi[i].all()!=0:
                ki2[i] = np.corrcoef(hBPi[i-2,:],hBPi[i,:])[0,1]
        for i in range(0,45):   
            if hBPi[i].all()!=0 and hBPi[i+2].all()!=0:
                ki[i] = np.corrcoef(hBPi[i,:],hBPi[i+2,:])[0,1]
    
        # Specific roughness calculation with gzi the modulation depth weighting function given by Aures
        for i in range(47):
            R_spec[i_time,i] = pow(gzi[i]*mdept[i]*ki2[i]*ki[i],2)
            
        # Total roughness calculation with calibration factor of 0.25 given in the article  
        # to produce a roughness of 1 asper for a 1-kHz, 60dB tone with carrier frequency 
        # of 70 Hz and a modulation depth of 1 (Daniel & Weber (1997), p. 118).    
        R[i_time] = 0.25 * sum(R_spec[i_time,:])

        
    return R, R_spec, time, center_freq
