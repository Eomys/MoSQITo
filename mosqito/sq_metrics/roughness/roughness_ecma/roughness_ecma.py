from numpy import(abs,arange,cos,pi,append,power,zeros,empty, sum, array,clip,  exp, median,where,argmax,argmin,argsort,
                  delete, exp, round, squeeze, sqrt, tanh, diff, percentile, int32, transpose, mean, vstack, linspace,
                  apply_along_axis)
from numpy.fft import rfft, fft
from scipy.signal import hilbert, resample, find_peaks, peak_prominences
import matplotlib.pyplot as plt
import numpy as np
# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._band_pass_signals import _band_pass_signals
from mosqito.sq_metrics.loudness.loudness_ecma._auditory_filters_centre_freq import _auditory_filters_centre_freq

# Data import
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_from_bandpass import _loudness_from_bandpass
from mosqito.sq_metrics.roughness.roughness_ecma._weighting import f_max, r_max, Q2_high, Q2_low, _high_mod_rate_weighting, _low_mod_rate_weighting
from mosqito.sq_metrics.roughness.roughness_ecma._refinement import _refinement

def roughness_ecma(signal, fs, plot=False):
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
    if fs != 48000:
        print(
            "[Warning] Signal resampled to 48 kHz fulfill the standard requirements and allow calculation."
        )
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000
    
    # INITIALIZE COMPUTATION PARAMETERS
    # Number of critical bands and their center frequency
    CBF = 53
    center_freq = _auditory_filters_centre_freq()
    # Hop size and block size for specific loudness calculation (7.1.1)
    sb=16384
    sh=4096
    duration =  len(signal) / fs

    # LOUDNESS COMPUTATION
    block_array_rect = array(_band_pass_signals(signal, sb, sh))
    L = block_array_rect.shape[1]
    N_specific, bark_axis = _loudness_from_bandpass(block_array_rect)
    N_specific = N_specific.T
    
    # ENVELOPPE CALCULATION AND DOWNSAMPLING (7.1.2)
    #envelopes = abs(block_array_rect + 1j * hilbert(block_array_rect))  
    envelopes0 = abs(hilbert(block_array_rect))
    
    # .........................................................................
    # plot envelope and bandpass signal for one segment
    
    
    
    if plot is True:
        from mosqito.utils.conversion import bark2freq
        band_to_plot = 35
        timestep_to_plot = 8
        
        t = np.linspace(0, (sb-1)/fs, sb)
        
        
        plt.figure()
        plt.plot(t, envelopes0[band_to_plot, timestep_to_plot, :],
                label='Envelope')
        plt.plot(t, block_array_rect[band_to_plot, timestep_to_plot, :], ':',
                label='Bandpass Signal')
        plt.legend()
        plt.xlim([0, 0.03])
        plt.title(f'{bark_axis[band_to_plot]:1.0f} Bark ({bark2freq(bark_axis[band_to_plot]):1.0f} Hz)')
        plt.tight_layout()
        plt.show(block=True)
    # .........................................................................
    
    # Downsampling to 1500 Hz
    sbb = 512 # new block size
    K = sbb//2 
    envelopes = resample(envelopes0, sbb, axis=2)  
    envelopes = transpose(envelopes,(1,0,2)) # transpose is used to stick to the standard index order l,z,k
    
    # .........................................................................
    # compare original and downsampled envelope
    
    
    if plot is True:
        from mosqito.utils.conversion import bark2freq
        
        band_to_plot = 35
        timestep_to_plot = 8
        
        t = np.linspace(0, (sb-1)/fs, sb)
        t_ = np.linspace(0, (sbb-1)/1500, sbb)
        
        plt.figure()
        plt.plot(t, envelopes0[band_to_plot, timestep_to_plot, :], 'o-',
                label='Envelope [original]')
        
        # # plot every 32nd sample in p_env for visual reference
        # plt.plot(t[::32], p_env[band_to_plot, timestep_to_plot, ::32], 's-.',
        #          color='C1', label='Envelope [every 32nd sample]')
        
        plt.plot(t_, envelopes[timestep_to_plot, band_to_plot,  :], '^:',
                markersize=12, color='C3', label='Envelope [downsampled]')
        plt.legend()
        plt.grid()
        plt.xlim([0, 0.015])
        plt.tight_layout()
        plt.title(f'{bark_axis[band_to_plot]:1.0f} Bark ({bark2freq(bark_axis[band_to_plot]):1.0f} Hz)')
        plt.show(block=True)
    
    # plt.savefig(f'04_DownsampledSignalsEnvelope_CritBand{band_to_plot}.png')
    
    # ************************************************************************

    
    # CALCULATION OF SCALED POWER SPECTRUM (7.1.3)
    K = sbb//2
    N_specific_max = array(N_specific).max(axis=1)
    
    # Hann window is precisely defined in the standard (different from numpy version)
    hann_window = (0.5-0.5*cos(2*pi*arange(sbb)/sbb))/sqrt(0.375)
    hann_window = hann_window / sum(hann_window)
        
    # phi_e0 = np.sum(power(envelopes * hann_window,2), axis=2)
    # den = transpose(N_specific_max * transpose(phi_e0))
    
    # scaling = np.zeros((L,CBF))
    # scaling[den!=0]  = power(N_specific[den!=0],2) / den[den!=0] 
    spectrum = zeros((L,CBF,K))
    phi_e0 = sum(power(envelopes * hann_window,2), axis=2)
    den = transpose(N_specific_max * transpose(phi_e0))
    idx = where((den!=0))
    # Hann window is precisely defined in the standard (different from numpy version)
    dft = power(abs(rfft((envelopes * hann_window), n=sbb-1, axis=2)),2)
    spectrum[idx[0],idx[1],:] = transpose(power(N_specific[idx],2) / den[idx] * transpose(dft[idx[0],idx[1],:]))    
    
    # plt.figure()
    # plt.title('Phi_e 0')
    # plt.plot(phi_e0)
    # plt.figure()
    # plt.title('Dénominateur')
    # plt.plot(den)
    
    if plot is True:
        plt.figure()
        plt.title('Scaling')
        plt.plot(scaling)
    
    #spectrum = scaling[..., np.newaxis] * power(abs(rfft((envelopes * hann_window), n=sbb-1, axis=2)),2)
    
    # .........................................................................
    # plot scaled power spectrum for one time segment
    
    if plot is True:
        timestep_to_plot = 8
        
        df_ = 1500/sbb
        f = np.linspace(0, 1500 - df_, sbb)[:sbb//2+1]
        
        Pspec = 10*np.log10(spectrum[timestep_to_plot, :,  :sbb//2+1]+0.00000000001)
    
        plt.figure()
        plt.pcolormesh(f, bark_axis, Pspec, 
                    vmax=np.max(Pspec), vmin=np.max(Pspec)-80)
        plt.title(f'Scaled power spectrum of envelopes')
        plt.xlabel('Freq [Hz]')
        plt.ylabel('Critical band [Bark]')
        plt.colorbar()
        plt.show(block=True)
    
    # .........................................................................
    
    
    
    
    # NOISE REDUCTION OF THE ENVELOPES (7.1.4)
    # Averaging with neighbouring bands
    av_spectrum = empty((L,CBF,K))
    av_spectrum[:,0] = (spectrum[:,0] + spectrum[:,1])/2
    av_spectrum[:,-1] = (spectrum[:,-1] + spectrum[:,-2])/2
    av_spectrum[:,1:-1] = (spectrum[:,:-2] + spectrum[:,1:-1] + spectrum[:,2:])/3
    S = av_spectrum.sum(axis=1)
    SS = median(S[:,2:], axis=1)
    
    # .........................................................................
    # plot averaged power spectrum for one time segment
    
    # bark_axis = np.linspace(0.5, 26.5, num=53, endpoint=True)
    # fs_ = 1500
    # df_ = fs_/sbb
    # f = np.linspace(0, fs_ - df_, sbb)[:sbb//2+1]
    # timestep_to_plot = 8
    # Pspec1 = 10*np.log10(spectrum[timestep_to_plot, :, :sbb//2+1])
    
    # plt.figure()
    # plt.pcolormesh(f, bark_axis, Pspec1,
    #                vmax = np.max(Pspec1), vmin=np.max(Pspec1)-80)
    # plt.title('Original power spectrum of envelopes')
    # plt.xlabel('Freq [Hz]')
    # plt.ylabel('Critical band [Bark]')
    # plt.colorbar()
    # plt.tight_layout()
    
    # plt.figure()
    # Pspec2 = 10*np.log10(av_spectrum[timestep_to_plot, :, :sbb//2+1])
    # plt.pcolormesh(f, bark_axis, Pspec2,
    #                vmax = np.max(Pspec2), vmin=np.max(Pspec2)-80)
    # plt.title('Averaged power spectrum of envelopes')
    # plt.xlabel('Freq [Hz]')
    # plt.ylabel('Critical band [Bark]')
    # plt.colorbar()
    # plt.tight_layout()
    
    if plot is True:
        plt.figure()
        freqs = linspace(0, 1500//2, 512)
        plt.plot(freqs, spectrum[3,5,:])
        plt.plot(freqs, spectrum[3,4,:])
        plt.plot(freqs, spectrum[3,6,:])
        plt.plot(freqs, av_spectrum[3,5,:], 'k')
        plt.title('Average spectrum')
        plt.show(block=True)
    # .........................................................................
    


    # Weighting 
    noise_suppression_weighting = zeros((L,K))
    w_wave = 0.0856 * S/(SS[:,None]+10e-10) * clip(0.1891*exp(0.0120*arange(K)),0,1)
    idx = where((w_wave>=0.05 * w_wave[:,2:].max()))
    noise_suppression_weighting[idx] = clip(w_wave[idx]-0.1407,0,1)
    Phi_E = av_spectrum * noise_suppression_weighting[:,None,:]
    
    if plot is True:
        plt.figure()
        plt.pcolormesh(f, np.arange(noise_suppression_weighting.shape[0]), noise_suppression_weighting[:, :sbb//2+1])
        plt.title(f"Weighting coefficient 'w' (Eq. 70)")
        plt.xlabel('Freq [Hz]')
        plt.ylabel('Time step')
        plt.colorbar()
        plt.tight_layout()
        plt.show(block=True)
        
        plt.figure()
        plt.plot(av_spectrum[5,:,:].T, 'b')
        plt.plot(Phi_E[5,:,:].T, 'k')
        plt.plot(noise_suppression_weighting[5,:], 'r')
        plt.title("Noise suppression")

    # Critical bands characteristics for the weightings to come
    fmax = f_max(center_freq) # center_freq = fréquence centrale de la bande z (eq 86 clause 7.1.5.2)
    rmax = r_max(center_freq)
    q2_high = Q2_high(center_freq)
    q2_low = Q2_low(center_freq)

    # Peak picking
    # maxima = apply_along_axis(find_peaks, axis=2, arr=Phi_E)[...,0]
    
    # maxima = apply_along_axis(find_peaks, axis=0, arr=np.ones((10,10,10)))[...,0]
    
    
    
    # plt.figure()
    # plt.plot(Phi_E[5,10,:])
    # plt.plot(maxima[5,10], Phi_E[5,10,maxima[5,10]], 'o')
    # plt.title("Peak picking")

    amplitude = zeros((L,CBF))
    for l in range(L):       
        for z in range(CBF):
            maxima_idx, _ = find_peaks(Phi_E[l, z, :])
            
            #maxima_idx = maxima[l,z]
            
            # SPECTRAL WEIGHTING (7.1.5)
            if len(maxima_idx) > 0:
                maxima_idx = delete(maxima_idx, where((Phi_E[l,z,maxima_idx]) <= 0.05*max(Phi_E[l,z,maxima_idx]))[0])
            if len(maxima_idx) == 0:
                amplitude[l,z] = 0
            else :
                prominence, _, _ = peak_prominences(Phi_E[l,z,:], maxima_idx)  # résultats de prominence identiques à _comp_prominence
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
                        
                        #_estimate_fund_mod_rate()
                        
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
    
    R_est = zeros((N50, CBF))
    R_est[where((amplitude_50>=0))] = amplitude_50[where((amplitude_50>=0))]

    R_lin_mean = sum(R_est, axis=1)/53
    R_sq_mean = sqrt(sum(R_est, axis=1)**2/53)

    B = zeros((N50))
    B[R_lin_mean!=0] = R_sq_mean[R_lin_mean!=0] / R_lin_mean[R_lin_mean!=0]
    E = 0.95555 * (tanh(1.6407*(B-2.5804))+1) * 0.5 + 0.58449

    R_time_spec_temp = transpose(0.018 * 0.75 * power(transpose(R_est),E))
    slope = vstack((R_time_spec_temp[None,0,:],diff(R_time_spec_temp, axis=0)[:-1,:]))

    tau = zeros((N50-1,CBF))
    tau[where((slope>=0))] = 0.0625
    tau[where((slope<0))] = 0.5000
    R_time_spec = zeros((N50, CBF))
    R_time_spec[0,:] = R_time_spec_temp[0,:] / 10
    R_time_spec[1:,:] = (R_time_spec_temp[1:,:]*(1-exp(-1/(50*tau)))  + R_time_spec_temp[:-1,:]*exp(-1/(50*tau))) / 10

    # CALCULATION OF REPRESENTATIVE VALUES (7.1.8)
    # CBF dependent value
    R_spec = mean(R_time_spec[10:,:], axis=0) 
    # time_dependent value
    R_time = 0.5 * sum(R_time_spec, axis=1)
    # single value
    R = percentile(R_time, 90)
    
    if plot is True:
        plt.figure()
        plt.plot(0.6 * sum(R_time_spec, axis=1))
    
    return R_time, R_spec, R

if __name__ == "__main__":
    import numpy as np
    
    # file = r"C:\Users\SaloméWanty\Downloads\spectro_Vibrations_norm_104.wav"

    # from mosqito import load
    # sig, fs = load(file, wav_calib=2e-5)
    # R_time, R_spec, R_time, R = roughness_ecma(sig, fs)
    
    
    
    def signal_test(fs, d, fc, fmod, dB, mdepth=1):
        dt = 1 / fs
        time = np.arange(0, d, dt)

        signal = (
            0.5
            * (1 + mdepth * (np.sin(2 * np.pi * fmod * time)))
            * np.sin(2 * np.pi * fc * time)
        )    
        
        rms = np.sqrt(np.mean(np.power(signal, 2)))
        ampl = 0.00002 * np.power(10, dB / 20) / rms
        signal = signal * ampl
        return signal
    
    
    file = r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_ecma\validation_specific_roughness_ecma.xlsx"
    import matplotlib.colors as mcolors
    fc = [125,250,500,1000,2000,4000, 8000]
    fmod = [20,30,40,50,60,70,80,90,100,120,140,160,200,300,400]
    fs = 48000
    d = 0.25
    dB = 60
    mdepth = 1
    fc = [1000]
    fmod = [70]
    Ro = np.empty((len(fc), len(fmod)))
    Rref = np.empty((len(fc), len(fmod)))
    for i in range(len((fc))):
        for j in range(len((fmod))):
            carrier = fc[i]
            mod = fmod[j]
            stimulus = signal_test(fs, d, carrier, mod, dB, mdepth)
            R_time, R_spec, R = roughness_ecma(stimulus, fs)
            Ro[i,j] = R
            
            # plt.figure()
            # plt.step(ref_spec[:,0], ref_spec[:,1], label="Artemis", color="k")
            # plt.step(_auditory_filters_centre_freq(), R_spec, label="Mosqito", color="#69c3c5")
            # plt.title("Artemis="+ref_R+"\n MOSQITO="+f"{R:.3f}"+" asper")
            # plt.legend()
            # plt.xlim(-5,9000)
            # plt.xlabel("Asper/Bark")
            # plt.ylabel("Frequency [Hz]")
            # # plt.show(block=True)
            # plt.savefig(r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\roughness\output\fc_" + f"{carrier}" +"_fmod_" + f"{mod}"+ ".png" )

    colors = plt.cm.rainbow(np.linspace(0,1,len(Ro)))
    plt.figure()
    for i in range(len((fc))):  
        plt.plot(np.array(fmod), Ro[i,:] + i, label=f"{fc[i]}", marker='o', color=colors[i])
        plt.plot(np.array(fmod), Rref[i,:] + i, marker='s', linestyle='--', color=colors[i])
    plt.legend()
    
    colors = plt.cm.rainbow(np.linspace(0,1,len(fmod)))
    plt.figure()
    for j in range(len((fmod))):  
        plt.plot(fc, Ro[:,j]+3*j, label=f"{fmod[j]}", marker='o', color=colors[j])
        plt.plot(fc, Rref[:,j]+3*j, marker='s', linestyle='--', color=colors[j])
    plt.legend()
    plt.show(block=True)
    
    from matplotlib import cm
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    Y, X = np.meshgrid(fc, fmod)
    ax.plot_surface(X, Y, Ro.T, cmap=cm.coolwarm)
    ax.plot_wireframe(X, Y, Rref.T, color='k')

    ax.set_xlabel('Fc Label')
    ax.set_ylabel('Fmod Label')
    ax.set_zlabel('R Label')
    

    plt.show(block=True)
    
    print('pause')


