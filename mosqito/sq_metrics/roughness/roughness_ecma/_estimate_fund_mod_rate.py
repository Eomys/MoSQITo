import numpy as np




def _estimate_fund_mod_rate(f_p, Ai_tilde):
    """_summary_

    Args:
        f_p (_type_): Estimated modulation rates of maxima
        Ai_tilde (_type_): Weighted Ai_tildelitudes of maxima

    Returns:
        _type_: _description_
    """

    N_peak = len(f_p)
    I_i0 = np.empty((N_peak), dtype=object)
    E_i0 = np.empty((N_peak))
    
    # Estimation of fundamental modulation rate (7.1.5.3) (ne dépend pas de l et z)
    for i0 in range(N_peak):
        f_p_temp = f_p #[i0:]
        # integer ratios of all peaks' modulation rates to the current peak modulation rate
        R_i0 = np.round(f_p_temp/f_p[i0]) 

        # check for duplicates in R
        values, index, counts = np.unique(R_i0, return_index=True, return_counts=True)
        candidates_idx = index[counts==1]

        for c in values[counts>1]:
            ic = np.nonzero(R_i0 == c)[0]
            crit = np.abs( (f_p_temp[ic] / (R_i0[ic] * f_p[i0])) - 1)
            candidates_idx = np.append(candidates_idx, ic[np.argmin(crit)])
         
        h_complex = np.abs(f_p_temp[candidates_idx]/(R_i0[candidates_idx]*f_p[i0]+10e-10)-1)
        I_i0[i0] = candidates_idx[h_complex < 0.04]    
        
        E_i0[i0] = np.sum(Ai_tilde[I_i0[i0]])
        
        
    # The harmonic complex corresponding to the best fundamental modulation rate is the one with the highest sum
    i_max = np.argmax(E_i0)
    I_max = I_i0[i_max]
    mod_rate = f_p[i_max]
    
    i_peak = np.argmax(Ai_tilde[I_max])
        
    w_peak = 1 + 0.1 * abs(sum(f_p[I_max]*Ai_tilde[I_max])/sum(Ai_tilde[I_max])-f_p[i_peak])**0.749
    A_hat = Ai_tilde[I_max] * w_peak    
    
    return mod_rate, A_hat