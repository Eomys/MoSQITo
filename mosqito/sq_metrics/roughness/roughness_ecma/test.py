from numpy import(
    abs,
    append,
    power,
    zeros,
    empty,
    sum,
    array,
    clip,
    exp,
    median,
    where,
    argmax,
    argmin,
    argsort,
    delete,
    exp,
    dot,
    round,
    squeeze,
    ceil,
    sqrt,
    tanh,
    sign,
    diff,
    concatenate,
    dot,
    int32,

)
from numpy.fft import fft
from numpy.linalg import inv
from scipy.signal import (hilbert, resample, find_peaks)
from scipy.signal.windows import hann


# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._rectified_band_pass_signals import _rectified_band_pass_signals
from mosqito.sq_metrics.loudness.loudness_ecma._auditory_filters_centre_freq import _auditory_filters_centre_freq

# Data import
# Threshold in quiet
from mosqito.sq_metrics import loudness_ecma

from mosqito.utils import load

from _weighting import rho, f_max, r_max, Q2_high, Q2_low, _high_mod_rate_weighting, _low_mod_rate_weighting
from _comp_prominence import _comp_prominence


def roughness_ecma(signal):
    """Calculation of the roughness according to ECMA-418-2 section 7

    Parameters
    ----------
    signal: numpy.array
        time signal values in 'Pa'. The sampling frequency of the signal must be 48000 Hz.

    Returns
    -------
    n_specific: list of numpy.array
        Specific Loudness [sone_HMS per Bark]. Each of the 53 element of the list corresponds to the time-dependant
        specific loudness for a given bark band. Can be a ragged array if a different sb/sh are used for each band.
    bark_axis: numpy.array
        Bark axis
    """
    # Sampling frequency
    fs = 48000
    N_samples = len(signal)
    duration = N_samples / fs
    CBF = 53
    center_freq = _auditory_filters_centre_freq()

    # Hop size and block size for specific loudness calculation (7.1.1)
    sb=16384
    sh=4096
    N_specific, bark_axis = loudness_ecma(signal, sb, sh)
    N_specific = array(N_specific)
    # ! ces valeurs sont déjà calculées dans la loudness
    block_array_rect = array(_rectified_band_pass_signals(signal, sb, sh))
    L = block_array_rect.shape[1]
    # ENVELOPPE CALCULATION AND DOWNSAMPLING (7.1.2)
    envelopes = abs(block_array_rect + 1j * hilbert(block_array_rect))
    N_pts = envelopes.shape[2]

    # Downsampling to 1500 Hz
    # New block and hop sizes
    sbb = 512
    shh = 128
    envelopes = resample(envelopes, sbb, axis=2)
    ########## BOUCLE SUR LES TIME BLOCKS l (voir nouveau fichier)


    # CALCULATION OF SCALED POWER SPECTRUM (7.1.3)
    spectrum = zeros((CBF,L,sbb//2))
    N_specific_max = array(N_specific).max(axis=0)
    phi_e = sum(power(envelopes * hann(sbb),2), axis=2)
    den = N_specific_max * phi_e
    # pk den nul ?

    # Hann window is precisely defined in the standard !!
    dft = power(abs(fft((envelopes * hann(sbb)),n=sbb//2, axis=2)),2)
    
    for z in range(envelopes.shape[0]): # for each CBF
        for l in range(envelopes.shape[1]): # for each time block
            if den[z,l]!=0:
                spectrum[z,l,:] = power(N_specific[z,l],2) / den[z,l] * dft[z,l,:]
    import pdb; pdb.set_trace()

    # NOISE REDUCTION OF THE ENVELOPES (7.1.4)

    # Averaging with neighbouring bands
    av_spectrum = empty((spectrum.shape))
    av_spectrum[0,:] = (spectrum[0,:]+spectrum[1,:])/2
    av_spectrum[-1,:] = (spectrum[-1,:]+spectrum[-2,:])/2
    av_spectrum[1:-1,:] = (spectrum[:-2,:]+spectrum[1:-1,:]+spectrum[2:,:])/3

    S = av_spectrum.sum(axis=0)
    SS = median(S, axis=1)

    # Weighting 
    wfw = zeros(S.shape)
    wf = zeros(S.shape)
    for k in range(sbb//2): # for each time block
        wfw[:,k] = 0.0856 * S[:,k]/(SS+10e-10) * clip(0.1891*exp(0.0120*k),0,1)
    idt = 0.05 * wfw.max(axis=1)
    Phi_E = zeros(av_spectrum.shape)
    amplitude = zeros((S.shape))

    for l in range(S.shape[0]):       
        idt = where(wfw[l,:]>0.05 * wfw[l,:].max())
        wf[l,idt] = clip(wfw[l,idt]-0.1407,0,1)
        
        for z in range(CBF):
            Phi_E[z,l,:] = av_spectrum[z,l,:] * wf[l,:]
            # Critical bands characteristics for the weightings to come
            fmax = f_max(center_freq[z]) # center_freq = fréquence centrale de la bande z (eq 86 clause 7.1.5.2)
            rmax = r_max(center_freq[z])
            q2_high = Q2_high(center_freq[z])
            q2_low = Q2_low(center_freq[z])

            # refaire boucle sur z ???

        # SPECTRAL WEIGHTING (7.1.5)
        for k in range(sbb//2):
            # Peak picking
            maxima = find_peaks(Phi_E[:,l,k])[0]
            
            if len(maxima) == 0:
                print('no peak')
                amplitude[l,z] = 0
                prominence = []
                prominence_idx = []
            elif len(maxima) > 0:
                if len(maxima) == 1:
                    print('only 1 peak')
                    prominence = _comp_prominence(Phi_E[:,l,k], maxima, 0)
                    prominence_idx = maxima

                elif len(maxima) > 0:
                    print('multiple peaks')
                    prominence = zeros(len(maxima))
                    # For each peak
                    for i in range(len(maxima)):
                        prominence[i] = _comp_prominence(Phi_E[:,l,k], maxima, i)
                    # Keep 10 maximum values
                    if len(maxima) > 10:
                        sort_idx = argsort(prominence)
                        prominence = prominence[sort_idx[-10:]]
                        prominence_idx = maxima[sort_idx[-10:]]
                    else:
                        prominence_idx = maxima
                idx = where((Phi_E[prominence_idx,l,k]) <= 0.05*max(Phi_E[prominence_idx,l,k]))[0]
                prominence = delete(prominence, idx)
                prominence_idx = delete(prominence_idx, idx)

                print(prominence)

                N_peak = len(prominence)
                amp = zeros(N_peak)
                mod_rate = zeros(N_peak)

                # For each prominent peak identified
                for i in range(N_peak):
                    # Refinement step
                    K = array([[prominence_idx[i]**2, prominence_idx[i]-1, 1],[prominence_idx[i]**2, prominence_idx[i], 1],[(prominence_idx[i]+1)**2, prominence_idx[i]+1, 1]])
                    
                    if k == 0:
                        Phi = array([0, Phi_E[prominence_idx[i],l,k], Phi_E[prominence_idx[i],l,k+1]])
                    elif k == (sbb/2)-1:
                        Phi = array([Phi_E[prominence_idx[i],l,k-1], Phi_E[prominence_idx[i],l,k], 0])
                    else:
                        Phi = array([Phi_E[prominence_idx[i],l,k-1], Phi_E[prominence_idx[i],l,k], Phi_E[prominence_idx[i],l,k+1]])
                    C = dot(inv(K), Phi)

                    delta_f = 1500/512
                    F = -C[1]/(2*C[0])*delta_f
                    mod_rate[i] = F + rho(F, delta_f) # modulation rate

                    # Weighting of high modulation rates
                    if k == 0:
                        amp_temp = Phi_E[prominence_idx[i],l,k] + Phi_E[prominence_idx[i],l,k+1] 
                    elif k == (sbb/2)-1:
                        amp_temp = Phi_E[prominence_idx[i],l,k-1] + Phi_E[prominence_idx[i],l,k]
                    else:
                        amp_temp = Phi_E[prominence_idx[i],l,k-1] + Phi_E[prominence_idx[i],l,k] + Phi_E[prominence_idx[i],l,k+1] 
                    amp[i] = _high_mod_rate_weighting(mod_rate[i], amp_temp, fmax, rmax, q2_high)


                # Estimation of fundamental modulation rate (7.1.5.3) (ne dépend pas de l et z)
                complex_energy = zeros((N_peak))
                harmonic_complex = zeros((N_peak), dtype=object)
                for i0 in range(N_peak):
                    mod_rate_temp = mod_rate[i0:]
                    R = round(mod_rate_temp/mod_rate[i0])
                    
                    # check for duplicates in R
                    if len(R)>1:
                        duplicates = set()
                        duplicates = [x for x in R if x in duplicates or duplicates.add(x)]
                    else:
                        duplicates = []

                    if len(duplicates)> 0 :
                        delete_list = array([])
                        for dup in duplicates:                                
                            dup_idx = where((R==dup))[0]
                            keep = argmin(abs(mod_rate_temp[dup_idx]/(array(R)[dup_idx]*mod_rate[i0])-1))
                            delete_list = append(delete_list, [dup_idx[x] for x in range(len(dup_idx)) if x!=keep])
                        R = delete(R, squeeze(delete_list).astype(int32))
                        mod_rate_temp = delete(mod_rate_temp, squeeze(delete_list).astype(int32))   
                        
                        
                    harmonic_complex[i0] = where((abs(mod_rate_temp/(R*mod_rate[i0])-1) < 0.04))[0]
                    complex_energy[i0] = sum(amp[harmonic_complex[i0]])
                        
                i_max = argmax(complex_energy)
                h_complex_max = harmonic_complex[argmax(complex_energy)]

                w = 1 + 0.1 * abs(sum(mod_rate[h_complex_max]*amp[h_complex_max])/sum(amp[h_complex_max])-mod_rate[argmax(amp[h_complex_max])])**0.749
                amp_temp = amp[h_complex_max] * w

                
                # Weighting of low modulation rates
                amplitude[l,z] = _low_mod_rate_weighting(mod_rate[i_max], amp_temp, fmax, q2_low)

                if amplitude[l,z]<0.074376:
                    amplitude[l,z] = 0


    # ENTROPY WEIGHTING (OPTIONAL) (7.1.6)


    # CALCULATION OF TIME DEPENDENT SPECIFIC ROUGHNESS (7.1.7)

    # amplitude_50 = CubicHermiteSpline(amplitude, linspace(0,256),)
    
    amplitude_50 = resample(amplitude, int(N_pts/48000*50), axis=1)
    amplitude_50 = amplitude_50[:,:int(duration*50)] # delete zero-padding
    
    idx = where((amplitude_50>=0))
    R_est = zeros((amplitude_50.shape))
    R_est[idx] = amplitude_50[idx]

    R_mean = sum(R_est, axis=1)/53

    if R_mean != 0 :
        B = sqrt(sum(R_est, axis=1)**2/53) / R_mean
    else :
        B = 0

    E = 0.95555 * (tanh(1.6407*(B-2.5804))+1)*0.5+0.58449

    R_spec_temp = 0.0180909 * power(R_est,E)

    slope = sign(diff(R_spec_temp))
    
    tau = zeros(len(slope))
    tau[slope>=0] = 0.0625
    tau[slope<0] = 0.5000
    
    R_spec = zeros((len(R_spec_temp)))
    R_spec[0] = R_spec_temp[0]
    R_spec[1:] = R_spec[1:]*(1-exp(-1/(50*tau)))  + R_spec[0:]*exp(-1/(50*tau))

    # CALCULATION OF REPRESENTATIVE VALUES (7.1.8)

    # CALCULATION OF ROUGHNESS FOR BINAURAL SIGNALS

    import pdb; pdb.set_trace()


    return envelopes


signal, fs = load(r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod70.wav", wav_calib=0.02)
signal, fs = load(r"C:\Users\LAP16\Desktop\loudness scale\marteau_piqueur.wav", wav_calib=0.2)
import matplotlib.pyplot as plt

envelopes = roughness_ecma(signal[:int(len(signal)/2)])



