# -*- coding: utf-8 -*-

# Local imports
from mosqito.sq_metrics import loudness_zwst
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import sharpness_din_from_loudness

def sharpness_din_st(signal, fs, weighting="din", field_type="free"):
    """
    Returns the sharpness value 

    This function computes the sharpness value according to different methods.

    Parameters
    ----------
    signal: array_like
        Input time signal in [Pa], dim (nperseg, nseg)
    fs: float
        Sampling frequency
    weighting : {'din', 'aures', 'bismarck', 'fastl'}
        Weighting function used for the sharpness computation. 
        Default is 'din'
    field_type : {'free', 'diffuse'}
        Type of soundfield.
        Default is 'free'

    Returns
    -------
    S : float
        Sharpness value in [acum], dim (nseg)

    See Also
    --------
    .sharpness_din_from_loudness : Sharpness computation from loudness values
    .sharpness_din_tv : Sharpness computation for a time-varying signal
    .sharpness_din_perseg : Sharpness computation by time-segment
    .sharpness_din_freq : Sharpness computation from a sound spectrum
    
    Notes
    -----
    The different methods account for the weighting function applied on the specific loudness values:
     * DIN 45692 : weighting defined in the standard
     * Aures
     * Bismarck
     * Fastl

    References
    ----------
    :cite:empty:`S-DIN.45692:2009`
    :cite:empty:`S-ZF:9`
    :cite:empty:`S-B74`
    
    .. bibliography::
        :keyprefix: S-

    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import sharpness_din_st 
       >>> import matplotlib.pyplot as plt
       >>> import numpy as np
       >>> f=1000
       >>> fs=48000
       >>> d=0.2
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> S = sharpness_din_st(stimulus, fs=fs)
       >>> plt.plot(time, stimulus)
       >>> plt.xlim(0, 0.05)
       >>> plt.xlabel("Time [s]")
       >>> plt.ylabel("Amplitude [Pa]")
       >>> plt.title("Sharpness = " + f"{S:.2f}" + " [Acum]")
    """
    if fs < 48000:
        print("[Warning] Signal resampled to 48 kHz to allow calculation. To fulfill the standard requirements fs should be >=48 kHz."
             )
        from scipy.signal import resample
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000

    # Compute loudness
    N, N_specific, _ = loudness_zwst(signal, fs, field_type=field_type)

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(N, N_specific, weighting=weighting)

    return S

