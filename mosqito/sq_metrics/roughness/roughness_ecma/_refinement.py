import numpy as np

def _rho(f, delta_f):
    """
    Function to compute the bias correction term defined in equation 78 of ECMA 418-2 (2022).
    WARNING: the function defined in the standard is wrong, the corrected version is used here.
    
    Parameters:
    ----------
    center_freq: array of float
        band center frequencies in [Hz]     
    Returns:
    -------   
    _rho:float
        corrected bias term       
    """
    # Data from the standard
    E = np.array([0,0.0457,0.0907,0.1346,0.1765,0.2157,0.2515,0.2828,0.3084,0.3269,0.3364,0.3348,0.3188,0.2844,0.2259,0.1351,0.0000,-0.1351,
                  -0.2259,-0.2844,-0.3188,-0.3348,-0.3364,-0.3269,-0.3084,-0.2828,-0.2515,-0.2157,-0.1765,-0.1346,-0.0907, -0.0457,0.000,0.000])
    
    theta = np.arange(0,34)
    # Eq. 79
    B = (np.floor(f/delta_f)+theta/32)*delta_f-(f+E[theta])
    # Eq. 80
    theta_min = np.argmin(abs(B))
    # Eq. 81
    if (theta_min>0) and (B[theta_min]*B[theta_min-1]<0):
        theta_corr = theta_min
    else:
        theta_corr = theta_min + 1

    # Eq. 78 as published in the standard - WRONG !
    # _rho = (E[theta_corr]
    #         - ( (E[theta_corr] - E[theta_corr-1])*
    #         B[theta_corr-1] / (B[theta_corr] - B[theta_corr-1])))
    
    # Eq. 78 corrected
    
    _rho = (E[theta_corr]
            - ( (E[theta_corr] - E[theta_corr-1])*
            B[theta_corr] / (B[theta_corr] - B[theta_corr-1])))

    return _rho

def _refinement(kpi, Phi_E_l_z):
    """ Function to apply the refinement step 7.1.5.1 from ECMA 418-2 (2nd edition, 2022).
    This aims at reducing the impact of the von-hann-window on the quadratic fit of the spectrum.
     
    Parameters:
    -----------
    kpi: int
        modulation rate index
    Phi_E_l_z : numpy.array
        Noise-reduced power spectrum for one time step 'l'
        and one critical band 'z', dim(sbb)
    Returns:
    --------
    mod_rate: float
        Corrected modulation rate
    amp: float
        Corrected amplitude of the modulation rate peak    
        
    """

    # Refinement step
    if kpi == 0:
        amp = Phi_E_l_z[kpi] + Phi_E_l_z[kpi+1] 
    elif kpi == 255:
        amp = Phi_E_l_z[kpi-1] + Phi_E_l_z[kpi]
    else:
        amp = Phi_E_l_z[kpi-1] + Phi_E_l_z[kpi] + Phi_E_l_z[kpi+1] 

    # Analytical resolution of Eq.73 to get new expression for Eq.76
    delta_f = 1500/512
    F = (kpi - (Phi_E_l_z[kpi+1]-Phi_E_l_z[kpi-1])/(2*Phi_E_l_z[kpi-1]+2*Phi_E_l_z[kpi+1]-4*Phi_E_l_z[kpi])) * delta_f

    mod_rate = F + _rho(F, delta_f) 
    
    return mod_rate, amp



