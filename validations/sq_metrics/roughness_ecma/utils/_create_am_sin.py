# -*- coding: utf-8 -*-
"""
Test signal for roughness calculation

Author:
    Fabio Casagrande Hirono
    Jan 2024
"""

import numpy as np


def _create_am_sin(spl_level, fc, xm, fs, print_m=False):
    """
    Creates an amplitude-modulated (AM) signal with sinusoidal carrier of level
    'spl_level' (in dB SPL) and frequency 'fc', arbitrary modulating signal
    'xm', and sampling frequency 'fs'. The AM signal length is the same as the
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
        
    fs: float
        Sampling frequency, in samples/second (Hz).
    
    print_m: bool, optional
        Flag declaring whether to print the calculated modulation index.
        Default is False.
    
    Returns
    -------
    y: numpy.array
        Amplitude-modulated signal with sine carrier, in Pascals
        
    Notes
    -----
    The modulation index 'm' will be equal to the peak value of the modulating
    signal 'xm'. Its value can be printed by setting the optional flag
    'print_m' to True.
    """
    
    Nt = xm.shape[0]        # signal length in samples
    T = Nt/fs               # signal length in seconds
    dt = 1/fs               # sampling interval in seconds

    # vector of time samples
    t = np.linspace(0, T-dt, int(T*fs))
    
    # Sine wave carrier, with level 'spl_level' and frequency 'fc' [Hz]
    p_ref = 20e-6
    A = np.sqrt(2) * p_ref * 10**(spl_level/20)
    xc = A*np.sin(2*np.pi*fc*t)

    # # signal power check - must be close to 'spl_level
    # sig_power_dB = 10*np.log10(np.var(xc)/(p_ref**2))

    # AM signal
    y_am = (1 + xm)*xc

    # modulation index
    m = np.max(np.abs(xm))

    if print_m:
        print(f"AM Modulation index = {m}")
    
    if m > 1:
        print("Warning ['create_am_cosine']: modulation index m > 1\n\tSignal is overmodulated!")

    return y_am