import numpy as np

def fm_sine_wave_generator(fs, mod_signal, fc, k, dB_level, print_info=False):
    """
    Creates a frequency-modulated (FM) signal with a sinusoidal carrier at 
    frequency 'fc', and an arbitrary modulating signal 'mod_signal'.
    The FM signal length is the same as the length of 'mod_signal'. 
    The signal level is then adjusted to a specific dB level.
    
    Parameters
    ----------
    fs: float
        Sampling frequency, in [Hz].
    mod_signal: array
        Modulating signal.    
    fc: float
        Carrier frequency, in [Hz]. Must be less than 'fs/2'.
    k: float
        Frequency sensitivity of the modulator. This is equal to the frequency
        deviation in Hz away from 'fc' per unit amplitude of the modulating
        signal 'mod_signal'.

    dB_level: float
        Sound Pressure Level in dB [ref 2e-5 Pa RMS]        
    
    print_info: Bool, optional
        If True, the maximum frequency deviation and FM modulation index 
        are printed along calculation. 
        Default to False    
    
    Returns
    -------
    fm_signal: numpy.array
        Frequency-modulated signal with sine carrier
    inst_freq: numpy.array
        Instantaneaous frequency [Hz]    
    f_delta: float
        Maximum frequency deviation
    MI: float
        Modulation index
            
    Examples
    --------
    .. plot::
       :include-source:

        >>> from mosqito.utils import fm_sine_wave_generator
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fs=48000
        >>> d = 1
        >>> dB=60
        >>> fc=50
        >>> fmod=10
        >>> k = fc//2
        >>> time = np.arange(0, d, 1/fs)
        >>> sine_wave = np.sin(2*np.pi*fmod*time)
        >>> signal, inst_freq, f_delta, MI = fm_sine_wave_generator(fs, sine_wave, fc, k, dB, True)
        >>> plt.figure()
        >>> plt.plot(time, signal)
        >>> plt.xlabel("Time axis [s]")
        >>> plt.ylabel("Amplitude signal [Pa]")    
        >>> plt.title(f'Modulation index = {MI:.1f}')
        >>> plt.figure()
        >>> plt.xlabel("Time axis [s]")
        >>> plt.ylabel("Instantaneous frequency [Hz]")    
        >>> plt.title(f'Max frequency deviation = {f_delta:.1f}')
        >>> plt.plot(time, inst_freq)

    """
    
     # sampling interval in seconds
    dt = 1/fs

    # instantaneous frequency of FM signal
    inst_freq = fc + k  *mod_signal
    
    # FM signal
    p_ref = 20e-6
    A = np.sqrt(2) * p_ref * 10**(dB_level/20)
    fm_signal = A*np.sin(2*np.pi * np.cumsum(inst_freq)*dt)
    
    # max frequency deviation
    f_delta = k*np.max(np.abs(mod_signal))
    
    # FM modulation index
    MI = np.max(np.abs(2*np.pi*k*np.cumsum(mod_signal)*dt))
    
    if print_info:
        print(f'\tMax freq deviation: {f_delta} Hz')
        print(f'\tFM modulation index: {MI:.2f} Hz')

    return fm_signal, inst_freq, f_delta, MI

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    plt.show(block=True)