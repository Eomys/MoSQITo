# -*- coding: utf-8 -*-


# Standard library imports
import numpy as np
from scipy.signal import butter, sosfreqz

def _n_oct_freq_filter(spectrum, fs, factor, fc, alpha, n=3):  
    """ n-th octave filtering in frequency domain

    Designs a digital 1/3-octave filter with center frequency fc for
    sampling frequency fs. 

    Parameters
    ----------
    spec : numpy.ndarray
        Frequency spectrum [complex]
    fs : float
        Sampling frequency [Hz]
    factor : integer
        Downsampling factor
    fc : float
        Filter exact center frequency [Hz]
    alpha : float
        Ratio of the upper and lower band-edge frequencies to the mid-band
        frequency
    n : int, optional
        Filter order. Default to 3

    Outputs
    -------
    level : float
        Rms level of sig in the third octave band centered on fc
    """

    # Normalized cutoff frequencies
    w1 = fc / (fs  / 2) / alpha
    w2 = fc / (fs  / 2) * alpha

    # Define filter coefficient
    sos = butter(n, [w1, w2], "bandpass", analog=False, output ='sos')
    
    # # filter signal
    # if len(spectrum.shape)>1:
    #     level = []
    #     # go into frequency domain
    #     w, h = freqz(b, a, worN=spectrum.shape[1])
    #     for i in range(spectrum.shape[0]):
    #         spec_filt = spectrum[i,:] * h
    #         # Compute overall rms level
    #         level.append(np.sqrt(np.sum(np.abs(spec_filt) ** 2)))
    #     level = np.array(level)
    # else:
    #     # go into frequency domain
    #     w, h = freqz(b, a, worN=len(spectrum))
    #     spec_filt = spectrum * h
    #     # Compute overall rms level
    #     level = np.sqrt(np.sum(np.abs(spec_filt) ** 2)) 
    
    
    # Get FRF and apply it
    w, h = sosfreqz(sos, worN=len(spectrum))
    spec_filt = np.multiply(h, spectrum.T).T
    
    # Compute overall rms level
    level = np.sqrt(np.sum(np.abs(spec_filt) ** 2, axis=0)) 
        
    return level
