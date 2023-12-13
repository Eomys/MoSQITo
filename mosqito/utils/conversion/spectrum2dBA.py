from numpy import array, linspace, interp, zeros

def spectrum2dBA(spectrum, fs):
    """A_weighting dB ponderation 
    
    This function does the dBA weighting of a spectrum according to CEI 61672:2014.
    

    Parameters
    ----------
    spectrum: array_like
        Input spectrum in [dB].
    fs: integer
        Sampling frequency in [Hz].
        
    Returns
    -------
    spectrum_dba: array_like
        dBA spectrum.
        
    Notes
    -----
    Third-octave spectrum are directly calculated, other are calculated
    using linear interpolation.

    See Also
    --------
    noct_spectrum : n-th octave band spectrum computation from a time signal
            
    Examples
    --------
    .. plot::
       :include-source:

        >>> from mosqito.sound_level_meter import noct_synthesis
        >>> from mosqito.utils import amp2db
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> f=1000
        >>> fs=48000
        >>> d=0.2
        >>> dB=60
        >>> time = np.arange(0, d, 1/fs)
        >>> stimulus = np.sin(2 * np.pi * f * time) + 0.5 * np.sin(6 * np.pi * f * time)
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> n = len(stimulus)
        >>> spec = np.abs(2/np.sqrt(2)/n*np.fft.fft(stimulus)[:n//2])
        >>> freqs = np.linspace(0, fs//2,n//2)
        >>> spec_3, freq_axis = noct_synthesis(spec, freqs, fmin=90, fmax=14000)
        >>> spec_3db = amp2db(spec_3, ref=2e-5)
        >>> plt.step(freq_axis, spec_3db)
        >>> plt.ylim(0,60)
        >>> plt.xlabel("Center frequency [Hz]")
        >>> plt.ylabel("Amplitude [dB]")
    """



    # Ponderation coefficients from the standard
    A_standard = array(
        [
            -70.4,
            -63.4,
            -56.7,
            -50.5,
            -44.7,
            -39.4,
            -34.6,
            -30.2,
            -26.2,
            -22.5,
            -19.1,
            -16.1,
            -13.4,
            -10.9,
            -8.6,
            -6.6,
            -4.8,
            -3.2,
            -1.9,
            -0.8,
            0,
            0.6,
            1,
            1.2,
            1.3,
            1.2,
            1,
            0.5,
            -0.1,
            -1.1,
            -2.5,
            -4.3,
            -6.6,
            -9.3,
        ]
    )

    freq_standard = array(
        [
            10,
            12.5,
            16,
            20,
            25,
            31.5,
            40,
            50,
            63,
            80,
            100,
            125,
            160,
            200,
            250,
            315,
            400,
            500,
            630,
            800,
            1000,
            1250,
            1600,
            2000,
            2500,
            3150,
            4000,
            5000,
            6300,
            8000,
            10000,
            12500,
            16000,
            20000,
        ]
    )

    # Linear interpolation on the spectrum axis
    spectrum_freq_axis = linspace(0, int(fs / 2), spectrum.size)
    A_pond = interp(spectrum_freq_axis, freq_standard, A_standard)

    # Ponderation of the given spectrum
    spectrum_dBA = zeros(spectrum.shape)
    for i in range(spectrum.shape[0]):
        spectrum_dBA[i] = spectrum[i] + A_pond[i]

    return spectrum_dBA