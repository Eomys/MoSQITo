# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 20:23:01 2020

@author: Salomé
"""
   
        
def screening(multiple_idx, ind):
    f = freqs[ind]       
    sort_spec = np.argsort(-1 * spec_db[multiple_idx])
    
    # highest tone in the crtical band
    ind_p = multiple_idx[sort_spec[0]]
    fp = freqs[ind_p]
    # suppression of the lower values
    sup = np.where(index == multiple_idx[sort_spec[2:]])[0]
    np.delete(index, sup)
    
    if fp != f:
        # critical band centered on fp
        f1, f2 = critical_band(fp)
        low_limit_idx = np.argmin(np.abs(freqs - f1))
        high_limit_idx = np.argmin(np.abs(freqs - f2))
        nb_idx = high_limit_idx - low_limit_idx + 1
    
        # Other tones in the critical band centered on f tones       
        multiple_idx = index[index>low_limit_idx]
        multiple_idx = multiple_idx[multiple_idx<high_limit_idx]
    
        if len(multiple_idx) > 1:
            multiple_idx, ind_p= screening(multiple_idx, ind_p)    
                       
    return (multiple_idx, ind_p)
        
