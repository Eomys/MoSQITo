# -*- coding: utf-8 -*-

# Standard library imports
from numpy import newaxis, array, squeeze

# Local application imports
from mosqito.sound_level_meter.noct_spectrum._filter_bandwidth import _filter_bandwidth
from mosqito.sound_level_meter.noct_spectrum._n_oct_time_filter import _n_oct_time_filter
from mosqito.sound_level_meter.noct_spectrum._center_freq import _center_freq


def noct_spectrum(sig, fs, fmin, fmax, n=3, G=10, fr=1000):
    """Compute nth-octave band spectrum
    
    This function computes the rms level of a signal for each third octave band
    between the 2 limit frequencies.
    
    Parameters
    ----------
    sig : array_like
        Time signal array with size (nperseg, nseg).
    fs : float
        Sampling frequency [Hz]
    fmin : float
        Minimum frequency band [Hz]
    fmax : float
        Maximum frequency band [Hz]
    n : int
        Number of bands per octave
    G : int
        System for specifying the exact geometric mean frequencies.
        Can be base 2 or base 10
    fr : int
        Reference frequency. Shall be set to 1 kHz for audible frequency
        range, to 1 Hz for infrasonic range (f < 20 Hz) and to 1 MHz for
        ultrasonic range (f > 31.5 kHz)

    Returns
    -------
    spec : array_like
        Third octave band spectrum of signal sig with size (nfreq, nseg)
    fpref : array_like
        Corresponding prefered third octave band center frequencies
        
    See Also
    --------
    .comp_spectrum : Spectrum computation from a time signal
    .noct_synthesis : Conversion of a spectrum to n-th octave band levels
            
    Examples
    --------
    .. plot::
       :include-source:

        >>> from mosqito.sound_level_meter import noct_spectrum
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
        >>> spec, freq_axis = noct_spectrum(stimulus, fs, fmin=90, fmax=14000)
        >>> spec_db = amp2db(spec, ref=2e-5)
        >>> plt.step(freq_axis, spec_db)
        >>> plt.xlabel("Center frequency [Hz]")
        >>> plt.ylabel("Amplitude [dB]")
    """

    # 1-dimensional array to 2-dimensional array with size (nperseg, 1)
    if sig.ndim == 1:
        sig = sig[:, newaxis]

    # Get filters center frequencies
    fc_vec, fpref = _center_freq(fmin=fmin, fmax=fmax, n=n, G=G, fr=fr)

    # Compute the filters bandwidth
    alpha_vec, _, _ = _filter_bandwidth(fc_vec, n=n)

    # Calculation of the rms level of the signal in each band
    spec = []
    for fc, alpha in zip(fc_vec, alpha_vec):
        spec.append(_n_oct_time_filter(sig, fs, fc, alpha))

    return squeeze(array(spec)), fpref
