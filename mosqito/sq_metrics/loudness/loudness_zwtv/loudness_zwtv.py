# -*- coding: utf-8 -*-

# Standard library imports
from numpy import linspace

# Local applications imports
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import _main_loudness
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import _calc_slopes
from mosqito.sq_metrics.loudness.loudness_zwtv._nonlinear_decay import _nl_loudness
from mosqito.sq_metrics.loudness.loudness_zwtv._temporal_weighting import _temporal_weighting
from mosqito.sq_metrics.loudness.loudness_zwtv._third_octave_levels import _third_octave_levels


def loudness_zwtv(signal, fs, field_type='free'):
    """
    Returns the loudness value 

    This function computes the acoustic loudness according to Zwicker method for
    time-varying signals.
    
    Parameters
    ----------
    signal: array_like or DataTime object
        Signal time values [Pa], dim (nperseg, nseg).
    fs : float, optional
        Sampling frequency, can be omitted if the input is a DataTime object. 
        Default to None
    field_type : {'free', 'diffuse'}
        Type of soundfield.
        Default is 'free'
        
    Returns
    -------
    N : float
        Overall loudness [sones], size (Ntime,).
    N_specific : numpy.ndarray
        Specific loudness [sones/bark], size (Nbark, Ntime).
    bark_axis : numpy.ndarray
        Bark axis, size (Nbark,).
    time_axis : numpy.ndarray
        Time axis, size (Ntime,).
    
    See Also
    --------
    loudness_zwst : Loudness computation for a stationary time signal
    loudness_zwst_perseg : Loudness computation by time-segment
    loudness_zwst_freq : Loudness computation from a sound spectrum

    Notes
    -----
    Normative reference:
        ISO 532:1975 (method B)
        DIN 45631:1991
        ISO 532-1:2017 (method 1)
    Due to normative continuity, as defined in the preceeding standards, the method is in accordance with
    ISO 226:1987 equal loudness contours (instead of ISO 226:2003).
    
    References
    ----------
    :cite:empty:`L_zw-ZF91`

    .. bibliography::
        :keyprefix: L_zw-
            
    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import loudness_zwtv
       >>> import matplotlib.pyplot as plt
       >>> import numpy as np
       >>> fs=48000
       >>> d=1
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> f = np.linspace(1000,5000, len(time))
       >>> stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> N, N_spec, bark_axis, time_axis = loudness_zwtv(stimulus, fs)
       >>> plt.plot(time_axis, N)
       >>> plt.xlabel("Time [s]")
       >>> plt.ylabel("Loudness [Sone]")
    """
    if fs < 48000:
        print("[Warning] Signal resampled to 48 kHz to allow calculation. To fulfill the standard requirements fs should be >=48 kHz."
             )
        from scipy.signal import resample
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000
    
    # Compute third octave band spectrum vs. time
    spec_third, time_axis, _ = _third_octave_levels(signal, fs)

    # Calculate core loudness (vectorized version)
    core_loudness = _main_loudness(spec_third, field_type)

    #
    # Nonlinearity
    core_loudness = _nl_loudness(core_loudness)
    #
    # Calculation of specific loudness
    loudness, spec_loudness = _calc_slopes(core_loudness)

    # temporal weigthing
    filt_loudness = _temporal_weighting(loudness)
    #
    # Decimation from temporal resolution 0.5 ms to 2ms and return
    dec_factor = 4
    N = filt_loudness[::dec_factor]
    N_spec = spec_loudness[:, ::dec_factor]
    time_axis = time_axis[::dec_factor]
    #
    # Build bark axis
    bark_axis = linspace(0.1, 24, int(24 / 0.1))

    return N, N_spec, bark_axis, time_axis

