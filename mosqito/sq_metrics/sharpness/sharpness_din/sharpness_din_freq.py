# -*- coding: utf-8 -*-

# Standard library import
from numpy import interp, arange

# Local imports
from mosqito.sq_metrics import loudness_zwst_freq
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import sharpness_din_from_loudness

def sharpness_din_freq(spectrum, freqs, weighting="din", field_type="free"):
    """
    Returns the sharpness value 

    This function computes the sharpness value along time according to different methods.

    Parameters
    -----------
    spectrum : array_like
        A RMS spectrum.
    freqs : array_like
        Frequency axis.
    weighting : {'din', 'aures', 'bismarck', 'fastl'}
        Weighting function used for the sharpness computation. 
        Default is 'din'
    field_type : {'free', 'diffuse'}
        Type of soundfield.
        Default is 'free'
        
    Returns
    --------
    S : numpy.array
        Sharpness value in [acum]

    See Also
    ---------
    sharpness_din_from_loudness : Sharpness computation from loudness values
    sharpness_din_st : Sharpness computation for a stationary time signal
    sharpness_din_tv : Sharpness computation for a non-stationary time signal
    sharpness_din_perseg : Sharpness computation by time-segment


    Notes
    ------
    The different methods account for the weighting function applied on the specific loudness values:
     * DIN 45692 : weighting defined in the standard
     * Aures
     * Bismarck
     * Fastl

    References
    -----------
    .. [DIN45692] Measurement technique for the simulation of the auditory sensation of sharpness, 2009

    Examples
    ---------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import sharpness_din_freq 
       >>> from mosqito.sound_level_meter import comp_spectrum
       >>> import matplotlib.pyplot as plt
       >>> import numpy as np
       >>> fs=48000
       >>> d=0.2
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> f = np.linspace(1000,5000, len(time))
       >>> stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> spec, freqs = comp_spectrum(stimulus, fs, db=False)
       >>> S = sharpness_din_freq(spec, freqs)
       >>> plt.plot(time, stimulus)
       >>> plt.xlim(0, 0.05)
       >>> plt.xlabel("Time [s]")
       >>> plt.ylabel("Amplitude [Pa]")
       >>> plt.title("Sharpness = " + f"{S:.2f}" + " [Acum]")
    """
    # Check the inputs
    if len(spectrum) != len(freqs):
        raise ValueError(
            'Input spectrum and frequency axis must have the same shape')
    
    if (freqs.max() < 24000) or (freqs.min() > 24):
        print("[WARNING] freqs argument is not wide enough to cover the full audio range. Missing frequency bands will be filled with 0. To fulfill the standard requirements, the frequency axis should go from 24Hz up to 24 kHz."
        )
        df = freqs[1] - freqs[0]
        spectrum = interp(arange(0,24000+df, df), freqs, spectrum)
        freqs = arange(0,24000+df, df)
        
    # Compute loudness
    N, N_specific, _ = loudness_zwst_freq(
        spectrum, freqs, field_type=field_type)

    if len(spectrum.shape) > 1:
        raise ValueError(
            "With a 2D spectrum use 'sharpness_din_perseg' calculation.")

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(N, N_specific, weighting=weighting)

    return S

