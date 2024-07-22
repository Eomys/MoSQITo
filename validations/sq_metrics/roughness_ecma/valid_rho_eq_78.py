import numpy as np
import matplotlib.pyplot as plt

# Set the default color cycle
from mosqito import COLORS as clr
import matplotlib as mpl
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=clr)

def valid_rho(f, delta_f):
    """
    Function to explain the bias term rho's correction.
    
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

    rho_wrong = (E[theta_corr]
            - ( (E[theta_corr] - E[theta_corr-1])*
            B[theta_corr-1] / (B[theta_corr] - B[theta_corr-1])))
    
    rho = (E[theta_corr]
            - ( (E[theta_corr] - E[theta_corr-1])*
            B[theta_corr] / (B[theta_corr] - B[theta_corr-1])))
    
    
    # This entire approach (Eqs. 78 to 81) is identical to
    # using linear interpolation with Numpy:
    rho_np = np.interp(0, B, E)
    
    plt.figure(figsize=[5.76, 4.8]) 
    plt.plot(B, E, '^:', markersize=8, label='Table 10, Eq. 79')
    plt.plot(0, rho_np, 'o', markersize=9, label='np.interp')
    plt.plot(0, rho_wrong, 's', markersize=8, label='Eq. 78 (as published)')
    plt.plot(0, rho, 'P', markersize=6, label='Eq. 78 (corrected)')
    plt.grid()
    plt.xlabel(r'$\beta(\theta)$', fontsize=14)
    plt.ylabel(r'E($\theta$)', fontsize=14)
    plt.legend()
    plt.xlim([-0.5, 0.2])
    plt.ylim([-0.35, 0.])
    plt.tight_layout()
    plt.savefig('rho_bias_term_equation_78_correction.png')
    
if __name__ == "__main__":

    valid_rho(70, 2.9297)