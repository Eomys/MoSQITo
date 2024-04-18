import numpy as np
from scipy.interpolate import pchip_interpolate

def _interpolation_50(amplitude, time, duration):
    """ Interpolation to 50 Hz
    
    Function to interpolate the amplitude[l,z] to 50 Hz with a piecewise cubic Hermitian function,
    as defined in section 7.1.7 of ECMA 418-2 (2nd edition, 2022)
    
    Parameters:
    ----------
    amplitude: array
        Modulation amplitude, dim(Ntime, Nbark)
    time: array
        Time axis
    duration: float
        Time duration of the signal in s.
    
    Returns:
    --------
    A_50: array
        Interpolated amplitude
    t_50: array
        New time array sampled at 50 Hz
    
    """
    # New sampling rate of 50 Hz
    rs_50 = 50
    
    # Last sample to be evaluated (Eq. 103) to removezero-padding from preprocessing
    N50 = int(duration*rs_50)
    
    # New time axis
    t_50 = np.arange(N50) / rs_50
    
    # Piecewise cubic Hermitian Interpolating Polynomial (PCHIP)
    A_50 = pchip_interpolate(time, amplitude, t_50, axis=0)
    
    return A_50, t_50
