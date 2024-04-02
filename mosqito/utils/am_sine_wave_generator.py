import numpy as np

def am_sine_wave_generator(d, fs, fc, fmod, MI , dB_level):
    """ Amplitude-modulated sine wave generation
    
    Creates a amplitude-modulated (AM) signal with a sinusoidal carrier at 
    fc [Hz] and a modulation sine at fmod [Hz], whose amplitude ratio is MI.
    The signal level is then adjusted to a specific dB level.
    
    Parameters
    ----------
    d: float 
        duration in [s]
    fs: integer
        sampling frequency
    fc: float
        Carrier frequency in [Hz]. Must be less than fs/2.
    fmod: numpy.array
        Modulation frequency in [Hz]. Must be between 20 and 300 Hz to generate roughness.
    MI: float
        Modulation index, between 0 and 1.
    dB_level: float
        Sound Pressure Level in dB [ref 2e-5 Pa RMS]        
    
    Returns
    -------
    signal: numpy.array
        Amplitude modulated signal from sine carrier
        
    Examples
    --------
    .. plot::
       :include-source:

        >>> from mosqito.utils import am_sine_wave_generator
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fs=48000
        >>> d=1
        >>> dB=60
        >>> fc=100
        >>> fmod=4
        >>> mdepth = 1
        >>> time = np.arange(0, d, 1/fs)
        >>> signal = am_sine_wave_generator(d, fs, fc, fmod, mdepth , dB)
        >>> plt.plot(time, signal)
        >>> plt.xlabel("Time axis [s]")
        >>> plt.ylabel("Amplitude signal [Pa]")

"""
    
    # time axis definition
    dt = 1 / fs
    time = np.arange(0, d, dt)

    # Modulated sine wave
    stimulus = (
        0.5
        * (1 + MI * (np.sin(2 * np.pi * fmod * time)))
        * np.sin(2 * np.pi * fc * time)
    )
    # Level adjustement
    rms = np.sqrt(np.mean(np.power(stimulus, 2)))
    p_ref = 2e-5
    ampl = p_ref * np.power(10, dB_level / 20) / rms
    signal = stimulus * ampl
    
    return signal
    
    
    
    
    
    
    
    
    
    

