import numpy as np
    
def _lowpass_filter(R_hat):
    """
    Implements the lowpass filtering from section 7.1.7 of ECMA-418-2 (2nd Ed,
    2022) standard for calculating roughness. It uses different time constants
    for the rising and falling slopes, as the perception of sound events rises
    quickly with the beginning of the event but decays slowly with the event
    end.
    
    Parameters
    ----------
    R_hat : array
        Array of specific roughness calibrated values, dim (Ntime50, Nbark)
        
    Returns
    -------
    R_time_spec : numpy.array
        Time-dependent specific roughness, dim (Ntime50, Nbark)
    """
    N50, CBF = R_hat.shape
    
    # Slope of the specific roughness values to distinguish rising from falling slopes
    slope = np.vstack((R_hat[None,0,:], np.diff(R_hat, axis=0)[:-1,:]))
    
    # Time constants for rising and falling slopes (Eq. 110)
    tau = np.zeros((N50-1,CBF))
    tau[np.where((slope>=0))] = 0.0625
    tau[np.where((slope<0))] = 0.5000
    
    # Apply filter (Eq. 109)
    R_time_spec = np.zeros((N50, CBF))
    R_time_spec[0,:] = R_hat[0,:]
    R_time_spec[1:,:] = (R_hat[1:,:]*(1-np.exp(-1/(50*tau)))  + R_hat[:-1,:]*np.exp(-1/(50*tau)))

    return R_time_spec