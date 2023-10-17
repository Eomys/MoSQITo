from numpy import(abs,arange,cos,pi,append,power,zeros,empty,sum,array,clip,exp,median,where,argmax,argmin,argsort,
                  delete,exp,dot,round,squeeze,sqrt,tanh,sign,diff,percentile,dot,int32,transpose,mean, linspace, vstack,
                  apply_along_axis, nan, sinh)
from numpy.fft import fft
from scipy.signal import (hilbert, resample, find_peaks)
from scipy.signal.windows import hann


# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._rectified_band_pass_signals import _rectified_band_pass_signals
from mosqito.utils.conversion import bark2freq
#from mosqito.sq_metrics.loudness.loudness_ecma._auditory_filters_centre_freq import _auditory_filters_centre_freq

# Data import
# Threshold in quiet
from mosqito.sq_metrics import loudness_ecma
from mosqito.utils import load
from _weighting import f_max, r_max, Q2_high, Q2_low, _high_mod_rate_weighting, _low_mod_rate_weighting
from _comp_prominence import _comp_prominence
from _comp_prominence_old import _comp_prominence_old
from _refinement import _refinement


def find_maxima(Phi_E):
    print(Phi_E.shape)
    idx = find_peaks(Phi_E)[0]
    if idx.size == 0:
        return nan
    else:
        return idx 
    


