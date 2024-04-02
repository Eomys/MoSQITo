import numpy as np


def am_broadband_noise_generator(mod_signal, dB_level, print_MI=False):
    """
    Creates a amplitude-modulated (AM) signal from a Gaussian broadband (noise) 
    carrier, and the input arbitrary modulating signal 'mod_signal', at
    sampling frequency 'fs'. The AM signal length is the same as the length of
    'mod_signal'. The signal level is then adjusted to a specific dB level.
    
    Parameters
    ----------
    mod_signal: array
        Array containing the modulating signal.
    dB_level: float
        Sound Pressure Level in dB [ref 2e-5 Pa RMS]        
    print_MI: Bool, optional
        If True, the modulation index is printed along calculation, 
        if False it is printed only in case of overmodulation.
        Default to False

    Returns
    -------
    am_signal: numpy.array
        Amplitude-modulated noise signal
    MI: float
        Modulation index
    
    Notes
    -----
    The modulation index MI is equal to the peak value of the modulating
    signal 'mod_signal'. Its value can be printed by setting the optional flag
    'print_MI' to True.
    
    Examples
    --------
    .. plot::
       :include-source:
       
        >>> from mosqito.utils import am_broadband_noise_generator
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fs=48000
        >>> d = 1
        >>> dB=60
        >>> fmod=4
        >>> mdepth = 1
        >>> time = np.arange(0, d, 1/fs)
        >>> sine_wave = np.sin(2*np.pi*fmod*time)
        >>> signal, MI = am_broadband_noise_generator(sine_wave, dB, True)
        >>> plt.plot(time, signal)
        >>> plt.xlabel("Time axis [s]")
        >>> plt.ylabel("Amplitude signal [Pa]")    
        >>> plt.title(f'Modulation index = {MI}')
        
    """
    
    # signal length in samples
    Nt = mod_signal.shape[0]
    
    # create vector of zero-mean, unitary std dev random samples
    rng = np.random.default_rng()
    xc = rng.standard_normal(Nt)    

    # normalise broadband signal energy to 'spl_level' [dB SPL ref 20 uPa]
    p_ref = 20e-6
    A_rms = p_ref * 10**(dB_level/20)
    xc *= A_rms/np.std(xc)
    
    # AM signal
    am_signal = (1 + mod_signal)*xc

    # AM modulation index
    MI = np.max(np.abs(mod_signal))

    if print_MI:
        print(f"AM Modulation index = {MI}")
    
    if MI > 1:
        print("Warning ['am_broadband_noise_generator']: modulation index MI > 1\n\tSignal is overmodulated!")

    return am_signal, MI

