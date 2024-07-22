import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy.fft import fft
from scipy.signal import hilbert, resample, decimate

# Set the default color cycle
from mosqito import COLORS as clr
import matplotlib as mpl
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=clr)

# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._preprocessing import _preprocessing
from mosqito.sq_metrics.loudness.loudness_ecma._band_pass_signals import _band_pass_signals
from mosqito.sq_metrics.loudness.loudness_ecma._ecma_time_segmentation import _ecma_time_segmentation
from mosqito.sq_metrics.loudness.loudness_ecma._auditory_filters_centre_freq import _auditory_filters_centre_freq
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_from_bandpass import _loudness_from_bandpass

from mosqito.sq_metrics.roughness.roughness_ecma._weighting import _f_max, _r_max, _Q2_high, _Q2_low, _high_mod_rate_weighting, _low_mod_rate_weighting
from mosqito.sq_metrics.roughness.roughness_ecma._estimate_fund_mod_rate import _estimate_fund_mod_rate
from mosqito.sq_metrics.roughness.roughness_ecma._peak_picking import _peak_picking
from mosqito.sq_metrics.roughness.roughness_ecma._von_hann_window import _von_hann_window
from mosqito.sq_metrics.roughness.roughness_ecma._noise_reduction import _noise_reduction
from mosqito.sq_metrics.roughness.roughness_ecma._interpolation_50 import _interpolation_50
from mosqito.sq_metrics.roughness.roughness_ecma._non_linear_transform import _non_linear_transform
from mosqito.sq_metrics.roughness.roughness_ecma._lowpass_filter import _lowpass_filter

from mosqito.utils.conversion.bark2freq import bark2freq