def _auditory_filters_centre_freq():
    """
    Auditory filter bank center frequencies generation

    This function generates the Auditory filter bank center frequencies according
    to ECMA-418-2 section 5.1.4.1 equation 9

    Parameters
    ----------

    Returns
    -------
    centre_freq: ndarray
        Vector of auditory filter bank center frequencies

    """

    z = arange(0.5,27,0.5)
    df_0 = 81.9289  # ECMA-418-2
    c = 0.1618  # ECMA-418-2

    # Central frequency
    center_freq = (df_0 / c) * sinh(c * z)

    return center_freq


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
    N_specific, _ = loudness_ecma(signal, sb, sh)
    N_specific = array(transpose(N_specific))
    # ! ces valeurs sont déjà calculées dans la loudness -> créer fonction loudness from band-pass ?
    block_array_rect = array(_rectified_band_pass_signals(signal, sb, sh))
    L = block_array_rect.shape[1]

    # ENVELOPPE CALCULATION AND DOWNSAMPLING (7.1.2)
    envelopes = abs(block_array_rect + 1j * hilbert(block_array_rect))  # transpose is used to stick to the standard index order l,z,k
    # Downsampling to 1500 Hz
    sbb = 512 # new block size
    K = sbb//2 
    envelopes = resample(envelopes, sbb, axis=2)
    envelopes = transpose(envelopes,(1,0,2))


    # CALCULATION OF SCALED POWER SPECTRUM (7.1.3)
    spectrum = zeros((L,CBF,K))
    N_specific_max = array(N_specific).max(axis=1)
    hann_window = (0.5-0.5*cos(2*pi*arange(sbb)/sbb))/sqrt(0.375)
    #hann_window = hann_window / sum(hann_window)
    phi_e = sum(power(envelopes * hann_window,2), axis=2)
    den = transpose(N_specific_max * transpose(phi_e))
    # Hann window is precisely defined in the standard (different from numpy version)
    dft = power(abs(fft((envelopes * hann_window),n=K, axis=2)/1.18),2)
    spectrum[where((den!=0))[0],where((den!=0))[1],:] = transpose(power(N_specific[where((den!=0))],2) / den[where((den!=0))] * transpose(dft[where((den!=0))[0],where((den!=0))[1],:]))

    # NOISE REDUCTION OF THE ENVELOPES (7.1.4)
    # Averaging with neighbouring bands
    av_spectrum = empty((L,CBF,K))
    av_spectrum[:,0] = (spectrum[:,0]+spectrum[:,1])/2
    av_spectrum[:,-1] = (spectrum[:,-1]+spectrum[:,-2])/2
    av_spectrum[:,1:-1] = (spectrum[:,:-2]+spectrum[:,1:-1]+spectrum[:,2:])/3

    S = av_spectrum.sum(axis=1)
    SS = median(S, axis=1)

    # Weighting 
    noise_suppression_weighting = zeros((L,K))
    w_wave = 0.0856 * S/(SS[:,None]+10e-10) * clip(0.1891*exp(0.0120*arange(K)),0,1)
    w_wave[where((w_wave<=0.05 * w_wave.max()))] = 0
    noise_suppression_weighting = clip(w_wave-0.1407,0,1)
    Phi_E = av_spectrum * noise_suppression_weighting[:,None,:]

    # Critical bands characteristics for the weightings to come
    fmax = f_max(center_freq) # center_freq = fréquence centrale de la bande z (eq 86 clause 7.1.5.2)
    rmax = r_max(center_freq)
    q2_high = Q2_high(center_freq)
    q2_low = Q2_low(center_freq)

    # Peak picking
    maxima = apply_along_axis(find_peaks, axis=2, arr=Phi_E)[...,0]

    amplitude = zeros((L,CBF))
    for l in range(L):       
        for z in range(CBF):
            maxima_idx = maxima[l,z]
            # SPECTRAL WEIGHTING (7.1.5)
            if len(maxima_idx) == 0:
                amplitude[l,z] = 0
            elif len(maxima_idx) > 0:
                maxima_idx = delete(maxima_idx, where((Phi_E[l,z,maxima_idx]) <= 0.05*max(Phi_E[l,z,maxima_idx]))[0])
            if len(maxima_idx) == 0:
                amplitude[l,z] = 0
            else :
                prominence = _comp_prominence(Phi_E[l,z,:], maxima_idx)
                # Keep 10 maximum values
                if len(maxima_idx) > 10:
                    sort_idx = argsort(prominence)
                    prominence = prominence[sort_idx[-10:]]
                    prominence_idx = maxima_idx[sort_idx[-10:]]
                else:
                    prominence_idx = maxima_idx

                N_peak = len(prominence)
                amp = zeros(N_peak)
                mod_rate = zeros(N_peak)
                complex_energy = zeros((N_peak))
                harmonic_complex = zeros((N_peak), dtype=object)

                if N_peak == 1:
                    # Refinement step
                    mod_rate, amp_temp = _refinement(prominence_idx[0], Phi_E[l,z,:])
                    # Weighting of modulation rates
                    amp_temp = _high_mod_rate_weighting(mod_rate, amp_temp, fmax[z], rmax[z], q2_high[z])
                    amplitude[l,z] = _low_mod_rate_weighting(mod_rate, array([amp_temp]), fmax[z], q2_low[z])
                else:
                    # Modulation rate and maxima's amplitudes
                    for i0 in range(N_peak):
                        kpi = prominence_idx[i0]
                        # Refinement step
                        mod_rate[i0], amp_temp = _refinement(kpi, Phi_E[l,z,:])
                        # Weighting of high modulation rates
                        amp[i0] = _high_mod_rate_weighting(mod_rate[i0], amp_temp, fmax[z], rmax[z], q2_high[z])

                    # Estimation of fundamental modulation rate (7.1.5.3) (ne dépend pas de l et z)
                    for i0 in range(N_peak):
                        mod_rate_temp = mod_rate[i0:]
                        R = round(mod_rate_temp/mod_rate[i0]) 
                        # check for duplicates in R
                        if len(R)>1:
                            duplicates = set()
                            duplicates = [x for x in R if x in duplicates or duplicates.add(x)]
                            if len(duplicates)> 0 :
                                delete_list = array([])
                                for dup in duplicates:                                
                                    dup_idx = where((R==dup))[0]
                                    keep = argmin(abs(mod_rate_temp[dup_idx]/(array(R)[dup_idx]*mod_rate[i0])-1))
                                    delete_list = append(delete_list, [dup_idx[x] for x in range(len(dup_idx)) if x!=keep])
                                R = delete(R, squeeze(delete_list).astype(int32))
                                mod_rate_temp = delete(mod_rate_temp, squeeze(delete_list).astype(int32))   
                        else:
                            duplicates = []     
                        harmonic_complex[i0] = where((abs(mod_rate_temp/(R*mod_rate[i0])-1) < 0.04))[0]
                        complex_energy[i0] = sum(amp[harmonic_complex[i0]])
                    # The harmonic complex corresponding to the best fundamental modulation rate is the one with the highest sum
                    i_max = argmax(complex_energy)
                    h_complex_max = harmonic_complex[argmax(complex_energy)]
                    w = 1 + 0.1 * abs(sum(mod_rate[h_complex_max]*amp[h_complex_max])/sum(amp[h_complex_max])-mod_rate[argmax(amp[h_complex_max])])**0.749
                    # print(mod_rate[i_max])
                    amp_temp = amp[h_complex_max] * w
                    # Weighting of low modulation rates
                    amplitude[l,z] = _low_mod_rate_weighting(mod_rate[i_max], amp_temp, fmax[z], q2_low[z])

            if amplitude[l,z]<0.074376:
                amplitude[l,z] = 0

    
    # OPTIONAL ENTROPY WEIGHTING (specific to ITT equipment): needs a signal of rotational speed (7.1.6)

    # CALCULATION OF TIME DEPENDENT SPECIFIC ROUGHNESS (7.1.7)
    N50 = int(duration*50)
    amplitude_50 = resample(amplitude, N50, axis=0)
    amplitude_50 = amplitude_50[:N50,:] # delete zero-padding

    #N50 = L
    #amplitude_50 = amplitude
    
    R_est = zeros((N50, CBF))
    R_est[where((amplitude_50>=0))] = amplitude_50[where((amplitude_50>=0))]

    R_lin_mean = sum(R_est, axis=1)/53
    R_sq_mean = sqrt(sum(R_est, axis=1)**2/53)

    B = zeros((N50))
    B[R_lin_mean!=0] = R_sq_mean[R_lin_mean!=0] / R_lin_mean[R_lin_mean!=0]
    E = 0.95555 * (tanh(1.6407*(B-2.5804))+1) * 0.5 + 0.58449

    R_time_spec_temp = transpose(0.0180909 * 0.75 * power(transpose(R_est),E))

    slope = vstack((R_time_spec_temp[None,0,:],diff(R_time_spec_temp, axis=0)[:-1,:]))

    tau = zeros((N50-1,CBF))
    tau[where((slope>=0))] = 0.0625
    tau[where((slope<0))] = 0.5000
    R_time_spec = zeros((N50, CBF))
    R_time_spec[0,:] = R_time_spec_temp[0,:]
    R_time_spec[1:,:] = R_time_spec_temp[1:,:]*(1-exp(-1/(50*tau)))  + R_time_spec_temp[:-1,:]*exp(-1/(50*tau))

    # CALCULATION OF REPRESENTATIVE VALUES (7.1.8)
    # CBF dependent value
    R_spec = mean(R_time_spec[15:,:], axis=0)
    # time_dependent value
    R_time = 0.2 * sum(R_time_spec, axis=1)
    # single value
    R = percentile(R_time[15:], 90)
    
    return R_spec, R_time, R

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from numpy import array
    freqs = _auditory_filters_centre_freq()

    # path = [r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod20.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod30.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod40.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod50.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod60.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod70.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod80.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod90.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod100.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod120.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod140.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod160.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod180.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod200.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod300.wav",
    #         r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod400.wav"
    #         ]
    # ref = array([0.2340, 0.4596, 0.7007, 0.8960, 0.9768, 1.0009, 0.9185, 0.7998, 0.6840, 0.5003, 0.3748, 0.2888, 0.2309, 0.1956, 0.0910, 0.0419])
    # R = zeros((16))
    # plt.figure()
    # for i in range(16):
    #     print("Signal n : ", i)
    #     signal, fs = load(path[i])
    #     R_spec, R_time, R[i] = roughness_ecma(signal[:int(len(signal)/2)])
    #     plt.step(freqs, R_spec, 'o',where='post', color="#0069a1", linestyle='--')

    # x = [20,30,40,50,60,70,80,90,100,120,140,160,180,200,300,400]
    # plt.figure()
    # plt.step(x, R, 'blue')
    # plt.step(x, ref, 'red', linewidth=8, alpha=0.25, label='référence Artemis')
    

    x_ref = [485.20056, 544.18116, 603.69901, 673.39525, 738.9283, 815.28005, 899.52143, 981.68271, 1077.21749, 1175.60934, 1290.01601, 1400.1749, 1519.74064, 1658.55205, 1810.04311, 1964.60889, 2132.37358, 2314.46426, 2525.86485, 2726.6215]
    y_ref = [0, 0.00781, 0.02344, 0.05468, 0.11978, 0.2285, 0.3255, 0.36976, 0.29881, 0.21418, 0.1328, 0.08137, 0.05013, 0.0306, 0.01888, 0.01042, 0.00586, 0.00325, 0.0013, 0.00065]
    
    plt.figure()
    signal, fs = load(r"C:\Users\LAP16\Documents\MoSQITooo\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod70.wav")
    R_spec, R_time, R = roughness_ecma(signal)
    #signal, fs = load(r"C:\Users\LAP16\Desktop\loudness scale\marteau_piqueur.wav")
    #R_spec, R_time, R = roughness_ecma(signal)
    print(R)

    plt.step(freqs, R_spec, where='mid', label='mosqito')
    plt.step(x_ref, y_ref, 'red', where='post', linewidth=8, alpha=0.25, label='référence Artemis')
    plt.title('Specific roughness, global value = 0.13')
    plt.xlabel('Frequency band [Bark]')
    plt.ylabel('Specific roughness [Asper/Bark]')
    plt.grid(visible=True)
    plt.legend()
    plt.show(block=True)
    

    print('done')
