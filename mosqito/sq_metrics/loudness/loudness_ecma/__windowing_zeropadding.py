# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 14:19:44 2024

@author: HironoASUS
"""

import numpy as np

def _windowing_zeropadding(signal, sb, sh):
    
    n_samples = signal.shape[0]
    
    # -----------------------------------------------------------------------    
    # Apply windowing function to first 5 ms (240 samples)
    
    n_fadein = 240
    
    # Eq. (1)
    w_fadein = 0.5 - 0.5*np.cos(np.pi * np.arange(n_fadein) / n_fadein)
    
    signal[:240] *= w_fadein
    
    # -----------------------------------------------------------------------    
    # Calculate zero padding at start and end of signal
    
    sb_max = np.max(sb)
    sh_max = np.max(sh)
    
    n_zeros_start = sb_max
    
    # Eqs. (2), (3) 
    n_new = sh_max * (np.ceil((n_samples + sh_max + sb_max)/(sh_max)) - 1)
    
    n_zeros_end = int(n_new) - n_samples
    
    signal = np.concatenate( (np.zeros(n_zeros_start),
                              signal,
                              np.zeros(n_zeros_end)))
    
    return signal, n_new