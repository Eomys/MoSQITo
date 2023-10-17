import numpy as np

def f_max(center_freq):
    return 72.6937*(1-1.1739*np.exp(-5.4583*center_freq/1000))

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

def _high_mod_rate_weighting(mod_rate, amp, fmax, rmax, q2_high):
    """
    """
    if mod_rate<fmax:
        weighted_amp = amp * rmax
    else:
        G = 1/((1+((mod_rate/fmax-fmax/mod_rate)*1.2822)**2)**q2_high)
        weighted_amp = G * amp * rmax

    return weighted_amp

def _low_mod_rate_weighting(mod_rate, amp, fmax, q2_low):

    if mod_rate < fmax:
        G = 1/((1+((mod_rate/fmax-fmax/mod_rate)*0.7066)**2)**q2_low)
        weighted_amp = sum(G * amp)
    else:
        weighted_amp = sum(amp)

    return weighted_amp