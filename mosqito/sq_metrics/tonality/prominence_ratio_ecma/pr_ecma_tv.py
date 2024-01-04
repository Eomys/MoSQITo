# -*- coding: utf-8 -*-

# Standard library import
from numpy import linspace, logspace, empty, nan, argmin, log10, ravel, abs
import numpy.random as rd

# Local imports
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.sound_level_meter.comp_spectrum import comp_spectrum
from mosqito.sq_metrics.tonality.prominence_ratio_ecma._pr_main_calc import _pr_main_calc


def pr_ecma_tv(signal, fs, prominence=True, overlap=0):
    """
    Returns the tone-to-noise ratio value 
    
    This function computes the prominence ratio according to ECMA-74, annex D.9
    for a non-stationary signal.

    Parameters
    ----------
    signal :numpy.array
        Signal time values in [Pa].
    fs : integer
        Sampling frequency.
    prominence : Bool
        If True, the algorithm only returns the prominent tones, if False it returns all tones detected.
        Default to True
    overlap : float
        Overlapping coefficient for the time windows of 200ms.
        Default to 0

    Returns
    -------
    t_pr : float
        Global PR value.
    pr : array of float
        PR values for each detected tone.
    promi : array of bool
        Prominence criterion for each detected tone.
    freqs : array_like
        Frequency axis [Hz].
    time : array_like
        Time axis [s].

    See Also
    --------
    .pr_ecma_freq : PR computation for a sound spectrum
    .pr_ecma_st : PR computation for a stationary signal
    .tnr_ecma_tv : TNR for a non-stationary signal
    
    Notes
    -----
    The computation is realised over successive time windows of 500ms.
    For each time window, the computation is based on a spectrum analysis detecting peaks to be compared with the overall smoothed spectrum.  
    The algorithm automatically detects the frequency of the tonal components according to Sottek's method.

    .. math::
        \\Delta L_{TNR} = L_{peak} - 10\\log_{10}\\left (10^{0.1L_{peakband}} -10^{0.1L_{peak}}\\right ) 
        
    .. math::
        \\Delta L_{PR} = 10\\log_{10}\\left ( 10^{0.1L_{peakband}} \\right ) - 10\\log_{10}\\left [0.5\\left (10^{0.1L_{lowerband}} -10^{0.1L_{upperband}}\\right )\\right]

    The difference between PR and TNR lies in the comparison process between the peak level and the background noise amplitude. 
    TNR compares the peak level to the level of its critical band, while PR compares the level of the peak's critical band to its two neighbor bands. 
    According to ECMA 74 standard, TNR can then prove to be more accurate for multiple tones in adjacent critical bands, for example when strong harmonics exist. 
    PR can be more effective for multiple tones within the same critical band and is more readily automated to handle such cases. 

    Along with the TNR/PR value comes a prominence indicator, a tone being considered as prominent if its dB level is sufficiently higher than the smoothed spectrum, depending on its frequency.

    
    References
    ----------
    :cite:empty:`PR-ECMA-418-2`
    
    .. bibliography::
        :keyprefix: PR-
            
    Examples
    --------
    The example stimulus is made of white noise + 2 sine waves at 1kHz and 3kHz.

    .. plot::
       :include-source:
       
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from mosqito.sq_metrics import pr_ecma_tv
        >>> fs = 48000
        >>> d = 2
        >>> dB = 60
        >>> time = np.arange(0, d, 1/fs)
        >>> f1 = 1000
        >>> f2 = np.zeros((len(time)))
        >>> f2[len(time)//2:] = 1500
        >>> stimulus = 2 * np.sin(2 * np.pi * f1 * time) + np.sin(2 * np.pi * f2 * time)+ np.random.normal(0,0.5, len(time))
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> t_pr, pr, promi, tones_freqs, time = pr_ecma_tv(stimulus, fs)
        >>> plt.figure(figsize=(10,8))
        >>> plt.pcolormesh(time, tones_freqs, np.nan_to_num(pr), vmin=0)
        >>> plt.colorbar(label = "PR value in dB")
        >>> plt.xlabel("Time [s]")
        >>> plt.ylabel("Frequency [Hz]")
        >>> plt.ylim(90,2000)
        """        
    if len(signal.shape) == 1:
      
        # Number of points within each frame according to the time resolution of 500ms
        nperseg = int(0.5 * fs)
        # Overlappinf segment length
        noverlap = int(overlap * nperseg)               
        # Time segmentation of the signal
        sig, time = time_segmentation(signal, fs, nperseg=nperseg, noverlap=noverlap, is_ecma=False)
        # Number of segments
        nseg = sig.shape[1]        
        # Spectrum computation
        spectrum_db, freq_axis = comp_spectrum(sig, fs, db=True)
        
    else:
        nseg = signal.shape[1]
        time = linspace(0, nseg/fs, num=nseg)
        
        # Compute spectrum
        spectrum_db, freq_axis = comp_spectrum(sig, fs, db=True)
            
            
    # compute tnr values
    tones_freqs, pr_, prom, t_pr = _pr_main_calc(spectrum_db, freq_axis)
            
    # Retore the results in a time vs frequency array
    freqs = logspace(log10(90), log10(11200), num=1000)
    pr = empty((len(freqs), nseg))
    pr.fill(nan)
    promi = empty((len(freqs), nseg), dtype=bool)
    promi.fill(False)
    
    for t in range(nseg):
        for f in range(len(tones_freqs[t])):
            ind = argmin(abs(freqs - tones_freqs[t][f]))
            if prominence == False:
                pr[ind, t] = pr_[t][f]
                promi[ind, t] = prom[t][f]
            if prominence == True:
                if prom[t][f] == True:
                    pr[ind, t] = pr_[t][f]
                    promi[ind, t] = prom[t][f]

    t_pr = ravel(t_pr)

    return t_pr, pr, promi, freqs, time 
    