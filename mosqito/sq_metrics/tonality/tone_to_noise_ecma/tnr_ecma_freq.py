# -*- coding: utf-8 -*-

# External import
from numpy import asarray, float32, abs
# Local functions imports
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc
from mosqito.utils import amp2db

def tnr_ecma_freq(spectrum, freqs,  prominence=True):
    """
    Returns the tone-to-noise ratio value 
    
    This function computes the tone-to-noise ratio according to ECMA-74, annex D.9
    from a sound spectrum.

    Parameters
    ----------
    spectrum : array_like
        Amplitude or complex frequency spectrum, dim(nperseg x nseg).
    freqs : array_like
        Frequency axis dim(nperseg x nseg) or ([)nperseg). 
    prominence : Bool
        If True, the algorithm only returns the prominent tones, if False it returns all tones detected.
        Default to True

    Returns
    -------
    t_tnr : float
        Global TNR value.
    tnr : array of float
        TNR values for each detected tone.
    promi : array of bool
        Prominence criterion for each detected tone.
    tones_freqs : array of float
        Frequency of the detected tones.

    See Also
    --------
    .pr_ecma_freq : PR computation for a sound spectrum
    .tnr_ecma_st : TNR for a stationary signal
    .tnr_ecma_tv : TNR computation for a non-stationary signal
    
    Notes
    -----
    The algorithm automatically detects the frequency of the tonal components according to Sottek method.

    
    References
    ----------
    :cite:empty:`TNR-ECMA-418-2`
    
    .. bibliography::
        :keyprefix: TNR-
            
    Examples
    --------
    The example stimulus is made of white noise + 2 sine waves at 1kHz and 3kHz.

    .. plot::
       :include-source:
       
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from mosqito.sound_level_meter import comp_spectrum
        >>> fs = 48000
        >>> d = 2
        >>> f = 1000
        >>> dB = 60
        >>> time = np.arange(0, d, 1/fs)
        >>> stimulus = np.sin(2 * np.pi * f * time) + 0.5 * np.sin(2 * np.pi * 3 * f * time)+ np.random.normal(0,0.5, len(time))
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> spectrum_db, freq_axis = comp_spectrum(stimulus, fs, db=True)
        >>> plt.plot(freq_axis, spectrum_db)
        >>> plt.ylim(0,60)
        >>> plt.xlabel("Frequency [Hz]")
        >>> plt.ylabel("Acoustic pressure [dB]")

    .. plot::
       :include-source:
       
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from mosqito.sq_metrics import tnr_ecma_freq
        >>> from mosqito.sound_level_meter import comp_spectrum
        >>> fs = 48000
        >>> d = 2
        >>> f = 1000
        >>> dB = 60
        >>> time = np.arange(0, d, 1/fs)
        >>> stimulus = np.sin(2 * np.pi * f * time) + 0.5 * np.sin(2 * np.pi * 3 * f * time)+ np.random.normal(0,0.5, len(time))
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> spec, freq_axis = comp_spectrum(stimulus, fs, db=False)
        >>> t_tnr, tnr, prom, tones_freqs = tnr_ecma_freq(spec.T, freq_axis.T)
        >>> plt.bar(tones_freqs, tnr, width=50)  
        >>> plt.grid(axis='y')
        >>> plt.ylabel("TNR [dB]")     
        >>> plt.title("Total TNR = "+ f"{t_tnr[0]:.2f}" + " dB")
        >>> plt.xscale('log')
        >>> xticks_pos = list(tones_freqs) + [100,1000,10000]
        >>> xticks_pos = np.sort(xticks_pos)
        >>> xticks_label = [str(elem) for elem in xticks_pos]
        >>> plt.xticks(xticks_pos, labels=xticks_label, rotation = 30)   
        >>> plt.xlabel("Frequency [Hz]")     
    """                 
    if len(spectrum) != len(freqs) :
        raise ValueError('Input spectrum and frequency axis must have the same size')
    
    # Compute spectrum dB values
    spectrum_db = amp2db(abs(spectrum), ref=2e-5)
            
    # compute TNR values
    tones_freqs, tnr, prom, t_tnr = _tnr_main_calc(spectrum_db, freqs)
  
    if prominence == False:
        return t_tnr, tnr, prom, tones_freqs
    else:
        return t_tnr, asarray(tnr, float32)[asarray(prom, bool)], asarray(prom, bool)[asarray(prom, bool)], asarray(tones_freqs, float32)[asarray(prom, bool)]
