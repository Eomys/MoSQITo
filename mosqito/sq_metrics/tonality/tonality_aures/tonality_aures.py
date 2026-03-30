# -*- coding: utf-8 -*-

import numpy as np
from scipy.signal import welch
from mosqito.sq_metrics.loudness import loudness_zwst_freq

def tonality_aures(signal, fs):
    """
    Compute the tonality value from a time signal according to Aures' model.
    The implementation is based on the documentation provided by the user.

    Parameters
    ----------
    signal : array_like
        Input time signal in [Pa].
    fs : float
        Sampling frequency in [Hz].
        
    Returns
    -------
    K : float
        Tonality value in [t.u.].
    """
    
    # TODO: The provided implementation is a basic translation of the provided 
    # documentation and may not be fully functionnal. It needs to be completed
    # and validated against a reference implementation.

    # 1. Signal preprocessing and spectrum analysis
    # The user's documentation suggests 0.2s blocks and a Blackman window.
    nperseg = 4096
    freqs, Pxx = welch(signal, fs, window='blackmanharris', nperseg=nperseg, scaling='density')
    
    # Convert PSD to amplitude spectrum
    amp_spec = np.sqrt(Pxx * (freqs[1]-freqs[0])) * np.sqrt(2)
    
    # Convert amplitude to dB SPL
    L = 20 * np.log10(amp_spec / 2e-5)
    
    # 2. Identification of tonal components
    tones = _find_tonal_components(L, freqs)
    
    # 3. Refine tonal components and calculate excess level
    refined_tones = []
    for (i, f_c_temp) in tones:
        # 3.1 3dB bandwidth and precise center frequency
        f_c, delta_z = _center_freq_3dB(i, L, freqs)
        
        # 3.2 Excess Level calculation
        delta_L = _excess_level(i, L, freqs, tones)
        
        if delta_L > 0:
            refined_tones.append((f_c, delta_z, delta_L))
            
    # 4. Weighting functions
    w_T_sum_sq = 0
    for (f_c, delta_z, delta_L) in refined_tones:
        w1 = 0.13 / (delta_z + 0.13)
        w2 = (1 / np.sqrt(1 + 0.2 * (f_c / 700 + 700 / f_c)**2))**0.29
        w3 = (1 - np.exp(-delta_L / 15))**0.29
        
        w1_p = w1**(1 / 0.29)
        w2_p = w2**(1 / 0.29)
        w3_p = w3**(1 / 0.29)
        
        w_T_sum_sq += (w1_p * w2_p * w3_p)**2
        
    w_T = np.sqrt(w_T_sum_sq)
    
    # 5. Loudness weighting factor
    freqs_loudness, Pxx_loudness = welch(signal, fs, window='hann', nperseg=4096, noverlap=2048, scaling='density')
    amp_spec_loudness = np.sqrt(Pxx_loudness * (freqs_loudness[1]-freqs_loudness[0])) * np.sqrt(2)

    N_total, N_specific, _ = loudness_zwst_freq(amp_spec_loudness, freqs_loudness)
    
    # Create a spectrum without tonal components
    amp_spec_no_tones = np.copy(amp_spec_loudness)
    # Find tone indices in the loudness spectrum
    for (i, f_c) in tones:
        # Find the closest index in the loudness frequency axis
        idx = (np.abs(freqs_loudness - f_c)).argmin()
        # Remove the 7 spectral lines around the tone - this is an approximation
        freq_res = freqs[1] - freqs[0]
        lines_to_remove = int(3 * (freqs_loudness[1]-freqs_loudness[0]) / freq_res)
        amp_spec_no_tones[max(0, idx-lines_to_remove):min(len(amp_spec_loudness), idx+lines_to_remove+1)] = 0
    
    N_gr, _, _ = loudness_zwst_freq(amp_spec_no_tones, freqs_loudness)

    if N_total > 0:
        w_Gr = 1 - N_gr / N_total
    else:
        w_Gr = 0
    
    # 6. Final tonality calculation
    c = 1.09
    K = c * (w_T**0.29) * (w_Gr**0.79)
    
    return K

def _bark(f):
    """Convert frequency from Hz to Bark."""
    return 13 * np.arctan(0.76 * f / 1000) + 3.5 * np.arctan((f / 7500)**2)

def _find_tonal_components(L, freqs):
    """Find tonal components in the spectrum."""
    tones = []
    for i in range(3, len(L) - 3):
        is_peak = L[i] > L[i-1] and L[i] > L[i+1]
        if is_peak:
            is_prominent = all(L[i] - L[i+m] >= 7 for m in [-3, -2, 2, 3])
            if is_prominent:
                f_c_temp = freqs[i] + 0.46 * (L[i+1] - L[i-1])
                tones.append((i, f_c_temp))
    return tones

def _center_freq_3dB(i, L, freqs):
    """Calculate center frequency and bandwidth using 3dB method."""
    L_peak = L[i]
    
    # Find lower 3dB point
    j = i
    while j > 0 and L_peak - L[j] < 3:
        j -= 1
    # TODO: Interpolate to find exact frequency
    f_l = freqs[j]
    
    # Find upper 3dB point
    k = i
    while k < len(L) - 1 and L_peak - L[k] < 3:
        k += 1
    # TODO: Interpolate to find exact frequency
    f_u = freqs[k]
    
    f_c = np.sqrt(f_l * f_u)
    delta_z = _bark(f_u) - _bark(f_l)
    
    return f_c, delta_z

def _excess_level(i, L, freqs, tones):
    """Calculate the excess level of a tonal component."""
    
    f_i = freqs[i]
    L_i = L[i]
    
    # Masking from other tonal components
    masking_tones = 0
    for k_idx, (k, f_c_k) in enumerate(tones):
        if k != i:
            L_k = L[k]
            z_i = _bark(f_i)
            z_k = _bark(f_c_k)
            
            if f_i <= f_c_k:
                s = 27
            else:
                s = -24 - (230 / (f_c_k + 0.2 * L_k))
                
            L_ek = L_k - s * (z_k - z_i)
            A_ek = 10**(L_ek / 20)
            masking_tones += A_ek
            
    # Masking from noise (not implemented, needs critical band analysis)
    E_gr = 0
    
    # Hearing threshold
    E_hs = 3.64 * (f_i/1000)**-0.8 - 6.5 * np.exp(-0.6 * (f_i/1000 - 3.3)**2) + 1e-3 * (f_i/1000)**4
    
    delta_L = L_i - 10 * np.log10(masking_tones**2 + E_gr + E_hs)
    
    return delta_L
