# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 14:25:04 2020

@author: wantysal
"""
import sys
sys.path.append('../../..')

# Standard library import
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap 

# Local imports
from mosqito.functions.tonality_tnr_pr.pr_main_calc import pr_main_calc


def comp_PR(is_stationary, signal, fs, plot='y'):
    """ Computation of prominence ratio according to ECMA-74, annex D.10 
    
    Parameters
    ----------
    is_stationary : boolean
        True if the signal is stationary    
    signal :numpy.array
        time signal values       
    fs : integer
        sampling frequency
    plot : str
        'y' to plot the results on a time / freq / tnr matrix, 'n' to only return the dict
    
    Output
    ------
    output = dict
    {    "name" : "tone-to-noise ratio",
         "time" : np.linspace(0, len(signal)/fs, num=nb_frame),
         "freqs" : <frequency of the tones>
         "values" : <PR calculated value for each tone>
         "prominence" : <True or False according to ECMA criteria>
         "global value" : <sum of the specific TNR values>       
            }
    
    
    """
        
    if is_stationary == True:
        tones_freqs, pr, prominence, total_pr = pr_main_calc(signal, fs)
        
        output = {
        "name" : "prominence ratio",
        "freqs" : tones_freqs,
        "values" : pr,
        "prominence" : prominence,
        "global value" : total_pr       
        }   
        
    if is_stationary == False:
        # Signal cut in frames of 200 ms along the time axis
        n = 0.5*fs
        nb_frame = math.floor(signal.size / n)
        time = np.linspace(0, len(signal)/fs, num=nb_frame)
        time = np.around(time,1)
        
        # Initialization of the result arrays
        tones_freqs = np.zeros((nb_frame), dtype = list)
        pr = np.zeros((nb_frame), dtype = list)
        prominence = np.zeros((nb_frame), dtype = list)
        total_pr = np.zeros((nb_frame))
        
        
        for i_frame in range(nb_frame):         
            segment = signal[int(i_frame*n):int(i_frame*n+n)]      
            tones_freqs[i_frame], pr[i_frame], prominence[i_frame], total_pr[i_frame] = pr_main_calc(segment, fs)
        
        output = {
            "name" : "prominence ratio",
            "time" : time,
            "freqs" : tones_freqs,
            "values" : pr,
            "prominence" : prominence,
            "global value" : total_pr       
        }  
        
        if plot == 'y':
            freq_axis = np.logspace(np.log10(90),np.log10(11200),num=1000)
            results = np.zeros((len(freq_axis),nb_frame))
            
            for t in range(nb_frame):
                for f in range(len(tones_freqs[t])):
                    ind = np.argmin(np.abs(freq_axis - tones_freqs[t][f]))            
                    results[ind, t] = pr[t][f]
                    
            cmap = np.load(r"C:\Users\pc\Documents\Salomé\eomys_cmp (1).npy")
            eomyscmp = ListedColormap(cmap)

            plt.pcolormesh(results, vmin=0, cmap = eomyscmp)
            plt.colorbar(label = "PR value in dB")
            plt.title("Prominence ratio along time and frequency", fontsize=14)
            
            plt.xlabel("Time [s]")
            plt.ylabel("Frequency [Hz]")
            
            # Frequency axis
            freq_labels = [90,200,500,1000,2000,5000,10000]
            freq_ticks = []
            for i in range(len(freq_labels)):
                freq_ticks.append(np.argmin(np.abs(freq_axis - freq_labels[i])))
            plt.yticks(freq_ticks, labels=[str(elem) for elem in freq_labels])
            
            # Time axis
            plt.xticks(np.arange(nb_frame), labels=[str(elem) for elem in time])

    
    return output























