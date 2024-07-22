import numpy as np
import matplotlib.pyplot as plt

from mosqito.sq_metrics.loudness.loudness_ecma._auditory_filters_centre_freq import _auditory_filters_centre_freq
from mosqito.sq_metrics.roughness.roughness_ecma._weighting import _f_max, _r_max, _Q2_high, _Q2_low,  _high_mod_rate_weighting, _low_mod_rate_weighting

from mosqito.utils.conversion.bark2freq import bark2freq
from mosqito.utils.conversion.freq2bark import freq2bark

# Set the default color cycle
from mosqito import COLORS as clr
import matplotlib as mpl
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=clr)

def freq2bark_(freq):
    """ Function to convert Hertz to the corresponding critical band 
    number z as defined in ECMA 418-2 (2nd edition, 2022)."""
    return 2*freq2bark(freq)

def bark2freq_(bark):
    """ Function to convert the critical band number z to its 
    central frequency in Hertz as defined in ECMA 418-2 (2nd edition, 2022)."""
    return bark2freq(bark/2)

def high_mod_rate_weighting_validation(fmod):
    """ Function to plot the weighting functions defined in sections 7.1.5.2
    and 7.1.5.4 of ECMA 418-2 (2nd edition, 2022)."""

    F_z = _auditory_filters_centre_freq()
    R_max = _r_max(F_z)
    F_max = _f_max(F_z)

    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    ax.plot(F_z, R_max, 'k')
    ax.set_xlabel('Center frequency [Hz]')
    ax.set_ylabel('Scaling factor '+r'$r_{max}$')
    ax.set_xscale('log')
    secax = ax.secondary_xaxis('top', functions=(freq2bark_, bark2freq_))
    secax.set_xlabel('Critical band number')
    secax.set_xticks(np.array([1,10,20,30,40]))    
    secax.set_xticklabels(np.array([1,10,20,30,40]))    
    plt.savefig('scaling_factor_rmax.png')
    plt.clf()

    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    ax.plot(F_z, F_max, 'k')
    ax.set_xlabel('Center frequency [Hz]')
    ax.set_ylabel(r'$f_{max}$')
    ax.set_xscale('log')
    secax = ax.secondary_xaxis('top', functions=(freq2bark_, bark2freq_))
    secax.set_xlabel('Critical band number')
    secax.set_xticks(np.array([1,10,20,30,40]))    
    secax.set_xticklabels(np.array([1,10,20,30,40]))    
    plt.savefig('maximum_modulation_rate_fmax.png')
    plt.clf()
    
    amp = 1
    q2_high = _Q2_high(F_z)

    G_high = np.empty((len(fmod), len(F_z)))
    w_high = np.empty((len(fmod), len(F_z)))
    for i, fm in enumerate(fmod):
        for j, fz in enumerate(F_z):   
            
            w_high[i,j] = _high_mod_rate_weighting(fm, amp, F_max[j], R_max[j], q2_high[j])
            
            G_high[i,j] = 1/((1+((fm/F_max[j]-F_max[j]/fm)*1.2822)**2)**q2_high[j])

    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    for i in range(len(fmod)):
        if fmod[i] == 70:
            ax.plot(F_z, G_high[i,:], 'k', label=f"{fmod[i]}"+" Hz")
        else:
            ax.plot(F_z, G_high[i,:], linestyle=':', label=f"{fmod[i]}"+" Hz")
            
    ax.legend(title='Modulation rate', loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_xlabel('Center frequency [Hz]')
    ax.set_ylabel('High modulation rates weighting function '+r'$G_{l,z}$')
    ax.set_xscale('log')

    secax = ax.secondary_xaxis('top', functions=(freq2bark_, bark2freq_))
    secax.set_xlabel('Critical band number')
    secax.set_xticks(np.array([1,10,20,30,40]))    
    secax.set_xticklabels(np.array([1,10,20,30,40]))    
    plt.tight_layout()
    plt.savefig('high_mod_rate_weighting_function_G.png')
    plt.clf()
    
    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    for i in range(len(fmod)):
        if fmod[i] == 70:
            ax.plot(F_z, w_high[i,:], 'k', label=f"{fmod[i]}"+" Hz")
        else:
            ax.plot(F_z, w_high[i,:], linestyle=':', label=f"{fmod[i]}"+" Hz")
    ax.legend(title='Modulation rate', loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_xlabel('Center frequency [Hz]')
    ax.set_ylabel('High modulation rates weighting')
    ax.set_xscale('log')
    secax = ax.secondary_xaxis('top', functions=(freq2bark_, bark2freq_))
    secax.set_xlabel('Critical band number')
    secax.set_xticks(np.array([1,10,20,30,40]))    
    secax.set_xticklabels(np.array([1,10,20,30,40]))    
    plt.tight_layout()
    plt.savefig('high_mod_rate_weighting.png')
    plt.clf()
    
def low_mod_rate_weighting_validation(fmod):
    """ Function to plot the weighting functions defined in sections 7.1.5.2
    and 7.1.5.4 of ECMA 418-2 (2nd edition, 2022)."""

    F_z = _auditory_filters_centre_freq()
    R_max = _r_max(F_z)
    F_max = _f_max(F_z)
    
    amp = 1
    q2_low = _Q2_low(F_z)

    G_low = np.empty((len(fmod), len(F_z)))
    w_low = np.empty((len(fmod), len(F_z)))
    for i, fm in enumerate(fmod):
        for j, fz in enumerate(F_z):   
            w_low[i,j] = _low_mod_rate_weighting(fm, amp, F_max[j], q2_low[j])
            G_low[i,j] = 1/((1+((fm/F_max[j]-F_max[j]/fm)*0.7066)**2)**q2_low[j]) 


    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    for i in range(len(fmod)):
        if fmod[i] == 70:
            ax.plot(F_z, G_low[i,:], 'k', label=f"{fmod[i]}"+" Hz")
        else:
            ax.plot(F_z, G_low[i,:], linestyle=':', label=f"{fmod[i]}"+" Hz")
    ax.legend(title='Modulation rate', loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_xlabel('Center frequency [Hz]')
    ax.set_ylabel('Low modulation rates weighting function '+r'$G_{l,z}$')
    ax.set_xscale('log')

    secax = ax.secondary_xaxis('top', functions=(freq2bark_, bark2freq_))
    secax.set_xlabel('Critical band number')
    secax.set_xticks(np.array([1,10,20,30,40]))    
    secax.set_xticklabels(np.array([1,10,20,30,40]))  
    plt.tight_layout()
    plt.savefig('low_mod_rate_weighting_function_G.png')
    plt.clf()
    
    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    for i in range(6):
        if fmod[i] == 70:
            ax.plot(F_z, w_low[i,:], 'k', label=f"{fmod[i]}"+" Hz")
        else:
            ax.plot(F_z, w_low[i,:], linestyle=':', label=f"{fmod[i]}"+" Hz")
    ax.plot(F_z, w_low[6,:], linestyle=':', label=r'$> 70$'+' Hz')
    ax.legend(title='Modulation rate', loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_xlabel('Center frequency [Hz]')
    ax.set_ylabel('Low modulation rates weighting')
    ax.set_xscale('log')
    secax = ax.secondary_xaxis('top', functions=(freq2bark_, bark2freq_))
    secax.set_xlabel('Critical band number')
    secax.set_xticks(np.array([1,10,20,30,40]))    
    secax.set_xticklabels(np.array([1,10,20,30,40]))    
    plt.tight_layout()
    plt.savefig('low_mod_rate_weighting.png')
    plt.clf()
   
if __name__ == "__main__":
    
    fmod_vector = np.array([20, 30, 40, 50, 60, 70, 80, 100,120,140,160,200,300])
    
    high_mod_rate_weighting_validation(fmod_vector)
    low_mod_rate_weighting_validation(fmod_vector)
