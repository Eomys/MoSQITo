import numpy as np
from numpy.fft import fft
from scipy.signal import hilbert, resample, decimate
import matplotlib.pyplot as plt

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

def roughness_ecma(signal, fs):
    """Calculation of the specific and total roughness according to ECMA-418-2
    (2nd Ed, 2022).

    This function computes the acoustic loudness according to ECMA-418-2 (section 7) method for
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
    envelopes = abs(hilbert(block_array))
    # Transposition to fit with the standard writing
    envelopes = np.transpose(np.asarray(envelopes),(1,0,2)) 
    
    # Downsampling to 1500 Hz
    sbb = 512 
    downsampling_factor = 32
    envelopes_downsampled_ = decimate(envelopes, downsampling_factor//4, axis=2)
    envelopes_downsampled = decimate(envelopes_downsampled_, 4, axis=2)

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
    
    # NOISE REDUCTION OF THE ENVELOPES (7.1.4)
    Phi_E = _noise_reduction(phi_E)
    
    # Critical bands characteristics for the weightings to come
    fmax = _f_max(center_freq) # center_freq = central frequency of the band z (eq 86 section 7.1.5.2)
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

    # CALCULATION OF TIME DEPENDENT SPECIFIC ROUGHNESS (7.1.7)
    # Interpolation to 50 Hz
    amplitude_50, t_50 = _interpolation_50(amplitude, time_axis, duration)
    R_est = np.clip(amplitude_50, 0, None)
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
        
    return R, R_time, R_spec, bark_axis, t_50

if __name__ == '__main__':
    
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
        return signal * ampl

    
    
    # Fig 1
    plt.figure(figsize=[7, 4.8])
    plt.plot(signal)
    # 01_broadband_noise_70Hz_square_modulated_signal.png

    file = r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_ecma\validation_specific_roughness_ecma.xlsx"
    import matplotlib.colors as mcolors
    fc = [125,250,500,1000,2000,4000, 8000]
    fmod = [20,30,40,50,60,70,80,90,100,120,140,160,200,300,400]
    fs = 48000
    d = 1
    dB = 60
    mdepth = 1
    # fc = [1000]
    # fmod = [70]
    Ro = np.empty((len(fc), len(fmod)))
    Rref = np.empty((len(fc), len(fmod)))
    for i in range(len((fc))):
        for j in range(len((fmod))):
            carrier = fc[i]
            mod = fmod[j]
            stimulus = signal_test(fs, d, carrier, mod, dB, mdepth)
            R_time, R_spec, R = roughness_ecma(stimulus, fs, plot=True)
            Ro[i,j] = R
            #ref_spec, ref_R = ref_artemis(file, carrier, mod)
            
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