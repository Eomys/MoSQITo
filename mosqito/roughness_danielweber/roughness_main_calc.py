# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 16:29:35 2020

@author: wantysal
"""
import sys
sys.path.append('../../..')


# Standard library imports
import numpy as np
from numpy.fft import fft, ifft

# Local imports
from mosqito.roughness_danielweber.excitation_pattern import excitation_pattern
from mosqito.conversion import amp2db
from mosqito.LTQ import LTQ

def roughness_main_calc(fourier,H,gzi,N,fs,low_limit,audible_freq_index,audible_freq_axis,audible_bark_axis):  
        
    # Spectrum module
    module	= np.abs(fourier[audible_freq_index])
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
    etmp = excitation_pattern(N,sizL,fourier,module,LdB,low_limit, audible_index, audible_freq_axis,audible_bark_axis)

    # The temporal specific excitation functions are obtained by IFFT
    ei = np.real(ifft(etmp * N * np.mean(np.blackman(N)) ,axis=1))


#-------------------------------2d stage---------------------------------------
#---------------------modulation depth calculation-----------------------------                 

    # The fluctuations of the envelope are contained in the low frequency part 
    # of the spectrum of specific excitations in absolute value 
    h0		=	np.mean(np.abs(ei),axis=1) 
    Fei = np.zeros((47,N),dtype=complex)
    for k in range (47):
        Fei[k,:]	=	fft(np.abs(ei[k,:])-h0[k]) 
        
    # This spectrum is appropriately weighted in order to model 
    # the low-frequency  bandpass characteristic of the roughness
    # on modulation frequency
    Fei	=   Fei * H

    # The time functions of the bandpass filtered envelopes hBPi(t) 
    # are calculated via inverse Fourier transform :          
    hBPi	= 2 * np.real(ifft(Fei))
    hBPrms	=	np.sqrt(np.mean(np.power(hBPi,2),axis=1))
            
    # Modulation depth estimation is given by envelope RMS values 
    # and excitation functions time average : 
    mdept = np.zeros((47))
    for k in range(47):    
        if h0[k]>0 :
            mdept[k]=hBPrms[k]/h0[k]
            if mdept[k]>1:
                mdept[k]=1        
            
            

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
    R_spec = np.zeros((47))    
    for i in range(47):
        R_spec[i] = pow(gzi[i]*mdept[i]*ki2[i]*ki[i],2)
        
    # Total roughness calculation with calibration factor of 0.25 given in the article  
    # to produce a roughness of 1 asper for a 1-kHz, 60dB tone with carrier frequency 
    # of 70 Hz and a modulation depth of 1 (Daniel & Weber (1997), p. 118).

    R = 0.25 * sum(R_spec)

    return R, R_spec
        