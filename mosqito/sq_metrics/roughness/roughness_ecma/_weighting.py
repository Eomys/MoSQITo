import numpy as np

def _f_max(center_freq):
    """
    Function to compute the modulation rate at which the weighting factor G reaches the maximum 
    of one for all band center frequencies according to equation 86 of ECMA 418-2 (2nd edition, 2022)
    
    Parameters
    ----------
    center_freq: array of float
        band center frequencies in [Hz]        
    """
    return 72.6937*(1-1.1739*np.exp(-5.4583*center_freq/1000))

def _r_max(center_freq):
    """
    Function to compute the scaling factor for all band center frequencies
    according to equation 84 of ECMA 418-2 (2nd edition, 2022)
    
    Parameters
    ----------
    center_freq: array of float
        band center frequencies in [Hz]        
    """
    r1 = np.zeros((len(center_freq)))
    r2 = np.zeros((len(center_freq)))

    r1[center_freq<1000] = 0.3560
    r2[center_freq<1000] = 0.8049

    r1[center_freq>=1000] = 0.8024
    r2[center_freq>=1000] = 0.9333

    r = 1/(1+r1*abs(np.log2(center_freq/1000))**r2)

    return r

def _Q2_high(center_freq):
    """ Function to compute high modulation rate weighting parameter according to equation 87 of ECMA 418-2 (2nd edition, 2022)

    Parameters
    ----------
    center_freq: float
        center frequency of the current band z in [Hz]

    Returns
    -------
    q2: float
        q2 parameter for high modulation rates
    """
    q2 = np.zeros((len(center_freq)))
    q2[center_freq/1000 < 2**(-3.4253)] = 0.2471
    q2[center_freq/1000 >= (2**-3.4253)] = 0.2471+0.0129*(np.log2(center_freq[center_freq/1000 >= 2**-3.4253]/1000)+3.4253)**2

    return q2

def _Q2_low(center_freq):
    """ Function to compute low modulation rate weighting parameter according to equation 96 of ECMA 418-2 (2nd edition, 2022)

    Parameters
    ----------
    center_freq: float
        center frequency of the current band z in [Hz]

    Returns
    -------
    q2: float
        q2 parameter for low modulation rates
    """
    return 1.0967-0.0640*np.log2(center_freq/1000)

def _high_mod_rate_weighting(mod_rate, amp, fmax, rmax, q2_high):
    """
    Function to weight high modulation rates according to equation 83 of ECMA 418-2 (2nd edition, 2022)
    
    Parameters
    ----------
    mod_rate : float
        estimated modulation rate [Hz]
    amp : float
        amplitude of the envelope spectrum at the estimated modulation rate
    fmax : float
        modulation rate at which the weighting factor G reaches the maximum of one for the current band z
    rmax : float
        scaling factor for the current band z
    q2_high : float
        parameter for the weighting function calculation at the current band z
        
    Returns
    -------
    weighted_amp : float
        the weighted amplitude
    
    """
    if mod_rate<fmax:
        weighted_amp = amp * rmax
    else:
        G = 1/((1+((mod_rate/fmax-fmax/mod_rate)*1.2822)**2)**q2_high)
        weighted_amp = G * amp * rmax
        
    return weighted_amp

def _low_mod_rate_weighting(mod_rate, amp, fmax, q2_low):
    """
    Function to weight low modulation rates according to equation 95 of ECMA 418-2 (2nd edition, 2022)
    
    Parameters
    ----------
    mod_rate : float
        estimated modulation rate [Hz]
    amp : float
        amplitude of the envelope spectrum at the estimated modulation rate
    fmax : float
        modulation rate at which the weighting factor G reaches the maximum of one for the current band z
    q2_low : float
        parameter for the weighting function calculation at the current band z
        
    Returns
    -------
    weighted_amp : float
        the weighted amplitude
    
    """
    if mod_rate < fmax:
        G = 1/((1+((mod_rate/fmax-fmax/mod_rate)*0.7066)**2)**q2_low)        
        weighted_amp = sum(G * amp)
    else:
        weighted_amp = sum(amp)

    return weighted_amp
            

