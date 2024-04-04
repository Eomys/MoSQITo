import numpy as np

def am_sine_generator(xmod, fs, fc, spl_level, print_m=False):
    """ Amplitude-modulated sine wave generation
    
    This function creates an amplitude-modulated (AM) signal with sinusoidal 
    carrier of frequency 'fc', and arbitrary modulating signal 'xmod'.
    The AM signal length is the same as the length of 'xmod'. 
    The signal level is adjusted to 'spl_level' in dB.

    Parameters
    ----------
    xmod: array
        Modulating signal, dim(N).
    fs: float
        Sampling frequency, in Hz.
    fc: float
        Carrier frequency, in Hz. Must be less than 'fs/2'.
    spl_level: float
        Sound Pressure Level [dB ref 20 uPa RMS] of the modulated signal.
    print_m: bool, optional
        Flag declaring whether to print the calculated modulation index.
        Default is False.
    
    Returns
    -------
    y: numpy.array
        Amplitude-modulated signal with sine carrier in Pascals, dim(N).
    m: float
        Modulation index    
        
    Warning
    -------
    spl_level must be provided in dB, ref=2e-5 Pa.
        
    See Also
    --------
    .am_noise_generator : Amplitude modulation with broadband noise carrier
    .fm_sine_generator : Frequency modulation with sine wave carrier
    .sine_wave_generator : Sine wave generation
        
    Notes
    -----
    The modulation index 'm' will be equal to the peak value of the modulating
    signal 'xmod'. Its value can be printed by setting the optional flag
    'print_m' to True.
    
    For 'm' = 0.5, the carrier amplitude varies by 50% above and below its
    unmodulated level. For 'm' = 1.0, it varies by 100%. With 100% modulation 
    the wave amplitude sometimes reaches zero, and this represents full
    modulation. Increasing the modulating signal beyond that point is known as
    overmodulation.
    
    Examples
    --------
    .. plot::
       :include-source:
       
        >>> from mosqito.utils import am_sine_generator
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fs = 48000      # [Hz]
        >>> duration = 1
        >>> t = np.linspace(0, duration, int(fs*duration))
        >>> dB = 60         # [dB SPL]
        >>> fc = 100        # [Hz]
        >>> fm = 4          # [Hz]
        >>> xmod = np.sin(2*np.pi*t*fm)
        >>> y_am, m = am_sine_generator(xmod, fs, fc, dB, True)    
        >>> fig, plots = plt.subplots(2, 1)
        >>> plots[0].set_title(f'Amplitude-modulated sine wave, modulation index = {m:.1f}')
        >>> plots[0].plot(t, xmod, 'C0', label='Modulating signal')
        >>> plots[0].legend(loc='upper right')
        >>> plots[0].grid()
        >>> plots[0].set_ylabel('Amplitude')
        >>> plots[0].set_xlim([0, duration])
        >>> plots[1].plot(t, y_am, '#69c3c5', label='AM signal')
        >>> plots[1].legend(loc='upper right')
        >>> plots[1].grid()
        >>> plots[1].set_ylabel('Amplitude')
        >>> plots[1].set_xlim([0, duration])
        >>> plots[1].set_xlabel('Time [s]')
        >>> fig.set_tight_layout('tight')
        >>>         """
    
    assert fc < fs/2, "Carrier frequency 'fc' must be less than 'fs/2'!"
    
    Nt = xmod.shape[0]        # signal length in samples
    T = Nt/fs               # signal length in seconds
    dt = 1/fs               # sampling interval in seconds

    # vector of time samples
    t = np.linspace(0, T-dt, int(T*fs))
    
    # unit-amplitude sinusoidal carrier with frequency 'fc' [Hz]
    xc = np.sin(2*np.pi*fc*t)

    # AM signal
    y_am = (1 + xmod)*xc

    # modulation index
    m = np.max(np.abs(xmod))

    if print_m:
        print(f"AM Modulation index = {m}")
    
    if m > 1:
        print("Warning ['am_sine_generator']: modulation index m > 1\n\tSignal is overmodulated!")

    # Apply amplitude factor to obtain 'spl_level'
    p_ref = 20e-6
    A_rms = p_ref * 10**(spl_level/20)
    y_am *= A_rms/np.std(y_am)

    return y_am, m
