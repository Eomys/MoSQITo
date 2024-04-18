import numpy as np
from scipy.signal import find_peaks

from mosqito.sq_metrics.roughness.roughness_ecma._refinement import _refinement

def _peak_picking(Phi_E_l_z):
    """
    Function to find the maxima of the average scaled power spectra, 
    according to section 7.1.5.1 of ECMA 418-2 (2nd Ed, 2022) 
    standard for calculating roughness.
    
    This function takes an array of noise-reduced, downsampled power spectrum
    values for one time step 'l' and one critical frequency 'z', finds
    'N_peaks' maxima that fulfill certain conditons, and estimates the
    frequencies and amplitudes of these maxima.
    
    Parameters
    ----------
    Phi_E_l_z : numpy.array
        Noise-reduced power spectrum for one time step 'l'
        and one critical band 'z', dim(sbb)
        
    Returns
    -------
    f_p : numpy.array
        Estimated modulation frequencies for all maxima in 'Phi_E_l_z'
    
    A : numpy.array
        Estimated amplitudes for all maxima in 'Phi_E_l_z'
    """

    # Find peaks index and prominence
    maxima_idx, maxima_dict = find_peaks(Phi_E_l_z[2:], prominence=[None, None])
    
    
    # Compensate for k_range starting at k=2
    maxima_idx += 2
    prominence = maxima_dict['prominences']
        
    if len(maxima_idx) == 0:
        f_p = np.array([])
        A = np.array([])
    else: 
        # Apply condition on the amplitude (Eq. 72)
        condition_not_met_idx = np.where((Phi_E_l_z[maxima_idx]) <= 0.05*max(Phi_E_l_z[maxima_idx]))[0]
        maxima_idx = np.delete(maxima_idx, condition_not_met_idx)
        prominence = np.delete(prominence, condition_not_met_idx)
        
        # Only the 10 maxima with the highest prominence are considered
        if len(maxima_idx) > 10:
            sort_idx = np.argsort(prominence)
            prominence = prominence[sort_idx[-10:]]
            prominence_idx = maxima_idx[sort_idx[-10:]]
        else:
            prominence_idx = maxima_idx      
            
    N_peak = len(prominence)
    if N_peak == 0:
        f_p = np.array([])
        A = np.array([])
    else:
        f_p = np.empty(N_peak)
        A = np.empty(N_peak)
                        
        # Modulation rate and maxima's amplitudes
        for i, kpi in enumerate(prominence_idx):
            # Refinement step
            f_p[i], A[i] = _refinement(kpi, Phi_E_l_z)
             
    return f_p, A