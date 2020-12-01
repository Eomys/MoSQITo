# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:39:05 2020
@author: wantysal
"""
# Standard library import
import numpy as np

# Local import
from mosqito.functions.roughness_danielweber.LTQ import LTQ
from mosqito.functions.conversion import db2amp
from mosqito.functions.roughness_danielweber.a0_zwicker import a0tab

def excitation_pattern(N,sizL,spectrum,module,LdB,low_limit, audible_index, audible_freq_axis,audible_bark_axis):
       
    # Terhardt's slopes definition
    # lower slope [dB/Bark]
    S1			=	-27
    S2			=	np.zeros((sizL))
    for l in np.arange(0,sizL,1):
        # upper slope [dB/Bark] 
        steep	=	-24-(230/audible_freq_axis[audible_index[l]])+(0.2*LdB[audible_index[l]])
        if steep<0:
            S2[l]=steep
        
    # Initialization    
    whichZ	    =	np.zeros((2,sizL),dtype = int)
    qd			=	np.arange(0,sizL,1)
    
    # Lower limit of the bark frequency bin corresponding to each audibe frequency component 
    whichZ[0,:]	=	np.floor(2*audible_bark_axis[audible_index[qd]])
    # Upper limit of the bark frequency bin corresponding to each audibe frequency component 
    whichZ[1,:]	=	np.ceil(2*audible_bark_axis[audible_index[qd]])
    
    
    # The excitation contributions in each interval [zi - 0.5, zi + 0.5] 
    # are linearly superimposed.
    # The contribution of a spectral component in each interval is:    
    # considering z(f) the frequency of the component given in Bark 
    # If  z(f) > zi + 0.5 Bark : 
    #     contribution to the specific excitation =  S1(Zi + 0.5 Bark)
    # If z(f) < zi - 0.5 Bark : 
    #     contribution to the specific excitation =  S2(Zi - 0.5 Bark)
    # If  z(f) falls into the interval [zi - 0.5; zi + 0.5] : 
    #     contribution to the specific excitation =  L 
    # The contributions whose level is lower than LTQ are omitted
    
    # The linear contributions different from 1 are divided by the absolute value
    # of the original fft and then multiplied by the fft to reconstruct a complete result
    # with the original phases and an absolute value weighted according to the triangular scheme

    Slopes      = np.zeros((sizL,47))
    
    for l in np.arange(0,sizL,1):
        level =	LdB[audible_index[l]]
        bark = audible_bark_axis[audible_index[l]]
        
        for k in np.arange(0,whichZ[0,l],1):
            Stemp	=	(S1*(bark-(k*0.5)))+level
            if Stemp > LTQ(k*0.5) - a0tab(k*0.5):
                Slopes[l,k]= db2amp(Stemp)
        
        for k in np.arange(int(whichZ[1,l]),47,1):
            Stemp	=	(S2[l]*((k*0.5)-bark))+level
            if Stemp  > LTQ(k*0.5) - a0tab(k*0.5):
                Slopes[l,k]= db2amp(Stemp)
    
                    
    ExcAmp     =	np.zeros((47,sizL))  
    etmp = np.zeros((47,len(spectrum)),dtype=complex)
    
    for k in range (1,46,1):        
        for l in np.arange(0,sizL,1):
            # index of the component on the audible axis
            N1tmp = audible_index[l]
            # index of the component on the full axis
            N2tmp = N1tmp + low_limit
            # the component belongs to the bark window
            if whichZ[0,l] == k  :
                ExcAmp[k,l]	=	1
            # the component is higher than the bark window
            elif whichZ[1,l]>k:
                ExcAmp[k,l]	=	Slopes[l,k+1]/module[N1tmp]
            # the component is lower than the window
            elif whichZ[0,l]<k:
                ExcAmp[k,l]   =	Slopes[l,k-1]/module[N1tmp]
            
            # reconstruction of the spectrum 
            etmp[k,N2tmp]	=	ExcAmp[k,l] * spectrum[N2tmp]
            # # # symmetrization in anticipation of subsequent IFFT
            # etmp[k,N-N2tmp] = etmp[k,N2tmp]
            
    return etmp
