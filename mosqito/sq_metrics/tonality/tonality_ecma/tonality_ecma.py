from numpy import empty, zeros, pi, sum, linspace, ones, array, transpose, power, arange, cos, sin, sqrt, logical_and, zeros
from numpy.fft import fft, ifft
import numpy as np

# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._band_pass_signals import _rectified_band_pass_signals

from mosqito.sq_metrics.loudness.loudness_ecma._nonlinearity import _nonlinearity

# Data import
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_ecma_data import ltq_z
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_from_bandpass import _loudness_from_bandpass
from mosqito.sq_metrics.loudness.loudness_ecma._auditory_filters_centre_freq import _auditory_filters_centre_freq

def tonality_ecma(signal):
    """Calculation of the tonality according to ECMA-418-2 section 6

    Parameters
    ----------
    signal: numpy.array
        time signal values in 'Pa'. The sampling frequency of the signal must be 48000 Hz.
    sb: int or list of int
        block size.
    sh: int or list of int
        Hop size.
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
    CBF = 53
    epsilon = 10e-12
    
    # Hop size and block size for specific loudness calculation (table 4)
    Z = linspace(0.5, 26.5, num=53, endpoint=True)
    sb = empty(53, dtype="int")
    sh = empty(53, dtype="int")
    NB = empty(53, dtype="int")
    sb[Z <= 1.5] = 8192
    sh[Z <= 1.5] = 2048
    NB[Z <= 1.5] = 2
    sb[logical_and(Z >= 2, Z <= 8)] = 4096
    sh[logical_and(Z >= 2, Z <= 8)] = 1024
    NB[logical_and(Z >= 2, Z <= 8)] = 2
    sb[logical_and(Z >= 8.5, Z <= 12.5)] = 2048
    sh[logical_and(Z >= 8.5, Z <= 12.5)] = 512
    NB[logical_and(Z >= 8.5, Z <= 12.5)] = 1
    sb[Z >= 13] = 1024
    sh[Z >= 13] = 256
    NB[Z >= 13] = 0
    
    block_array_rect = _rectified_band_pass_signals(signal, sb, sh)
    N_spec, _ = _loudness_from_bandpass(block_array_rect, rectify=False)
    
    ACF = empty((CBF), dtype='object')
    for z in range(CBF):
        dft = power(abs(fft(block_array_rect[z], n=2*sb[z], axis=1)),2)
        ACF_unscaled = ifft(dft).real
        L = len(N_spec[z])
        ACF[z] = np.zeros((L, sb[z]))
        
        # a = np.flip(np.cumsum(block_array_rect[z][:,int(sb[z]-np.floor(0.75*sb[z])-1):sb[z]-1], axis=1))
        # b = np.flip(np.cumsum(np.flip(block_array_rect[z][:,:sb[z]-1]), axis=1)[:,:int(0.75*sb[z])])
        
        ACF[z][:,:int(0.75*sb[z])] = ACF_unscaled[:,:int(0.75*sb[z])] / (sqrt(
            np.flip(np.cumsum(block_array_rect[z][:,int(sb[z]-np.floor(0.75*sb[z])-1):sb[z]-1], axis=1)) *
            np.flip(np.cumsum(np.flip(block_array_rect[z][:,:sb[z]-1]), axis=1)[:,:int(0.75*sb[z])])
            )+epsilon) * np.array(N_spec[z])[:,np.newaxis]
        
            
    # del ACF_unscaled, block_array_rect
    # import gc
    # gc.collect()

    # Boundary values for coming averaging
    sbb = ones(53, dtype="int") * 4096
    shh = ones(53, dtype="int") * 1024
    sbb[1:3] = 4096
    shh[1:3] = 1024
    sbb[3:5] = 8192
    shh[3:5] = 2048
    sbb[15] = 2048
    shh[15] = 512
    sbb[16:18] = 4096
    shh[16:18] = 1024
    sbb[25] = 2048
    shh[25] = 512
    idx = [1,2,3,4,15,16,17,25]
    block_array_rect_boundary = _rectified_band_pass_signals(signal, sbb, shh)
    N_spec_boundary, _ = _loudness_from_bandpass(block_array_rect_boundary, rectify=False)
    
    ACF_boundary = empty((len(idx)), dtype='object')
    for i in range(len(idx)):
        z = idx[i]
        dft = power(abs(fft(block_array_rect_boundary[z], n=2*sbb[z], axis=1)),2)
        ACF_unscaled = ifft(dft).real
        L = len(N_spec_boundary[z])
        
        ACF_boundary[i] = np.zeros((L, sbb[z]))
                
        # a = np.flip(np.cumsum(block_array_rect_boundary[idx[i]][:,int(sbb[z]-np.floor(0.75*sbb[z])-1):sbb[z]-1], axis=1))
        # b = np.flip(np.cumsum(np.flip(block_array_rect_boundary[i][:,:sbb[z]-1]), axis=1)[:,:int(0.75*sbb[z])])
                
        ACF_boundary[i][:,:int(0.75*sbb[z])] = ACF_unscaled[:,:int(0.75*sbb[z])] / (sqrt(
            np.flip(np.cumsum(block_array_rect_boundary[z][:,int(sbb[z]-np.floor(0.75*sbb[z])-1):sbb[z]-1], axis=1)) *
            np.flip(np.cumsum(np.flip(block_array_rect_boundary[z][:,:sbb[z]-1]), axis=1)[:,:int(0.75*sbb[z])])
            )+epsilon) * np.array(N_spec_boundary[z])[:,np.newaxis]
                
    ACF_av = empty((CBF), dtype='object')
    # AVERAGING OF THE SCALED ACF (6.2.3)
    ACF_av[0] = sum(np.asarray(ACF[0:2])) / 2
    ACF_av[1] = sum(np.asarray(ACF[0:3])) / 3
    ACF_av[2] = (sum(np.asarray(ACF[:3])) + sum(np.asarray(ACF_boundary[2:4]))) / 5 
    ACF_av[3] = (sum(np.asarray(ACF_boundary[0:2])) + sum(np.asarray(ACF[3:6]))) / 5 
    ACF_av[4] = (np.asarray(ACF_boundary[1]) + sum(np.asarray(ACF[3:7]))) / 5 
    ACF_av[14] = (sum(np.asarray(ACF[12:16])) + np.asarray(ACF_boundary[5]) )/ 5 
    ACF_av[15] = (sum(np.asarray(ACF[13:16])) + sum(np.asarray(ACF_boundary[5:7]))) / 5 
    ACF_av[16] = (np.asarray(ACF_boundary[4]) + sum(np.asarray(ACF[16:18]))) / 3
    ACF_av[24] = sum(np.asarray(ACF[23:25]) + sum(np.asarray(ACF_boundary[7]))) / 3
    
    for z in range(5,14):
        ACF_av[z] = sum(np.asarray(ACF[z-NB[z]:z+NB[z]+1])) / (2*NB[z]+1)
    for z in range(17,24):
        ACF_av[z] = sum(np.asarray(ACF[z-NB[z]:z+NB[z]+1])) / (2*NB[z]+1)
    for z in range(25,53):
        ACF_av[z] = sum(np.asarray(ACF[z-NB[z]:z+NB[z]+1])) / (2*NB[z]+1)

    
    
    
    # APPLICATION OF ACF WINDOW (6.2.4)
    # Bandwidth (ECMA 418-2 equation 7)
    center_freq = _auditory_filters_centre_freq()
    af_f0 = 81.9289
    c = 0.1618
    delta_f = sqrt((af_f0 ** 2) + ((c * center_freq) ** 2))
    
    # Lag times limits !!!!!! milliseconds !!!!!!
    tau_min = 0.002 
    tau_start = np.maximum(0.5/delta_f, tau_min)
    tau_end = np.maximum(4/delta_f, tau_start + 0.001)  # !! +1 millisecond

    # Indices for the calculted lag times
    m_start = (np.ceil(tau_start * fs) - 1).astype(int)
    m_end = (np.floor(tau_end * fs) - 1).astype(int)
    # Number of samples in the window
    M = m_end - m_start + 1
    
    # The window is applied to all elements of index m_start<m<m_end, 0 elsewhere
    phi_prime = np.empty((CBF), dtype="object")
    N_prime = np.empty((CBF), dtype="object")
    k_max = np.empty((CBF))
    f_tone = np.empty((CBF))
    
    for z in range(CBF):
        phi_tau = np.zeros((len(N_spec[z]), ACF_av[z].shape[1]))
        phi_tau[:,m_start[z]:m_end[z]] = ACF_av[z][:,m_start[z]:m_end[z]] - np.sum(ACF_av[z][:,m_start[z]:m_end[z]])/M[z]
        
    # ESTIMATION OF TONAL LOUDNESS (6.2.5)
        phi_prime[z] = np.fft.fft(phi_tau, n=16384, axis=1)
        
        N_prime[z] = np.minimum(4 * np.max(np.abs(phi_prime[z]), axis=1) / M[z], ACF_av[z][:,0])
        
        k_max[z] = np.argmax(phi_prime[z])    
        f_tone[z] = k_max[z] * fs / 16384
        
    # RESAMPLING TO COMMON TIME BASIS (6.2.6)

    print('pause')
    # NOISE REDUCTION (6.2.7)

    # CALCULATION OF TIME DEPENDENT SPECIFIC TONALITY (6.2.8)

    # CALCULATION OF AVERAGED SPECIFIC TONALITY (6.2.9)

    # CALCULATION OF TIME DEPENDENT TONALITY (6.2.10)
    
    return T
    
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from numpy import array
    from mosqito import load
    
    colors= ["#0069a1", "#59eb98", "#8c6dd7", "#e50a66", "#e6af00", "#69c3c5"]


    sig, fs = load(r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\tonality_tnr_pr\white_noise_tone_at_442_Hz.wav")
    
    T = tonality_ecma(sig)
    
    print('done')