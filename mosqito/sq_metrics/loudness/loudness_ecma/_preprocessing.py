# -*- coding: utf-8 -*-

from numpy import pi, cos, arange, max, ceil, concatenate, zeros

def _preprocessing(signal, sb, sh):
    """
    Performs windowing and zero-padding as described in Section 5.1.2 of
    ECMA-418-2 (2nd Ed, 2022) standard for calculating Loudness. 
    
    Parameters
    ----------
    signal : (n_samples,)-shaped numpy.array
        Array containing the sound signal samples, at sampling frequency 48 kHz
    
    sb : int
        Block size, in samples
    
    sh : int
        Hop size, in samples
    """
    
    n_samples = signal.shape[0]
    
    # Apply windowing function to first 5 ms (240 samples)
    n_fadein = 240
    w_fadein = 0.5 - 0.5 * cos(pi * arange(n_fadein) / n_fadein)
    signal[:240] *= w_fadein
    
    # Calculate zero padding at start and end of signal
    sb_max = max(sb)
    sh_max = max(sh)
    
    n_zeros_start = sb_max
    n_new = sh_max * (ceil((n_samples + sh_max + sb_max)/(sh_max)) - 1)
    n_zeros_end = int(n_new) - n_samples
    
    signal = concatenate( (zeros(n_zeros_start),
                              signal,
                              zeros(n_zeros_end)))
    
    return signal, n_new