import numpy as np
from error_correction import E


def rho(f, delta_f):
    theta = np.arange(0,34)
    B = (np.floor(f/delta_f)+theta/32)*delta_f-(f+E[theta])
    theta_min = np.argmin(B)

    if (theta_min>0) and (B[theta_min]*B[theta_min-1]<0):
        theta_corr = theta_min
    else:
        theta_corr = theta_min + 1

    rho = E[theta_corr]-(E[theta_corr]-E[theta_corr-1])*B[theta_corr-1]/(B[theta_corr]-B[theta_corr-1])

    return rho

def r_max(center_freq):

    if center_freq<1000:
        r1 = 0.3560
        r2 = 0.8049
    else:
        r1 = 0.8024
        r2 = 0.9333

    r = 1/(1+r1*abs(np.log2(center_freq/1000))**r2)

    return r

def Q2_high(center_freq):
    if center_freq/1000 < 2**-3.4253 :
        q2 = 0.2471
    else:
        q2 = 0.2471+0.0129*(np.log2(center_freq/1000)+3.4253)**2
    
    return q2

def Q2_low(center_freq):
    return 1.0967-0.0640*np.log2(center_freq/1000)

