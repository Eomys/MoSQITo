import numpy as np    
    
def _non_linear_transform(R_est): 
    """Function to apply the non-linear transform on the intermediate roughness results.
    
    This version is adapted from section 7.1.7 of ECMA 418-2 (2nd edition, 2022), 
    based on [1] R. Sottek, J. Becker, T. Lobato, "Progress in Roughness Calculation", 
    Proceedings of Internoise 2020, p.2835, 2846, Seoul, South Korea.
    The parameters have been adapted to get a better fitting of the reference values
    based on the modulation and carrier frequencies.

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
    
    # Eq. 106
    B = np.zeros((N50))
    B[R_lin_mean!=0] = R_sq_mean[R_lin_mean!=0] / R_lin_mean[R_lin_mean!=0]
    
    # !!! ~Eq. 105 !!!
    # Equation from the article [1] instead of ECMA 418-2 to get a better fitting 
    # of the results values
    E = 0.25 * (np.tanh(1.75 * (B-2.5) )) + 0.7
    
    # !!! calibration factor c_R [asper / Bark_HMS]
    # The value has been corrected to get better results
    c_R = 0.045
    
    # Estimation of time-dependent specific roughness (Eq. 104)
    R_hat = c_R * np.power(R_est,E[...,np.newaxis])
    

    return R_hat


