# -*- coding: utf-8 -*-
"""
Test signal for roughness calculation

Author:
    Fabio Casagrande Hirono
    Jan 2024
"""

import numpy as np


def _create_fm_sin(spl_level, fc, xm, k, fs, return_aux_params=False,
                   print_info=False):
    """
    Creates a frequency-modulated (FM) signal with sinusoidal carrier of level
    'spl_level' (in dB SPL) and frequency 'fc', arbitrary modulating signal
    'xm', and sampling frequency 'fs'. The FM signal length is the same as the
    length of 'xm'. 
    
    Parameters
    ----------
    spl_level: float
        Sound Pressure Level [ref 20 uPa RMS] of the (unmodulated) carrier sine
        wave.
        
    fc: float
        Carrier frequency, in Hz. Must be less than 'fs/2'.
        
    xm: numpy.array
        Numpy array containing the modulating signal.
    
    k: float
        Frequency sensitivity of the modulator. This is equal to the frequency
        deviation in Hz away from 'fc' per unit amplitude of the modulating
        signal 'xm'.

    fs: float
        Sampling frequency, in Hz.
    
    return_aux_params: bool, optional
        Flag declaring whether to return a dict containing auxiliary parameters.
        See notes for details. Default is False.
    
    print_info: bool, optional
        Flag declaring whether to print values for maximum frequency deviation and FM modulation index. Default is False.
    
    
    Returns
    -------
    y_fm: numpy.array
        Frequency-modulated signal with sine carrier
    
    aux_params: dict
        Dictionary of auxiliary parameters, containing:
            'inst_freq': numpy array of instantaneous frequency of output signal;
            'max_freq_deviation': float, maximum frequency deviation from 'fc';
            'FM_modulation_index': float, FM modulation index
    """
    
     # sampling interval in seconds
    dt = 1/fs

    # instantaneous frequency of FM signal
    inst_freq = fc + k*xm
    
    # FM signal
    p_ref = 20e-6
    A = np.sqrt(2) * p_ref * 10**(spl_level/20)
    y_fm = A*np.sin(2*np.pi * np.cumsum(inst_freq)*dt)
    
    # max frequency deviation
    f_delta = k*np.max(np.abs(xm))
    
    # FM modulation index
    m_FM = np.max(np.abs(2*np.pi*k*np.cumsum(xm)*dt))
    
    if print_info:
        print(f'\tMax freq deviation: {f_delta} Hz')
        print(f'\tFM modulation index: {m_FM:.2f} Hz')

    aux_params = {
        'inst_freq': inst_freq,
        'max_freq_deviation': f_delta,
        'FM_modulation_index': m_FM}

    if return_aux_params:
        
        return y_fm, aux_params
    
    else:
        return y_fm
