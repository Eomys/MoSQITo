import numpy as np
from scipy.signal import find_peaks, peak_prominences

from mosqito.sq_metrics.roughness.roughness_ecma._refinement import _refinement

def _peak_picking(Phi_E):
    """Function to find the maxima of the average scaled power spectra, 
    according to section 7.1.5.1 of ECMA 418-2.

    Arguments:
    ----------
    Phi_E : numpy.array
        1D average scaled power spectra at defined index [l,z]

    Returns:
    --------
    f_p: 
    
    A: _description_
    """
    
    # Peak picking
    maxima_idx, maxima_dict = find_peaks(Phi_E[2:], prominence=[None, None])
    maxima_idx += 2
    prominence = maxima_dict['prominences']
                
    if len(maxima_idx) == 0:
        f_p = np.array([])
        A = np.array([])
    else: 
        # Compute peaks prominence
        
        # Only the 10 maxima with the highest prominence are considered
        if len(maxima_idx) > 10:
            sort_idx = np.argsort(prominence)
            prominence = prominence[sort_idx[-10:]]
            prominence_idx = maxima_idx[sort_idx[-10:]]
        else:
            prominence_idx = maxima_idx
            
        # Eq 72
        condition_not_met_idx = np.where((Phi_E[maxima_idx]) <= 0.05*max(Phi_E[maxima_idx]))[0]
        maxima_idx = np.delete(maxima_idx, condition_not_met_idx)
        prominence_idx = np.delete(prominence_idx, condition_not_met_idx)
        prominence = np.delete(prominence, condition_not_met_idx)
            
            
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
            f_p[i], A[i] = _refinement(kpi, Phi_E)
            
    # plt.figure()
    # freqs = linspace(0, 1500//2, 256)

    # plt.plot(freqs, Phi_E[l, z, :])
    # plt.plot(freqs[maxima_idx], Phi_E[l, z, maxima_idx], 'o')
    # plt.plot(freqs[maxima_idx], prominence)
    # plt.show(block=True)

 
    return f_p, A