def roughness_ecma_validation_plots(signal, fs, show=True, save=False, save_path=None):
    """Calculation of the specific and total roughness according to ECMA-418-2
    (2nd Ed, 2022), Section 7.

    This function computes the acoustic loudness according to ECMA-418-2 section 7 method for
    stationary signals. The calculation is based on the Hearing Model (HMS) used in loudness_ecma aswell.

    Parameters
    ----------
    signal: numpy.array
        Signal time values [Pa]. The sampling frequency of the signal must be 48000 Hz.
    fs: int
        Sampling frequency [Hz].

    Returns
    -------
    R : float
        Overall roughness representative value [asper_HMS].
    R_time : numpy.ndarray
        Roughness over time [asper_HMS], size (Ntime,).
    R_specific : numpy.ndarray
        Specific roughness [asper_HMS/bark], size (Nbark, Ntime).
	    Each of the 53 elements of the list corresponds to the time-dependant specific roughness for a given bark band. 
    bark_axis : numpy.ndarray
        Corresponding bark axis, size (Nbark,).
    time_axis : numpy.ndarray
        Time axis, size (Ntime,).

    Warning
    -------
    The sampling frequency of the signal must be 48 kHz.

    See Also
    --------
    .roughness_dw : Daniel and Weber roughness computation
    .loudness_ecma : Loudness computation based on the hearing model of ECMA 418-2

    References
    ----------
    :cite:empty:`R_ecma-ECMA-418-2`

    .. bibliography::
        :keyprefix: R_ecma-

    Examples
    --------
    .. plot::
       :include-source:

        >>> from mosqito.sq_metrics import roughness_ecma
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> f=1000
        >>> fs=48000
        >>> d=1
        >>> dB=60
        >>> fmod = 70
        >>> fc = 1000
        >>> mdepth = 1
        >>> time = np.arange(0, d, 1/fs)
        >>> signal = (0.5* (1 + mdepth * (np.sin(2 * np.pi * fmod * time)))
        >>>         * np.sin(2 * np.pi * fc * time)
        >>>     )    
        >>> rms = np.sqrt(np.mean(np.power(signal, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = signal * ampl
        >>> R, R_time, R_spec, bark_axis, time_axis = roughness_ecma(stimulus, fs)
        >>> plt.step(bark_axis, R_spec)
        >>> plt.xlabel("Bark axis [Bark]")
        >>> plt.ylabel("Specific roughness [Asper/Bark]")
        >>> plt.title("Roughness = " + f"{R:.2f}" + " [Asper]")
    """

    # Check on the sampling frequency
    if fs != 48000:
        print(
            "[Warning] Signal resampled to 48 kHz fulfill the standard requirements and allow calculation."
        )
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000
    
    # INITIALIZE COMPUTATION PARAMETERS
    if (show is False) & (save is False):
        plot = False
    else:
        plot = True
    # Number of critical bands and their center frequency
    CBF = 53
    center_freq = _auditory_filters_centre_freq()
    # Hop size and block size for specific loudness calculation (7.1.1)
    sb=16384
    sh=4096
    duration =  len(signal) / fs
        
    # Preprocessing 
    signal, n_new = _preprocessing(signal, sb, sh)
    # Gammatone bandpass filtering
    bandpass_signals = _band_pass_signals(signal, sb, sh)
    # Time segmentation
    block_array, time_array = _ecma_time_segmentation(bandpass_signals, sb, sh, n_new)
    time_axis = np.array(time_array)[0]
    block_array = np.asarray(block_array)
    
    # LOUDNESS COMPUTATION
    N_specific, bark_axis = _loudness_from_bandpass(block_array)
    N_specific = np.array(N_specific).T
    L = N_specific.shape[0]
    
    # ENVELOPPE CALCULATION AND DOWNSAMPLING (7.1.2)
    envelopes_ = abs(hilbert(block_array))
    # Transposition to fit with the standard writing
    envelopes = np.transpose(np.asarray(envelopes_),(1,0,2)) 
    
    if plot:
        # .........................................................................
        # Envelope and bandpass signal for one segment
        
        z = 15
        timestep_to_plot = 8
        t = np.linspace(0, (sb-1)/fs, sb)
        
        fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
        ax.plot(t, envelopes[timestep_to_plot, z, :], label='Envelope')
        ax.plot(t, block_array[z, timestep_to_plot, :], ':', label='Bandpass Signal')
        ax.set_xlim(0, 0.03)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Amplitude signal [Pa]')
        ax.set_title(f'{bark_axis[z]:1.1f} Bark ({bark2freq(bark_axis[z]):1.0f} Hz)')
        ax.legend()
        plt.tight_layout()
        if save:
            plt.savefig(save_path+'02_Bandpassed_signals_envelope.png')
        if show:
            plt.show(block=True)
        # .........................................................................
    
    # Downsampling to 1500 Hz
    sbb = 512 
    downsampling_factor = 32
    envelopes_downsampled_ = decimate(envelopes, downsampling_factor//4, axis=2)
    envelopes_downsampled = decimate(envelopes_downsampled_, 4, axis=2)
    
    if plot:
        # .........................................................................
        # Comparison of different downsampling methods
        fs_ = 1500
        t = np.linspace(0, (sb-1)/fs, sb)
        t_ = np.linspace(0, (sbb-1)/fs_, sbb)
        timestep_to_plot = 8
        z = 35
        
        # Comparison with scipy.signal.resample method   
        envelopes_resampled = resample(envelopes, int(envelopes.shape[2]/fs*fs_), axis=2)
        fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
        ax.plot(t, block_array[z, timestep_to_plot, :], ':', label='Bandpass Signal', color='C1')
        ax.plot(t, envelopes[timestep_to_plot, z, :], label='Envelope', color='C0')
        ax.plot(t_, envelopes_downsampled[timestep_to_plot, z, :], '^:', markersize=6, label='Envelope [decimated]', color='C2')
        ax.plot(t_, envelopes_resampled[timestep_to_plot, z, :], 'o--', markersize=6, label='Envelope [resampled]', color='C3')
        ax.set_xlim(0.001, 0.011)
        ax.set_ylim(-0.033, 0.033)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Amplitude signal [Pa]')
        ax.set_title(f'{bark_axis[z]:1.1f} Bark ({bark2freq(bark_axis[z]):1.0f} Hz)')
        ax.legend()
        plt.tight_layout()
        if save:
            plt.savefig(save_path+'03_Bandpassed_signals_envelope_downsampling.png')
        if show:
            plt.show()    
            
        # Comparison with true decimation approach (only keep 1 point out of 32)
        fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
        ax.plot(t, envelopes[timestep_to_plot, z, :].T, 'o-', label='Envelope [original]')
        # plot every 32nd sample in p_env for visual reference
        ax.plot(t[::32], envelopes[timestep_to_plot, z, ::32], 's-.', color='C1', label='Envelope [every 32nd sample]')
        ax.plot(t_, envelopes_downsampled[timestep_to_plot, z, :], '^:', markersize=6, color='C2', label='Envelope [decimated]')
        ax.plot(t_, envelopes_resampled[timestep_to_plot, z, :], 'o--', markersize=6, color='C3', label='Envelope [resampled]')
        ax.set_xlim(0, 0.015)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Amplitude signal [Pa]')
        ax.set_title(f'{bark_axis[z]:1.0f} Bark ({bark2freq(bark_axis[z]):1.0f} Hz)')
        ax.legend()
        plt.tight_layout()
        if save:
            plt.savefig(save_path+'03_Bandpassed_signals_envelope_decimation.png')
        if show:
            plt.show()
        # .........................................................................

    # CALCULATION OF SCALED POWER SPECTRUM (7.1.3)
    
    # Maximum loudness in each time block
    N_specific_max = np.asarray(N_specific).max(axis=1)
    
    # Hann window is precisely defined in the standard (different from numpy version)
    hann_window = _von_hann_window(sbb)
    phi_E0 = np.sum(np.power(envelopes_downsampled * hann_window,2), axis=2)
    den = N_specific_max[:,np.newaxis] * phi_E0
    
    dft = (abs(fft((envelopes_downsampled * hann_window), axis=2)[:,:,:sbb//2])/2*np.sqrt(2))**2
    scaling = np.zeros((L, CBF))
    scaling[den!=0] = np.power(N_specific[den!=0],2) / den[den!=0]
    phi_E = scaling[:, :, np.newaxis] * dft
    
    if plot:
        # .........................................................................
        # plot scaled power spectrum for one time segment
        
        timestep_to_plot = 8
        df_ = fs_/sbb
        f = np.linspace(0, fs_ - df_, sbb)[:sbb//2]
        Pspec = 20*np.log10(phi_E[timestep_to_plot, :, :sbb//2+1]+1e-10)

        plt.subplots(figsize=[5.76, 4.8]) 
        plt.pcolormesh(f, bark_axis, Pspec, vmax=np.max(Pspec), vmin=np.max(Pspec)-80)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Critical band [Bark]')
        # plt.title(f'Scaled power spectrum of envelopes')
        clb = plt.colorbar()
        clb.ax.set_title(r'$\Phi_{E}$'+'[dB]')    
        plt.tight_layout()
        if save:
            plt.savefig(save_path+'04_Scaled_envelope_power_spectra.png')
        if show:
            plt.show()
        # .........................................................................

    # NOISE REDUCTION OF THE ENVELOPES (7.1.4)
    Phi_E = _noise_reduction(phi_E)
    
    if plot:
        # .........................................................................
        # plot averaged power spectrum for one time segment
        Phi_avg = np.zeros(Phi_E.shape)
        
        # average bands {0, 1}
        Phi_avg[:, 0, :] = (Phi_E[:, 0,:]+ Phi_E[:, 1,:])/2.
        # average bands {n-1, n, n+1}    
        for z in range(1, 52):
            Phi_avg[:,z, :] = (Phi_E[:,z-1, :]+ Phi_E[:,z, :]+ Phi_E[:,z+1, :])/3.
        # average bands {51, 52}
        Phi_avg[:,52, :] = (Phi_E[:,51,:]+ Phi_E[:,52, :])/2.
        
        df_ = fs_/sbb
        f = np.linspace(0, fs_ - df_, sbb)[:sbb//2]
        
        timestep_to_plot = 8
        Pspec = 20*np.log10(Phi_avg[timestep_to_plot, :, :sbb//2+1]+1e-10)

        plt.figure(figsize=[5.76, 4.8]) 
        plt.pcolormesh(f, bark_axis, Pspec, vmax = np.max(Pspec), vmin=np.max(Pspec)-80)
        plt.title('Averaged power spectrum of envelopes')
        plt.xlabel('Freq [Hz]')
        plt.ylabel('Critical band [Bark]')
        plt.colorbar()
        plt.tight_layout()
        if save:
            plt.savefig(save_path+'05_Averaged_envelope_power_spectra.png')
        if show:
            plt.show(block=True)
            
        Pspec = 20*np.log10(Phi_E[timestep_to_plot, :, :sbb//2+1]+1e-10)
        
        plt.figure(figsize=[5.76, 4.8])
        plt.pcolormesh(f, bark_axis, Pspec,
                    vmax=np.max(Pspec), vmin=np.max(Pspec)-80)
        #plt.title(f'Scaled power spectrum of envelopes')
        plt.xlabel('Freq [Hz]')
        plt.ylabel('Critical band [Bark]')
        clb = plt.colorbar()
        clb.ax.set_title(r'$\hat{\Phi}_{E}$'+'[dB]')    
        plt.tight_layout()
        if save:
            plt.savefig(save_path+'05_Weighted_envelope_power_spectra.png')
        if show:
            plt.show(block=True)
        # .........................................................................
    
    # Critical bands characteristics for the weightings to come
    fmax = _f_max(center_freq)
    rmax = _r_max(center_freq)
    q2_high = _Q2_high(center_freq)
    q2_low = _Q2_low(center_freq)

    amplitude = np.zeros((L,CBF))
    for l in range(L):       
        for z in range(CBF):
        
            # SPECTRAL WEIGHTING (7.1.5)
            f_p, Ai = _peak_picking(Phi_E[l, z, :])                            
            N_peak = len(f_p)
            
            if N_peak == 0:
                amplitude[l,z] = 0
            else:
                Ai_tilde = np.empty(N_peak)
                for i0 in range(N_peak):
                    # Weighting of high modulation rates
                    Ai_tilde[i0] = _high_mod_rate_weighting(f_p[i0], Ai[i0], fmax[z], rmax[z], q2_high[z])         
                
                # Estimation of fundamental modulation rate
                mod_rate, A_hat = _estimate_fund_mod_rate(f_p, Ai_tilde)
                
                # Weighting of low modulation rates
                amplitude[l,z] = _low_mod_rate_weighting(mod_rate, A_hat, fmax[z], q2_low[z])

    amplitude[amplitude<0.074376]=0
    
    # TODO: OPTIONAL ENTROPY WEIGHTING (specific to ITT equipment): needs a signal of rotational speed (7.1.6)

    if plot:
        # .........................................................................
        # plot scaled peak amplitudes
        plt.figure(figsize=[5.76, 4.8])
        plt.pcolormesh(time_array[0], bark_axis, amplitude.T)
        #plt.title(f"Weighted peaks' magnitudes")
        plt.xlabel('Time [s]')
        plt.ylabel('Critical band [Bark]')
        clb = plt.colorbar()
        clb.ax.set_title(r'$A(l,z)$')    
        plt.tight_layout()
        if save:
            plt.savefig(save_path+'08_Weighted_peaks_magnitudes.png')   
        if show:
            plt.show()
        # .........................................................................

    # CALCULATION OF TIME DEPENDENT SPECIFIC ROUGHNESS (7.1.7)
    # Interpolation to 50 Hz
    amplitude_50, t_50 = _interpolation_50(amplitude, time_axis, duration)
    R_est = np.clip(amplitude_50, 0, None)
        
    if plot:
        # .........................................................................
        # select a critical band to plot
        z = 35
        plt.figure(figsize=[5.76, 4.8])
        plt.plot(time_axis, amplitude[:, z], 'o:', label='A')
        plt.plot(t_50, R_est[:, z], '^--', label='R_est')
        plt.legend()
        plt.xlabel('Time [s]')
        plt.ylabel('Roughness [estimate]')
        plt.vlines(t_50, np.min(R_est[:, z]), np.max(amplitude_50[:, z]), color='#808080',
                    linestyle='--')
        plt.grid()
        plt.xlim(0.2, 1)
        plt.title(f'{bark_axis[z]:1.1f} Bark ({bark2freq(bark_axis[z]):1.0f} Hz)')
        plt.tight_layout()
        if save:
            plt.savefig(save_path+'09_time_dependent_specific_roughness_interpolation.png')
        if show:
            plt.show()
        # .........................................................................

    # Non linear transformation 
    R_time_spec_temp = _non_linear_transform(R_est)
    # Lowpass filtering
    R_time_spec = _lowpass_filter(R_time_spec_temp)

    # CALCULATION OF REPRESENTATIVE VALUES (7.1.8)
    # CBF dependent value
    R_spec = np.mean(R_time_spec[10:,:], axis=0) 
    # Time_dependent value
    R_time = 0.5 * np.sum(R_time_spec, axis=1)
    # Single representative value
    R = np.percentile(R_time, 90)
        
    return R, R_time, R_spec, bark_axis, t_50, R_est

if __name__ == "__main__":
    
    path = "./validations/sq_metrics/roughness_ecma/"
          
    '''
    To get the exact same figures as in the paper, load the corresponding wav file:
    '''
    from scipy.io.wavfile import read
    from scipy.signal import square
    fs, signal = read(path + "/input/test_signal_internoise_2024.wav")

    fs = 48000
    duration = 1
    time = np.linspace(0,duration, int(duration*fs), endpoint=False)
    fmod = 70
    mod_signal = square(2*np.pi*fmod*time)

    fig, ax = plt.subplots(figsize=[5.76, 2.4]) 
    ax.plot(time, signal, label="Modulated signal")
    ax.plot(time, mod_signal, linewidth=1, label="Modulating square signal", color=clr[3])
    ax.set_xlim(0, 0.2)
    ax.set_xticks([0,0.05,0.1,0.15,0.2])
    ax.set_xticklabels([0,0.05,0.1,0.15,0.2])
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude signal [Pa]')
    #ax.set_title('60 dB broadband noise modulated with a 70Hz square signal')
    plt.tight_layout()
    plt.savefig(path+'\\output\\01_broadband_noise_70Hz_square_modulated_signal.png')
    #plt.clf()
    plt.show(block=True)
    
    R, R_time, R_spec, bark_axis, t_50, _ = roughness_ecma_validation_plots(signal, fs, False, True, path+'/output/')
    
    '''
    To re-generate a new test signal and get the corresponding figures:
    '''
    # Test signal generation 
    from mosqito.utils import am_broadband_noise_generator
    from scipy.signal import square
    from scipy.io.wavfile import write
    
    fs = 48000
    duration = 1
    time = np.linspace(0,duration, int(duration*fs), endpoint=False)
    fmod = 70
    mod_signal = square(2*np.pi*fmod*time)
    signal, _ = am_broadband_noise_generator(mod_signal, dB_level=60)
    write("input/new_test_signal.wav", fs, signal)

    fig, ax = plt.subplots(figsize=[5.76, 4.8]) 
    ax.plot(time, signal, label="Modulated signal")
    ax.plot(time, mod_signal, label="Modulating square signal")
    ax.set_xlim(0, 0.2)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude signal [Pa]')
    ax.set_title('60 dB broadband noise modulated with a 70Hz square signal')
    plt.tight_layout()
    #plt.savefig(path+'\\output\\01_broadband_noise_70Hz_square_modulated_signal.png')
    plt.clf()

