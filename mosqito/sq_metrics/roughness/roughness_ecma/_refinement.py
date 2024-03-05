from numpy import array, dot, arange, floor, argmin, mean
from numpy.linalg import inv

def _rho(f, delta_f):

    E = array([0,0.0457,0.0907,0.1346,0.1765,0.2157,0.2515,0.2828,0.3084,0.3269,0.3364,0.3348,0.3188,0.2844,0.2259,0.1351,0.0000,-0.1351,
                  -0.2259,-0.2844,-0.3188,-0.3348,-0.3364,-0.3269,-0.3084,-0.2828,-0.2515,-0.2157,-0.1765,-0.1346,-0.0907, -0.0457,0.000,0.000])
    theta = arange(0,34)
    B = (floor(f/delta_f)+theta/32)*delta_f-(f+E[theta])
    theta_min = argmin(B)

    if (theta_min>0) and (B[theta_min]*B[theta_min-1]<0):
        theta_corr = theta_min
    else:
        theta_corr = theta_min + 1

    _rho = E[theta_corr]-(E[theta_corr]-E[theta_corr-1])*B[theta_corr-1]/(B[theta_corr]-B[theta_corr-1])

    return _rho

def _refinement(kpi, Phi_E):
    """ Function to apply the refinement step 7.1.5.1 to the input peak
     
    kpi: modulation rate index
    Phi_E: Phi_E[l,z,:]
        
    """

    # Refinement step
    #Km = array([[kpi**2, kpi-1, 1],[kpi**2, kpi, 1],[(kpi+1)**2, kpi+1, 1]])
    if kpi == 0:
        #Phi = array([0, Phi_E[kpi], Phi_E[kpi+1]])
        amp = Phi_E[kpi] + Phi_E[kpi+1] 
    elif kpi == 255:
        #Phi = array([Phi_E[kpi-1], Phi_E[kpi], 0])
        amp = Phi_E[kpi-1] + Phi_E[kpi]
    else:
        #Phi = array([Phi_E[kpi-1], Phi_E[kpi], Phi_E[kpi+1]])
        amp = Phi_E[kpi-1] + Phi_E[kpi] + Phi_E[kpi+1] 

    # C = dot(inv(Km), Phi)
    # F = -C[1]/(2*C[0])*delta_f
    # mod_rate = F + _rho(F, delta_f) # modulation rate
    

    c0 = 1/2*(Phi_E[kpi+1] + Phi_E[kpi-1] - 2*Phi_E[kpi])
    c1 = Phi_E[kpi] - Phi_E[kpi-1] - (2*kpi-1) * c0
    
    delta_f = 1500/512
    F = -c1/(2*c0)*delta_f
    
    f_p = F + _rho(F, delta_f) # modulation rate
    mod_rate = F + _rho(F, delta_f) # modulation rate
    #mod_rate = mean([F , kpi * delta_f])
    #mod_rate = kpi * delta_f
    
    return f_p, amp