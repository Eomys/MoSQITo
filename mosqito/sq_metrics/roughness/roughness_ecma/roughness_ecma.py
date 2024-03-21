from numpy import abs, array, asarray, mean, transpose, newaxis, power, zeros, empty, clip, percentile, sqrt
from numpy.fft import fft
from scipy.signal import hilbert, resample, decimate

# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._preprocessing import _preprocessing
from mosqito.sq_metrics.loudness.loudness_ecma._band_pass_signals import _band_pass_signals
from mosqito.sq_metrics.loudness.loudness_ecma._ecma_time_segmentation import _ecma_time_segmentation
from mosqito.sq_metrics.loudness.loudness_ecma._auditory_filters_centre_freq import _auditory_filters_centre_freq
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_from_bandpass import _loudness_from_bandpass
from mosqito.sq_metrics.roughness.roughness_ecma._weighting import f_max, r_max, Q2_high, Q2_low, _high_mod_rate_weighting, _low_mod_rate_weighting
from mosqito.sq_metrics.roughness.roughness_ecma._estimate_fund_mod_rate import _estimate_fund_mod_rate
from mosqito.sq_metrics.roughness.roughness_ecma._peak_picking import _peak_picking
from mosqito.sq_metrics.roughness.roughness_ecma._von_hann_window import _von_hann_window
from mosqito.sq_metrics.roughness.roughness_ecma._noise_reduction import _noise_reduction
from mosqito.sq_metrics.roughness.roughness_ecma._interpolation_50 import _interpolation_50
from mosqito.sq_metrics.roughness.roughness_ecma._non_linear_transform import _non_linear_transform


def roughness_ecma(signal, fs, plot=False):
    """Calculation of the roughness according to ECMA-418-2 section 7

    Parameters
    ----------
    signal: numpy.array
        time signal values in 'Pa'. The sampling frequency of the signal must be 48000 Hz.
    fs: float
        Sampling frequency in [Hz]
        
    Returns
    -------
    R : float
        Overall roughness representative value [asper].
    R_time : numpy.ndarray
        Roughness over time [asper], size (Ntime,).
    R_specific : numpy.ndarray
        Specific roughness [asper/bark], size (Nbark, Ntime).
    bark_axis : numpy.ndarray
        Bark axis, size (Nbark,).
    time_axis : numpy.ndarray
        Time axis, size (Ntime,).
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
        
    # Preprocessing 
    signal, n_new = _preprocessing(signal, sb, sh)
    # Gammatone bandpass filtering
    bandpass_signals = _band_pass_signals(signal, sb, sh)
    # Time segmentation
    block_array, time_array = _ecma_time_segmentation(bandpass_signals, sb, sh, n_new)
    time_axis = array(time_array)[0]
    block_array = asarray(block_array)
    
    # LOUDNESS COMPUTATION
    N_specific, bark_axis = _loudness_from_bandpass(block_array)
    N_specific = array(N_specific).T
    L = N_specific.shape[0]
    
    # ENVELOPPE CALCULATION AND DOWNSAMPLING (7.1.2)
    envelopes = abs(hilbert(block_array))
    # Transposition to get to fot with the standard writing
    envelopes = transpose(asarray(envelopes),(1,0,2)) 
    
    # Downsampling to 1500 Hz
    sbb = 512 

    downsampling_factor = 32
    envelopes_downsampled_ = decimate(envelopes, downsampling_factor//4, axis=2)
    envelopes_downsampled = decimate(envelopes_downsampled_, 4, axis=2)

    # CALCULATION OF SCALED POWER SPECTRUM (7.1.3)
    N_specific_max = asarray(N_specific).max(axis=1)
    
    # Hann window is precisely defined in the standard (different from numpy version)
    hann_window = _von_hann_window(sbb)
    phi_e0 = sum(power(envelopes_downsampled * hann_window,2), axis=2)
    den = N_specific_max[:,newaxis] * phi_e0
    
    #dft = power(abs(rfft((envelopes_downsampled * hann_window), n=sbb-1, axis=2))/2,2)
    dft = (abs(fft((envelopes_downsampled * hann_window), axis=2)[:,:,:sbb//2])/2*sqrt(2))**2
    scaling = zeros((L, CBF))
    scaling[den!=0] = power(N_specific[den!=0],2) / den[den!=0]
    spectrum = scaling[:, :, newaxis] * dft
    
    # NOISE REDUCTION OF THE ENVELOPES (7.1.4)
    Phi_E = _noise_reduction(spectrum, plot)
    
    # Critical bands characteristics for the weightings to come
    fmax = f_max(center_freq) # center_freq = fréquence centrale de la bande z (eq 86 clause 7.1.5.2)
    rmax = r_max(center_freq)
    q2_high = Q2_high(center_freq)
    q2_low = Q2_low(center_freq)

    amplitude = zeros((L,CBF))
    for l in range(L):       
        for z in range(CBF):
        
            # SPECTRAL WEIGHTING (7.1.5)
            f_p, Ai = _peak_picking(Phi_E[l, z, :])       
                         
            N_peak = len(f_p)
            
            if N_peak == 0:
                amplitude[l,z] = 0
            else:
                Ai_tilde = empty(N_peak)
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
    amplitude_50, N50 = _interpolation_50(amplitude, time_axis, duration)
    R_est = clip(amplitude_50, 0, None)

    # Non linear transformation ()
    R_time_spec = _non_linear_transform(R_est, CBF, N50)

    # CALCULATION OF REPRESENTATIVE VALUES (7.1.8)
    # CBF dependent value
    R_spec = mean(R_time_spec[10:,:], axis=0) 
    # Time_dependent value
    R_time = 0.5 * sum(R_time_spec, axis=1)
    # Single value
    R = percentile(R_time, 90)
        
    return R, R_time, R_spec, bark_axis, time_axis

