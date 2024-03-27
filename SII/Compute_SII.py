# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from mosqito.utils.LTQ import LTQ
from mosqito.utils.conversion import freq2bark


def compute_sii(method, speech, noise=None, threshold=None):
    """
    

    Parameters
    ----------
    method : string
        Frenquency bands type used for the computation ('critical', 'equally_critical', 'third_octave', 'octave').
    speech : ndarray or string
        Speech spectrum. Can be either an imported array in dB or a string to use the data provided in the standard ('normal', 'raised', 'loud', 'shout'). 
        ! axis should be the same as the one specified in method.
    noise : ndarray
        Background noise spectrum in dB. ! axis should be the same as the one specified in method.
        In case of a single value, it will be set on each frequency band.
        If None, it is set to -50 dB.
    threshold : ndarray or string or None
        Hearing threshold used to take into account the human ear sensitivity. Can be either an imported array in dB or 'zwicker' to use the Zwicker hearing thresholed. 
        If None, no threshold is applied.

    Returns
    -------
    specific_sii : TYPE
        DESCRIPTION.
    sii : TYPE
        DESCRIPTION.

    """
    
    if (method!='critical') & (method!='equally_critical') & (method!='third_octave') & (method!='octave'):
        raise ValueError('Method should be "critical", "equally_critical", "third_octave" or "octave".')
        
    if (speech.astype!=np.array) & (speech!='normal') & (speech!='raised') & (speech!='loud') & (speech!='shout'):
        raise ValueError('Speech should be either an array or "normal", "raised", "loud" or "shout" to use standard data.')
        
    
    if method == 'critical':
        from Critical_band_procedure import (
            CENTER_FREQUENCIES,
            LOWER_FREQUENCIES,
            UPPER_FREQUENCIES,
            IMPORTANCE, 
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
            FREEFIELD2EARDRUM_TRANSFER_FUNCTION )
        if speech == 'normal':
            from Critical_band_procedure import (       
                STANDARD_SPEECH_SPECTRUM_NORMAL,
                OVERALL_SPEECH_LEVEL_NORMAL )
            E = STANDARD_SPEECH_SPECTRUM_NORMAL
        elif speech == 'raised':
            from Critical_band_procedure import (       
                STANDARD_SPEECH_SPECTRUM_RAISED,
                OVERALL_SPEECH_LEVEL_RAISED )
            E = STANDARD_SPEECH_SPECTRUM_RAISED
        elif speech == 'loud':
            from Critical_band_procedure import (       
                STANDARD_SPEECH_SPECTRUM_LOUD,
                OVERALL_SPEECH_LEVEL_LOUD )
            E = STANDARD_SPEECH_SPECTRUM_LOUD
        elif speech == 'shout':
            from Critical_band_procedure import (       
                STANDARD_SPEECH_SPECTRUM_SHOUT,
                OVERALL_SPEECH_LEVEL_SHOUT )
            E = STANDARD_SPEECH_SPECTRUM_SHOUT
        else:
            E = np.array(speech)
    elif method == 'equally_critical':
        from Eq_critical_band_procedure import (
            CENTER_FREQUENCIES,
            LOWER_FREQUENCIES,
            UPPER_FREQUENCIES,
            IMPORTANCE, 
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
            FREEFIELD2EARDRUM_TRANSFER_FUNCTION )        
        if speech == 'normal':
            from Eq_critical_band_procedure import (
                OVERALL_SPEECH_LEVEL_NORMAL )
            E = STANDARD_SPEECH_SPECTRUM_NORMAL
        elif speech == 'raised':
            from Eq_critical_band_procedure import (
                STANDARD_SPEECH_SPECTRUM_RAISED,
                OVERALL_SPEECH_LEVEL_RAISED )
            E = STANDARD_SPEECH_SPECTRUM_RAISED
        elif speech == 'loud':
            from Eq_critical_band_procedure import (
                STANDARD_SPEECH_SPECTRUM_LOUD,
                OVERALL_SPEECH_LEVEL_LOUD )
            E = STANDARD_SPEECH_SPECTRUM_LOUD
        elif speech == 'shout':
            from Eq_critical_band_procedure import (
                STANDARD_SPEECH_SPECTRUM_SHOUT,
                OVERALL_SPEECH_LEVEL_SHOUT )
            E = STANDARD_SPEECH_SPECTRUM_SHOUT
        else:
            E = np.array(speech)
    if method == 'third_octave':
        from Third_octave_band_procedure import (
            CENTER_FREQUENCIES,
            BANDWIDTH,
            IMPORTANCE, 
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
            FREEFIELD2EARDRUM_TRANSFER_FUNCTION )
        
        if speech == 'normal':
            from Third_octave_band_procedure import (   
                OVERALL_SPEECH_LEVEL_NORMAL )
            E = STANDARD_SPEECH_SPECTRUM_NORMAL
        elif speech == 'raised':
            from Third_octave_band_procedure import (   
                STANDARD_SPEECH_SPECTRUM_RAISED,
                OVERALL_SPEECH_LEVEL_RAISED )
            E = STANDARD_SPEECH_SPECTRUM_RAISED
        elif speech == 'loud':
            from Critical_band_procedure import (       
                STANDARD_SPEECH_SPECTRUM_LOUD,
                OVERALL_SPEECH_LEVEL_LOUD )
            E = STANDARD_SPEECH_SPECTRUM_LOUD
        elif speech == 'shout':
            from Third_octave_band_procedure import (   
                STANDARD_SPEECH_SPECTRUM_SHOUT,
                OVERALL_SPEECH_LEVEL_SHOUT )
            E = STANDARD_SPEECH_SPECTRUM_SHOUT
        else:
            E = np.array(speech)
    if method == 'critical':
        from Octave_band_procedure import (   
            CENTER_FREQUENCIES,
            BANDWIDTH,
            IMPORTANCE, 
            REFERENCE_INTERNAL_NOISE_SPECTRUM,
            STANDARD_SPEECH_SPECTRUM_NORMAL,
            FREEFIELD2EARDRUM_TRANSFER_FUNCTION )
        
        if speech == 'normal':
            from Octave_band_procedure import (   
                OVERALL_SPEECH_LEVEL_NORMAL )
            E = STANDARD_SPEECH_SPECTRUM_NORMAL
        elif speech == 'raised':
            from Octave_band_procedure import (   
                STANDARD_SPEECH_SPECTRUM_RAISED,
                OVERALL_SPEECH_LEVEL_RAISED )
            E = STANDARD_SPEECH_SPECTRUM_RAISED
        elif speech == 'loud':
            from Octave_band_procedure import (   
                STANDARD_SPEECH_SPECTRUM_LOUD,
                OVERALL_SPEECH_LEVEL_LOUD )
            E = STANDARD_SPEECH_SPECTRUM_LOUD
        elif speech == 'shout':
            from Octave_band_procedure import (   
                STANDARD_SPEECH_SPECTRUM_SHOUT,
                OVERALL_SPEECH_LEVEL_SHOUT )
            E = STANDARD_SPEECH_SPECTRUM_SHOUT
        else:
            E = np.array(speech)
            
    nbands = len(CENTER_FREQUENCIES)
    
    if noise is None:
        N = np.zeros((len(E)))
        N.fill(-50)
    else:
        N = np.array(noise)
        if N.size == 1:         
            N = np.zeros((len(E)))
            N.fill(noise)
        
    if threshold is None:
        T = np.zeros((len(E)))
    elif threshold == 'zwicker':
        T = LTQ(freq2bark(CENTER_FREQUENCIES))
    else:
        T = np.array(threshold)
    
    if method == 'octave':
        Z = N
        
    else:
        V = E - 24
        B = np.maximum(N, V)
        
        if method == 'third_octave':
            C = -80 + 0.6 * (B + 10*np.log10(CENTER_FREQUENCIES)-6.353)
            Z = np.zeros((nbands))
            for i in range(nbands): 
                s = 0
                for k in range(i-1):
                    s += 10**(0.1*B[k] + 3.32 * C[k] * np.log10(0.89 * CENTER_FREQUENCIES[i] / CENTER_FREQUENCIES[k]))
                    
                Z[i] = 10 * np.log10(10**(0.1*N[i]) + s)
        else:
            C = -80 + 0.6 * (B + 10*np.log10(UPPER_FREQUENCIES - LOWER_FREQUENCIES))
            Z = np.zeros((nbands))
            for i in range(nbands): 
                s = 0
                for k in range(i-1):
                    s += 10**(0.1*B[k] + 3.32 * C[k] * np.log10(CENTER_FREQUENCIES[i] / UPPER_FREQUENCIES[k]))
                    
                Z[i] = 10 * np.log10(10**(0.1*N[i]) + s)
        
        # 4.3.2.4
        Z[0] = B[0]
    
        
        
        
    # STEP 4
    X = REFERENCE_INTERNAL_NOISE_SPECTRUM + T
    
    # STEP 5
    D = np.maximum(Z, X)
    
    # STEP 6
    L = 1 - (E - STANDARD_SPEECH_SPECTRUM_NORMAL )
    L[np.where(L>1)] = 1
    
    # STEP 7
    K = (E - D + 15)/30
    K[np.where(K>1)] = 1
    K[np.where(K<0)] = 0
    
    A = L * K
    
    # STEP 8
    sii = np.sum(IMPORTANCE * A)
    specific_sii = A
    
    
    return specific_sii, sii


