# -*- coding: utf-8 -*-
"""
Generate amplitude-modulated (AM) broadband noise

Author:
    Fabio Casagrande Hirono
    Mar 2024
"""

import numpy as np

def am_noise_generator(spl_level, xm, fs, print_m=False):
    """
    Creates an amplitude-modulated (AM) signal of level 'spl_level' (in dB SPL),
    with Gaussian broadband (noise) carrier, arbitrary modulating signal 'xm',
    and sampling frequency 'fs'. The AM signal length is the same as the length 
    of 'xm'. 
    
    Parameters
    ----------
    spl_level: float
        Sound Pressure Level [ref 20 uPa RMS] of the modulated signal.
    
    xm: (N,)-shaped numpy.array
        Numpy array containing the modulating signal.
    
    fs: float
        Sampling frequency, in Hz.
    
    print_m: bool, optional
        Flag declaring whether to print the calculated modulation index.
        Default is False.
    

    Returns
    -------
    y: (N,)-shaped numpy.array
        Amplitude-modulated noise signal, in Pascals.
    
        
    Notes
    -----
    The modulation index 'm' will be equal to the peak value of the modulating
    signal 'xm'. Its value can be printed by setting the optional flag
    'print_m' to True.
    
    For 'm' = 0.5, the carrier amplitude varies by 50% above and below its
    unmodulated level. For 'm' = 1.0, it varies by 100%. With 100% modulation 
    the wave amplitude sometimes reaches zero, and this represents full
    modulation. Increasing the modulating signal beyond that point is known as
    overmodulation.    
    """
    
    # signal length in samples
    Nt = xm.shape[0]
    
    # create vector of zero-mean, unitary std dev random samples
    rng = np.random.default_rng()
    xc = rng.standard_normal(Nt)    

    # AM signal
    y_am = (1 + xm)*xc

    # AM modulation index
    m = np.max(np.abs(xm))

    if print_m:
        print(f"AM Modulation index = {m}")
    
    if m > 1:
        print("Warning ['create_am_noise']: modulation index m > 1\n\tSignal is overmodulated!")

    # normalise broadband signal energy to 'spl_level' [dB SPL ref 20 uPa]
    p_ref = 20e-6
    A_rms = p_ref * 10**(spl_level/20)
    y_am *= A_rms/np.std(y_am)
    
    # # signal power check - must be close to 'spl_level
    # sig_power_dB = 10*np.log10(np.var(y_am)/(p_ref**2))

    return y_am