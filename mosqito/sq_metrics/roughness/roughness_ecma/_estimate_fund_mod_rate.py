import numpy as np




def _estimate_fund_mod_rate(f_p, ):

    N_peak = len(f_p)
    amp = np.zeros(N_peak)
    f_p = np.zeros(N_peak)
    complex_energy = np.zeros((N_peak))
    harmonic_complex = np.zeros((N_peak), dtype=object)

    
    # Estimation of fundamental modulation rate (7.1.5.3) (ne dépend pas de l et z)
    for i0 in range(N_peak):
        f_p_temp = f_p[i0:]
        # integer ratios of all peaks' modulation rates to the current peak modulation rate
        R_i0 = round(f_p_temp/f_p[i0]) 

        # check for duplicates in R
        values, index, counts = np.unique(R_i0, return_index=True, return_counts=True)
        candidates_idx = index[counts==1]

        for c in values[counts>1]:
            ic = np.nonzero(R_i0 == c)[0]
            crit = np.abs( (f_p_temp[ic] / (R_i0[ic] * f_p[i0])) - 1)
            candidates_idx.append(ic[np.argmin(crit)])
         
        h_complex = np.abs(f_p_temp[candidates_idx]/(R_i0*f_p[i0])-1)
        I_i0 = h_complex[h_complex < 0.04]    
            
        
        harmonic_complex[i0] = np.where((abs(f_p_temp[candidates_idx]/(R_i0*f_p[i0])-1) < 0.04))[0]
        complex_energy[i0] = np.sum(amp[harmonic_complex[i0]])
        
    # The harmonic complex corresponding to the best fundamental modulation rate is the one with the highest sum
    i_max = np.argmax(complex_energy)
    h_complex_max = harmonic_complex[np.argmax(complex_energy)]
    w = 1 + 0.1 * abs(sum(f_p[h_complex_max]*amp[h_complex_max])/sum(amp[h_complex_max])-f_p[np.argmax(amp[h_complex_max])])**0.749
    amp_temp = amp[h_complex_max] * w
    
    
    

    return f_p_temp, fmax, amp_temp