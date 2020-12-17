# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:51:19 2020

@author: wantysal
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft
# from scipy.signal import welch, periodogram


# Local functions imports
from mosqito.functions.shared.conversion import amp2db, db2amp
from mosqito.functions.tonality.LTH import LTH
from mosqito.functions.tonality.critical_band import critical_band
from mosqito.functions.noctfilter.n_oct_filter import getFrequencies

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

def comp_TNR(signal, fs):
    """ Computation of tone-to-noise ration according to ECMA-74, annex D.9 """
        
    n = len(signal)    
    window = np.hanning(n)
    window = window / np.mean(window)
    
    # Creation of the spectrum by FFT
    spectrum = fft(signal * window) 
    spectrum[0] *= 0.5
    spectrum =  2 * spectrum / (n *2**0.5 )
    
    # Conversion into dB level
    module = np.abs(spectrum)
    spectrum_db = amp2db(module, ref = 0.00002)
        
    # Frequency axis of interest
    freq_axis = np.arange(0,int(n/2),1) * (fs/n)    
    index = np.where((freq_axis > 89.1) & (freq_axis < 11200))[0]
    freqs = freq_axis[index]
    spec_db = spectrum_db[index]
    
    plt.plot(freqs,spec_db)
    
    # 1/24 octave bands filter
    filter_freqs = getFrequencies(90, 11200, 24, G=10, fr=1000)['f']  
    
    # Smoothed spectrum
    smoothed_spectrum = np.zeros((filter_freqs.shape[0]))    
    for i in range(filter_freqs.shape[0]):
        bin_index = np.where((freqs >= filter_freqs[i,0]) & (freqs <= filter_freqs[i,2]))[0]
        spec_sum = 0
        for j in bin_index:
            spec_sum += 10**(spec_db[j]/20)
        smoothed_spectrum[i] = 20*np.log10(spec_sum / len(bin_index))
        
    plt.plot(filter_freqs[:,1], smoothed_spectrum ) 
    

    # Correspondance between the 2 spectra
    filter_freqs[167,2] = 11200
    filter_freqs[0,0] = 89.1
    cor  = []
    low = []
    high = []
    for i in range(len(filter_freqs)):
        cor.append(np.argmin(np.abs(freqs - filter_freqs[i,1])))
        low.append(np.argmin(np.abs(freqs - filter_freqs[i,0])))
        high.append(np.argmin(np.abs(freqs - filter_freqs[i,2])))
    
    smooth_spec = np.zeros((spec_db.shape))
    for i in range(filter_freqs.shape[0]):
        smooth_spec[low[i]:high[i]] = smoothed_spectrum[i]
    plt.plot(freqs, smooth_spec + 6)
    
    
#### Screening test to find the discrete tones##########################################
    # Criteria 1 : the level of the spectral line exceeds the corresponding lines 
    # of the smoothed spectrum by at least 6 dB
    indexx = np.where(spec_db > smooth_spec + 6)[0]
    plt.plot(freqs[indexx], spec_db[indexx], "s")

    # Criteria 2 : the level of the spectral line is higher than the level of 
    # the two neighboring lines
    maxima = (np.diff(np.sign(np.diff(spec_db[indexx]))) < 0).nonzero()[0] + 1 # local max 
    plt.plot(freqs[indexx][maxima], spec_db[indexx][maxima], "o")

    
    # Criteria 3 : the level of the spectral line exceeds the threshold of hearing
    threshold = LTH(freqs)
    plt.plot(freqs, threshold + 10)
    audible = np.where(spec_db[indexx][maxima] > threshold[indexx][maxima] + 10)[0]
    plt.plot(freqs[indexx][maxima][audible], spec_db[indexx][maxima][audible], "x")
    
    index = np.arange(0,len(spec_db))[indexx][maxima][audible]
        
    nb_tones = len(audible)
    tnr = []

####Evaluation of each candidate###############################################
    for t in range(nb_tones):
        ind = index[t]
        f = freqs[ind]
        
        # critical band centered on f
        f1, f2 = critical_band(f)
        low_limit_idx = np.argmin(np.abs(freqs - f1))
        high_limit_idx = np.argmin(np.abs(freqs - f2))
        nb_idx = high_limit_idx - low_limit_idx + 1
    
        # Other tones in the critical band centered on f tones       
        multiple_idx = index[index>low_limit_idx]
        multiple_idx = multiple_idx[multiple_idx<high_limit_idx]
    
        if len(multiple_idx) > 1:
            multiple_idx, ind_p = screening(multiple_idx, ind)  
                       
            if len(multiple_idx) > 1:
                fp = freqs[ind_p]
                sort_spec = np.argsort(-1 * spec_db[multiple_idx])
                ind_s = multiple_idx[sort_spec[1]]
                fs = freqs[ind_s]
                    
                # proximity criterion
                delta_f = 21 * 10 ** (1.2 * (np.abs(fp / 212)) ** 1.8)
                if np.abs(fs - fp) < delta_f:
                    # tone SPL
                    Lt = 10 * np.log10(( (10 ** (spec_db[ind_p]/10) + 10 ** (spec_db[ind_s]/10))))
                    
                    # total SPL in the critical band
                    spec_sum = 0
                    for i in np.arange(low_limit_idx, high_limit_idx+1):
                        spec_sum += 10 ** (spec_db[i] / 10)
                    spec_sum -= 10 ** (spec_db[ind_s]/10)
                    Ltot = 10 * np.log10((spec_sum))
        
                    delta_ft = 2 * (freq_axis[1] - freq_axis[0])
                    f = fp
                    ind = ind_p
            else:
                 ind = ind_p
                
        else:
            
            # tone SPL
            Lt = spec_db[ind]
            
            # total SPL in the critical band
            spec_sum = 0
            for i in np.arange(low_limit_idx, high_limit_idx+1):
                spec_sum += 10 ** (spec_db[i] / 10) 
            Ltot = 10 * np.log10((spec_sum))
        
            delta_ft = freqs[1] - freqs[0]
    
    
        # SPL of the masking noise
        delta_fc = f2 - f1
        delta_ftot = freq_axis[high_limit_idx] - freq_axis[low_limit_idx]
        Ln = 10 * np.log10(10 ** (Ltot/10) - 10 ** (Lt/10)) + 10 * np.log10( delta_fc / (delta_ftot - delta_ft))

        
    # Tone-to-noise ratio
    tnr.append([ind,f,Lt - Ln])
        
    # Prominence criteria
    for i in range(len(tnr)):
        if tnr[i][1] >= 89.1 and tnr[i][1] < 1000:
            if tnr[i][2] >= 8 + 8.33 * np.log10(1000/tnr[i][1]):
                print('Prominent tone at ' + str(tnr[i][1]) + ' Hz')
        elif tnr[i][1] > 1000 and tnr[i][1] < 11200:
            if tnr[i][2] >= 8 :
                print('Prominent tone at ' + str(tnr[i][1]) + ' Hz')
                
    return tnr

signal, fs = load(True, file, 2*2**0.5)
comp_TNR(signal, fs)