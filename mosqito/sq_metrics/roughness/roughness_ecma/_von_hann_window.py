import numpy as np

def _von_hann_window(N):
    """
    Calculates the Von Hann window as defined in 
    ECMA-418-2 (2nd Ed, 2022) standard, used for calculating roughness.
    
    Returns
    -------
    hann : numpy.array
        Array containing the samples of the Von Hann weighting function.
    """
    
    arg1 = 2 * np.pi * np.arange(N) / N
    
    return (0.5 - 0.5*np.cos(arg1)) / np.sqrt(0.375)   

