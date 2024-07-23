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
    fs_50 = 50
    N50, CBF = R_hat.shape
    
    # Find indices where R_hat increases or remains the same over time (rising slopes)
    R_rising = np.zeros(R_hat.shape).astype(bool)
    R_rising[:, 1:] = (np.diff(R_hat, axis=-1) >= 0)
    
    # Find indices where R_hat decreases over time (falling slopes)
    R_falling = np.logical_not(R_rising)
    
    # Filtering time constants (Eq. 110)
    tau = np.zeros(R_hat.shape)
    tau[R_rising] = 0.0625
    tau[R_falling] = 0.5000
    
    # Time-dependent specific roughness calculation (Eq. 109)
    exp_ = np.exp(-1 / ( fs_50 * tau ) )
    
    R_spec = np.zeros(R_hat.shape)
    #  First time block l_50 = 0
    R_spec[:, 0] = R_hat[:, 0]

    # Following time blocks l=50 >=1
    R_spec[:, 1:] = ( R_hat[:, 1:] * (1 - exp_[:, 1:])
                     + R_hat[:, 0:-1] * exp_[:, 1:] )
    
    # Apply filter (Eq. 109)
    R_time_spec = np.zeros((N50, CBF))
    R_time_spec[0,:] = R_hat[0,:]
    R_time_spec[1:,:] = (R_hat[1,:]*(1-np.exp(-1/(50*tau[1,:])))  + R_hat[0:-1,:]*np.exp(-1/(50*tau[1,:])))

    return R_time_spec