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
from mosqito.roughness_danielweber.roughness_main_calc import roughness_main_calc
from mosqito.roughness_danielweber.weighting_function_gzi import gzi_definition
from mosqito.roughness_danielweber.H_test import H_function
from mosqito.roughness_danielweber.a0_zwicker import a0tab
from mosqito.conversion import freq2bark, db2amp, amp2db, bark2freq
from mosqito.roughness_danielweber.excitation_pattern import excitation_pattern
from mosqito.conversion import amp2db
from mosqito.LTQ import LTQ


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

#  Creation of overlapping 200 ms frames of the sampled input signal 

    # Number of sample points within each frame
    N = int(0.2*fs)
    
    # Signal cutting according to the time resolution of 0.2s
    # with the given overlap proportion (number of rows = number of frames)
    row = math.floor(signal.size/((1-overlap)*N))-1  
    reshaped_signal = np.zeros((row,N))     
    for i_row in range(row):        
        reshaped_signal[i_row,:] = signal[i_row*int(N*(1-overlap)):i_row*int(N*(1-overlap))+N]      

    segment =   reshaped_signal[3,:]  
    n = len(segment)
    
    # Calculate Blackman analysis window with calibration for wav-level and intensity-level
    window = np.blackman(n)
    window = window/sum(window)
    segment = segment * window


    # Calculate a0 transfer characteristic of the outer and inner ear
    duration = n/fs             # 200 ms
    nMax = round(fs/2*duration) # number of frequencies
    nZ = np.arange(0,nMax,1)
    freqs = nZ/duration
    barks = freq2bark(freqs)
    transferOuterInnerEar = a0tab(barks)

    # Make a list of minimum excitation
    # and find the spectral components higher than this
    minExcitDB = LTQ(barks)
    complexSpc = transferOuterInnerEar * fft(segment)[0:nMax]
    amplSpc = abs(complexSpc)
    dBSpc = 20*np.log10(amplSpc)
    iComp = np.where(dBSpc>minExcitDB)[0]
    nComp = len(iComp)


    
    # Calculate the slopes of the excitations by the significant components
    # Terhardt (1979), p. 158, Eqs 2 and 3;
    # Daniel & Weber (1997), p. 117, Eqs 4 and 5.
    
    # Terhardt's slopes definition
    # lower slope [dB/Bark]
    slopeLow			=	-27
    slopeHigh			=	np.zeros((nComp))    
    # upper slope [dB/Bark] 
    for k in np.arange(0,nComp,1):
        slopeHigh[k]	=	min(-24-(230/freqs[iComp[k]])+(0.2*dBSpc[iComp[k]]),0)

     # Calculate excitation pattern for 47 auditory filters separated half a 
     # Bark on a Bark scale 
    nCh = 47
    z = np.arange(0,nCh)/2
    zb = bark2freq(z)*duration
    minExcitDB = np.interp(zb,nZ, minExcitDB)
    chLow = math.floor(2*barks[iComp])
    chHgh = math.ceil(2*barks[iComp])
    slopes = np.zeros((nComp, nCh))
    for k in np.arange(0,nComp):
        levDB = dBSpc[iComp[k]]
        b = barks[iComp[k]]
        for j in np.arange (1,chLow[k]):
            sl = (slopeLow*(b-(j*0.5)))+levDB
            if sl>minExcitDB[j]:
                slopes[k,j] = np.power(10,0.05*sl)
        for j in np.arange(chHgh[k],nCh):
            sl = (slopeHigh[k]*((j*0.5)-b))+levDB
            if sl>minExcitDB[j]:
                slopes[k,j] = np.power(10,0.05*sl)


    # Calculate weighting functions h (Daniel & Weber (1997), p.117) 
    hWeight =  H_function(int(N/2))

    # % Calculate modulation depth of the temporal envelopes of 
    # % the auditory-filter outputs
    temporalEnvelope = np.zeros((nCh, n))
    modDepth = np.zeros((nCh))
    for k in np.arange(0,nCh,1):
        exc = np.zeros((n))
        for j in np.arange(0,nComp,1):
            i = iComp[j]
            if chLow[j] == k:
                ampl = 1
            elif chHgh[j] == k:
                ampl = 1
            elif chHgh[j]>k:
                ampl = slopes[j, k+1]/amplSpc[i]
            else:
                ampl = slopes[j, k-1]/amplSpc[i]
            exc[i] = ampl*complexSpc[i]
        excitation = np.abs(n*np.real(ifft(exc)))
        
        h0 = np.mean(excitation)
        spcEnvelope = fft(excitation-h0)
        temporalEnvelope[k,:] = 2*np.real(ifft(spcEnvelope*hWeight[k,:]))
        rmsTempEnv = np.sqrt(np.mean(np.power(temporalEnvelope[k,:],2)))
        if h0>0:
            modDepth[k]= rmsTempEnv/h0
            if modDepth[k]>1:
                modDepth[k] = 1
        else:
            modDepth[k] = 0

    # Crosscorrelation coefficients ki2 between the envelopes of the channels i-2 and i
    # and ki calculated from channels i and i+2 with dz= 1 bark    
    ki2 = np.zeros((47))
    ki = np.zeros((47))
        
    for i in range(2,47):
        if temporalEnvelope[i-2].all()!=0 and temporalEnvelope[i].all()!=0:
            ki2[i] = np.corrcoef(temporalEnvelope[i-2,:],temporalEnvelope[i,:])[0,1]
    for i in range(0,45):   
        if temporalEnvelope[i].all()!=0 and temporalEnvelope[i+2].all()!=0:
            ki[i] = np.corrcoef(temporalEnvelope[i,:],temporalEnvelope[i+2,:])[0,1]

    # Aures modulation depth weighting function
    center_freq = np.arange(1,48,1)/2
    gzi = gzi_definition(center_freq)

    # Specific roughness calculation with gzi the modulation depth weighting function given by Aures
    R_spec = np.zeros((47))    
    for i in range(47):
        R_spec[i] = pow(gzi[i]*modDepth[i]*ki2[i]*ki[i],2)
        
    # Total roughness calculation with calibration factor of 0.25 given in the article  
    # to produce a roughness of 1 asper for a 1-kHz, 60dB tone with carrier frequency 
    # of 70 Hz and a modulation depth of 1 (Daniel & Weber (1997), p. 118).

    R = 0.25 * sum(R_spec)

    return R, R_spec
        