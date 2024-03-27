import numpy as np    
    
def _non_linear_transform(R_est): 
    """Function to apply the non-linear transform on the intermediate roughness results, 
    as defined in section 7.1.7 of ECMA 418-2 (2nd edition, 2022)

    Parameters:
    ------------
    R_est: array
        Estimated roughness values, dim(Ntime50, Nbark)

    Returns:
    ---------
    R_time_spec: array
        Time dependent specific roughness, dim(Ntime50, Nbark)
    """
    
    N50, CBF = R_est.shape
    
    
    # squared mean (Eq. 107)
    R_sq_mean = np.sqrt( np.sum(R_est**2, axis=1) / CBF )
    # linear mean (Eq. 108)
    R_lin_mean = np.mean(R_est, axis=1)
    
    B = np.zeros((N50))
    # Eq. 106
    B[R_lin_mean!=0] = R_sq_mean[R_lin_mean!=0] / R_lin_mean[R_lin_mean!=0]
    # Eq. 105
    E = 0.95555 * (np.tanh( 1.6407 * (B-2.5804) ) + 1) * 0.5 + 0.58449
    
    # calibration factor c_R [asper / Bark_HMS], with a tolerance of 0.25%
    c_R = 0.0180909 * 0.9
    # Estimation of time-dependent specific roughness (Eq. 104)
    R_hat = c_R * np.power(R_est,E[...,np.newaxis])
    

    return R_hat