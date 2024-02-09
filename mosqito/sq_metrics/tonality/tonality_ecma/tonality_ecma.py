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
    N_spec, _ = _loudness_from_bandpass(block_array_rect)
    
    ACF = empty((CBF), dtype='object')
    for z in range(CBF):
        dft = power(abs(fft(block_array_rect[z], n=2*sb[z], axis=1)),2)
        ACF_unscaled = ifft(dft).real
        ACF[z] = []
        for m in range(int(0.75*sb[z])):
            # AUTOCORRELATION FUNCTION (6.2.2)
            ACF[z].append(ACF_unscaled[:,m] / (sqrt(np.sum(block_array_rect[z][:,:int(sb[z]-m-1)], axis=1)*np.sum(block_array_rect[z][:,m:int(sb[z]-m-1)], axis=1))+10e-12)* N_spec[z])
            
    del ACF_unscaled, block_array_rect
    import gc
    gc.collect()

    # # Boundary values for coming averaging
    # sbb = ones(53, dtype="int") * 4096
    # shh = ones(53, dtype="int") * 1024
    # sbb[1:3] = 4096
    # shh[1:3] = 1024
    # sbb[3:5] = 8192
    # shh[3:5] = 2048
    # sbb[15] = 2048
    # shh[15] = 512
    # sbb[16:18] = 4096
    # shh[16:18] = 1024
    # sbb[25] = 2048
    # shh[25] = 512
    # idx = [1,2,3,4,15,16,17,25]
    # block_array_rect_boundary = _rectified_band_pass_signals(signal, sbb, shh)
    # N_spec_boundary, _ = _loudness_from_bandpass(block_array_rect_boundary)
    
    # ACF_boundary = empty((len(idx)), dtype='object')
    # for i in range(len(idx)):
    #     z = int(Z[i])
    #     dft = power(abs(fft(block_array_rect_boundary[z], n=2*sbb[z], axis=1)),2)
    #     ACF_unscaled = ifft(dft).real
    #     ACF_boundary[i] = []
    #     for m in range(int(0.75*sbb[z])):
    #         # AUTOCORRELATION FUNCTION (6.2.2)
    #         ACF_boundary[i].append(ACF_unscaled[:,m] / (sqrt(np.sum(block_array_rect_boundary[z][:,:int(sbb[z]-m-1)], axis=1)*np.sum(block_array_rect_boundary[z][:,m:int(sbb[z]-m-1)], axis=1))+10e-12)* N_spec_boundary[z])
        
    # del ACF_unscaled, block_array_rect_boundary
    # import gc
    # gc.collect()
    
    # ACF_av = empty((CBF), dtype='object')
    # # AVERAGING OF THE SCALED ACF (6.2.3)
    # ACF_av[0] = sum(np.asarray(ACF[0:2])) / 2
    # ACF_av[1] = sum(np.asarray(ACF[0:3])) / 3
    # ACF_av[2] = (sum(np.asarray(ACF[:3])) + sum(np.asarray(ACF_boundary[2:4]))) / 5 
    # ACF_av[3] = (sum(np.asarray(ACF_boundary[0:2])) + sum(np.asarray(ACF[3:6]))) / 5 
    # ACF_av[4] = (np.asarray(ACF_boundary[1]) + sum(np.asarray(ACF[3:7]))) / 5 
    # ACF_av[14] = (sum(np.asarray(ACF[12:16])) + np.asarray(ACF_boundary[5]) )/ 5 
    # ACF_av[15] = (sum(np.asarray(ACF[13:16])) + sum(np.asarray(ACF_boundary[5:7]))) / 5 
    # ACF_av[16] = (np.asarray(ACF_boundary[4]) + sum(np.asarray(ACF[16:18]))) / 3
    # ACF_av[24] = sum(np.asarray(ACF[23:25]) + sum(np.asarray(ACF_boundary[7]))) / 3
    
    # for z in range(5,14):
    #     ACF_av[z] = sum(np.asarray(ACF[z-NB[z]:z+NB[z]+1])) / (2*NB[z]+1)
    # for z in range(17,24):
    #     ACF_av[z] = sum(np.asarray(ACF[z-NB[z]:z+NB[z]+1])) / (2*NB[z]+1)
    # for z in range(25,53):
    #     ACF_av[z] = sum(np.asarray(ACF[z-NB[z]:z+NB[z]+1])) / (2*NB[z]+1)

    ACF_av = ACF
    # APPLICATION OF ACF WINDOW (6.2.4)
    # Bandwidth (ECMA 418-2 equation 7)
    center_freq = _auditory_filters_centre_freq()
    af_f0 = 81.9289
    c = 0.1618
    delta_f = sqrt((af_f0 ** 2) + ((c * center_freq) ** 2))
    
    # Lag times limits
    tau_min = 2 #millisecond
    tau_start = np.max(0.5/delta_f, tau_min)
    tau_end = np.max(4/delta_f, tau_start+1)  # !! +1 millisecond

    # Indices for the calcultaed lag times
    m_start = np.ceil(tau_start * fs) - 1
    m_end = np.florr(tau_end * fs) - 1
    # Number of samples in the window
    M = m_end - m_start + 1
    
    # The window is applied to all elements of index m_start<m<m_end, 0 elsewhere
    phi = np.empty((CBF), dtype="object")
    for z in range(CBF):
        phi[z] = np.zeros((len(ACF_av[z])))
        phi[z][m_start:m_end] = ACF_av[z][m_start:m_end] - np.sum(ACF_av[z][m_start:m_end])/M
    # ESTIMATION OF TONAL LOUDNESS (6.2.5)

    # RESAMPLING TO COMMON TIME BASIS (6.2.6)

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