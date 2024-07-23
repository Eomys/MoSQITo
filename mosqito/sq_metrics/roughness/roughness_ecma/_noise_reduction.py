import numpy as np
import matplotlib.pyplot as plt


def _noise_reduction(spectrum):
    """ Noise reduction
    
    Function to apply a noise reduction weighting on the envelopes scaled power spectra,
    according to section 7.1.4 of ECMA 418-2 (2nd edition 2022).

    Parameter:
    ----------
    spectrum : array
        Scaled power spectra of the envelopes, dim(Ntime, Nbark, sbb)

    Returns:
    --------
    Phi_E : array
        Weighted power spectra.
    """

    L, _, K = spectrum.shape
    
    # Averaging with neighbouring bands
    spectrum_average = np.empty((spectrum.shape))
    spectrum_average[:,0] = (spectrum[:,0] + spectrum[:,1])/2
    spectrum_average[:,-1] = (spectrum[:,-1] + spectrum[:,-2])/2
    spectrum_average[:,1:-1] = (spectrum[:,:-2] + spectrum[:,1:-1] + spectrum[:,2:])/3
    
    # Sum and median of the scaler power spectra
    s = np.sum(spectrum_average, axis=1)
    s_tilde = np.median(s[:,2:], axis=1)
    
    # Weighting function definition
    noise_suppression_weighting = np.zeros((L,K))
    
    w_tilde = 0.0856 * (s/(s_tilde[:,np.newaxis]+10e-10)) * np.clip(0.1891*np.exp(0.0120*np.arange(K)),0,1)
    w_tilde_max = np.max( w_tilde[:, 2:], axis=-1)
    idx = np.where((w_tilde>=0.05 * w_tilde_max[:, np.newaxis]))
    
    noise_suppression_weighting[idx] = np.clip(w_tilde[idx]-0.1407,0,1)
    
    # Weighting aplication
    Phi_E = spectrum_average * noise_suppression_weighting[:,None,:]
    
    return Phi_E
