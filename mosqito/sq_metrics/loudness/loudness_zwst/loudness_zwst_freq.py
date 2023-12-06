# -*- coding: utf-8 -*-

# Third party imports
import numpy as np

# Local application imports
from mosqito.sound_level_meter.noct_spectrum.noct_synthesis import noct_synthesis
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import _main_loudness
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import _calc_slopes
from mosqito.utils.conversion import amp2db


def loudness_zwst_freq(spectrum, freqs, field_type="free"):
    """
    Returns the loudness value 

    This function computes the acoustic loudness according to Zwicker method for
    stationary signals.
    
    Parameters
    ----------
    spectrum : array_like
        A RMS spectrum.
    freqs : array_like
        Frequency axis.
    field_type : {'free', 'diffuse'}
        Type of soundfield corresponding to spec_third.
        Default is 'free'
                
    Returns
    -------
    N : float or array_like
        Overall loudness array in [sones], size (Ntime,).
    N_specific : array_like
        Specific loudness array [sones/bark], size (Nbark, Ntime).
    bark_axis: array_like
        Bark axis array, size (Nbark,).

    See Also
    --------
    loudness_zwst : loudness computation for a stationary time signal
    loudness_zwst_perseg : loudness computation by time-segment
    loudness_zwtv : loudness computation for a non-stationary time signal

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
    .. [ZF] E.Zwicker and H.Fastl, "Program for calculating loudness according to DIN 45631 (ISO 532B)", 
            J.A.S.J (E) 12, 1 (1991).
        
    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import loudness_zwst_freq 
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
       >>> n = len(stimulus)
       >>> spec = np.abs(2/np.sqrt(2)/n*np.fft.fft(stimulus)[:n//2])
       >>> freqs = np.linspace(0, fs//2,n//2)
       >>> N, N_spec, bark_axis = loudness_zwst_freq(spec, freqs)
       >>> plt.plot(bark_axis, N_spec)
       >>> plt.xlabel("Frequency band [Bark]")
       >>> plt.ylabel("Specific loudness [Sone/Bark]")
       >>> plt.title("Loudness = " + f"{N:.2f}" + " [Sone]")       
    """
    
    if len(spectrum) != len(freqs):
        raise ValueError('Input spectrum and frequency axis must have the same shape')

    # Compute third octave band spectrum
    spec_third, _ = noct_synthesis(spectrum, freqs, fmin=24, fmax=12600)

    # Compute dB values
    spec_third = amp2db(spec_third, ref=2e-5)

    # Compute main loudness
    Nm = _main_loudness(spec_third, field_type)
    #
    # Computation of specific loudness pattern and integration of overall
    # loudness by attaching slopes towards higher frequencies
    N, N_specific = _calc_slopes(Nm)

    # Define Bark axis
    bark_axis = np.linspace(0.1, 24, int(24 / 0.1))

    return N, N_specific, bark_axis
