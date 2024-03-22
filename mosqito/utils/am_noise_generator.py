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
        Sound Pressure Level [dB ref 20 uPa RMS] of the modulated signal.
    
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

    return y_am


# %% run example for AM noise generator

if __name__ == "__main__":
    
    import matplotlib.pyplot as plt
    
    # preliminary definitions
    fs = 48000      # [Hz]
    dt = 1/fs
    
    T = 0.1         # [s]
    t = np.linspace(0, T-dt, int(T*fs))
    
    spl = 60        # [dB SPL]
    p_ref = 20e-6   # [Pa RMS]
    
    # sine carrier frequency
    fc = 1000        # [Hz]
    
    # modulating signal: low frequency sine wave
    fm = 100         # [Hz]
    xm = np.sin(2*np.pi*t*fm)
    
    # frequency-modulated signal
    y_am = am_noise_generator(spl, xm, fs)
    
    # signal power check - must be close to 'spl_level'
    sig_power_dB = 10*np.log10(np.var(y_am)/(p_ref**2))
    print('AM noise generator example:')
    print(f'\tTarget SPL: {spl:.1f} dB')
    print(f'\tResulting SPL: {sig_power_dB:.1f} dB')
    
    # plot signal
    fig, plots = plt.subplots(2, 1)
    
    plots[0].set_title('Test signal - amplitude-modulated broadband noise')
    
    plots[0].plot(t, xm, 'C0', label='Modulating signal')
    plots[0].legend(loc='upper right')
    plots[0].grid()
    plots[0].set_ylabel('Amplitude')
    plots[0].set_xlim([0, T])
    
    plots[1].plot(t, y_am, 'C1', label='AM signal')
    plots[1].legend(loc='upper right')
    plots[1].grid()
    plots[1].set_ylabel('Amplitude')
    plots[1].set_xlim([0, T])
    plots[1].set_xlabel('Time [s]')
    
    fig.set_tight_layout('tight')
    