# -*- coding: utf-8 -*-


# Standard library imports
from numpy import multiply, sqrt
from scipy.signal import butter, sosfreqz

def _n_oct_freq_filter(spectrum, fs, fc, alpha, n=3):  
    """ n-th octave filtering in frequency domain

    Designs a digital 1/3-octave filter with center frequency fc for
    sampling frequency fs. 

    Parameters
    ----------
    spec : numpy.ndarray
        Frequency spectrum [complex]
    fs : float
        Sampling frequency [Hz]
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
    # Get FRF and apply it
    w, h = sosfreqz(sos, worN=len(spectrum))
    spec_filt = multiply(h, spectrum.T).T
    
    # Compute overall rms level
    level = sqrt(sum(abs(spec_filt) ** 2, axis=0)) 
        
    return level
