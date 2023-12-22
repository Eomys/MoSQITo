from numpy import(abs,arange,cos,pi,append,power,zeros,empty,sum,array,clip,exp,median,where,argmax,argmin,argsort,
                  delete,exp,dot,round,squeeze,sqrt,tanh,sign,diff,percentile,dot,int32,transpose,mean, linspace, vstack,
                  apply_along_axis, nan, sinh)
from numpy.fft import fft
from scipy.signal import (hilbert, resample, find_peaks)
from scipy.signal.windows import hann
import numpy as np

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
    _, N_specific, _, _ = loudness_ecma(signal, sb, sh)
    N_specific = array(transpose(N_specific))
    
    # ! ces valeurs sont déjà calculées dans la loudness
    # TODO create function loudness_from_bandpass ?
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
    R = percentile(R_time, 90)
    
    return R_spec, R_time, R



def ref_zf(fc, fmod):
    """Give the reference value for roughness by linear interpolation from the data
    given in E. Zwicker, H. Fastl: Psychoacoustics, 1990 (figure 11.2)

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer
        modulation frequency

    Output
    ------
    roughness reference values
    """

    if fc == 125:
        fm = np.array(
            [
                10.022323,
                14.848474,
                22.114502,
                24.942839,
                27.836662,
                31.386786,
                34.207447,
                36.984425,
                39.57145,
                43.002625,
                47.327793,
                51.28128,
                57.166443,
                62.746964,
                67.984726,
                75.005325,
                82.11216,
                88.736916,
                93.929695,
                101.51012,
                106.34942,
                105.52151,
                139.52977,
                179.7899,
                226.8836,
                618.8289,
            ]
        )

        R = np.array(
            [
                0.08789206,
                0.15167634,
                0.2644867,
                0.29879957,
                0.32463667,
                0.3400558,
                0.34709367,
                0.33893484,
                0.3292617,
                0.31324393,
                0.2748609,
                0.24245752,
                0.20193195,
                0.1835343,
                0.16109457,
                0.12749602,
                0.10928232,
                0.09564932,
                0.08615938,
                0.07580507,
                0.07027298,
                0.070275314,
                0.04090890,
                0.02875568,
                0.018735673,
                0.0032628998,
            ]
        )

    if fc == 250:
        fm = np.array(
            [
                9.866886,
                12.62216,
                27.420376,
                32.75557,
                38.11424,
                43.422382,
                49.456688,
                57.491714,
                65.77677,
                79.65614,
                87.87329,
                105.86451,
                129.53415,
                156.846,
                166.90276,
                164.31425,
                194.89453,
                236.00826,
                320.22247,
                996.67883,
            ]
        )

        R = np.array(
            [
                0.08789789,
                0.12193831,
                0.3708092,
                0.43099418,
                0.4755579,
                0.49039465,
                0.47503302,
                0.41672865,
                0.34165177,
                0.24969354,
                0.20581095,
                0.15120474,
                0.10822188,
                0.07665783,
                0.07013886,
                0.07014351,
                0.05207635,
                0.037664894,
                0.022104176,
                0.0031560503,
            ]
        )

    if fc == 500:
        fm = np.array(
            [
                11.409495,
                30.487507,
                33.946957,
                36.913254,
                39.927513,
                42.292023,
                46.705784,
                50.772938,
                52.936295,
                56.059425,
                59.361572,
                63.18659,
                66.90265,
                71.01811,
                74.79408,
                78.56848,
                83.38223,
                94.163795,
                113.73634,
                149.61226,
                228.0776,
                269.4534,
                343.64062,
                438.18573,
                536.22815,
                1831.6288,
            ]
        )

        R = np.array(
            [
                0.10152269,
                0.4159882,
                0.48784226,
                0.53730124,
                0.58255917,
                0.61374336,
                0.65500504,
                0.67568153,
                0.6826773,
                0.68430084,
                0.6717034,
                0.6593232,
                0.6337642,
                0.6012624,
                0.56008166,
                0.5258434,
                0.47217426,
                0.38673645,
                0.2821931,
                0.1763591,
                0.08655889,
                0.06439575,
                0.04328783,
                0.02805619,
                0.020718602,
                0.0024511195,
            ]
        )

    if fc == 1000:
        fm = np.array(
            [
                11.087001,
                13.655874,
                17.425774,
                22.323097,
                28.37367,
                34.94905,
                42.370758,
                49.96757,
                56.425716,
                63.209957,
                69.42832,
                74.194626,
                81.15967,
                87.05505,
                95.19742,
                103.28752,
                112.92756,
                137.10373,
                160.75127,
                193.66571,
                220.964,
                246.33324,
                284.3601,
                332.1115,
                402.6136,
                472.69742,
                578.35956,
                700.3975,
                2566.1887,
            ]
        )

        R = np.array(
            [
                0.10113691,
                0.13728729,
                0.19609652,
                0.27899456,
                0.39539358,
                0.5409575,
                0.7005437,
                0.8453598,
                0.9321353,
                0.98051274,
                0.99174285,
                0.9837013,
                0.9491586,
                0.90162235,
                0.80737907,
                0.7173512,
                0.6151961,
                0.44188514,
                0.34071133,
                0.25057378,
                0.19783457,
                0.16634719,
                0.13030091,
                0.10086449,
                0.07060981,
                0.05522989,
                0.03911979,
                0.02859039,
                0.0032180264,
            ]
        )

    if fc == 2000:
        fm = np.array(
            [
                9.91285,
                14.026899,
                42.67351,
                48.009727,
                51.526123,
                55.798893,
                58.02824,
                63.2473,
                68.39307,
                73.18517,
                78.91965,
                85.31508,
                94.640015,
                97.87623,
                112.84719,
                116.1008,
                134.20557,
                142.05911,
                176.54396,
                208.32822,
                247.7417,
                325.8978,
                392.00952,
                472.19678,
                560.03955,
                661.0346,
                2300.151,
            ]
        )

        R = np.array(
            [
                0.0769564,
                0.12057757,
                0.5939494,
                0.68385667,
                0.7424558,
                0.78007925,
                0.7985556,
                0.8280814,
                0.8409192,
                0.8384773,
                0.8165356,
                0.78357395,
                0.69696763,
                0.65123534,
                0.5195601,
                0.49169108,
                0.3902205,
                0.3513164,
                0.2457958,
                0.18558311,
                0.13721035,
                0.08642737,
                0.0607108,
                0.043004807,
                0.031432506,
                0.02523464,
                0.0031944455,
            ]
        )

    if fc == 4000:
        fm = np.array(
            [
                11.3765,
                15.561241,
                43.589268,
                47.646236,
                51.401146,
                56.619133,
                59.81015,
                63.843525,
                67.08531,
                70.85759,
                74.06288,
                77.41061,
                81.33141,
                87.916466,
                97.7758,
                100.33316,
                115.681206,
                119.01259,
                134.40422,
                148.2887,
                177.72102,
                205.42125,
                235.5931,
                272.31946,
                296.5826,
                330.12863,
                406.07715,
                481.70474,
                562.59235,
                1862.4557,
            ]
        )

        R = np.array(
            [
                0.07075734,
                0.10967778,
                0.4784683,
                0.52834743,
                0.5683734,
                0.6097778,
                0.6274577,
                0.6473149,
                0.6522843,
                0.6521323,
                0.6452131,
                0.6333704,
                0.62010473,
                0.57756937,
                0.51043147,
                0.48305747,
                0.38639748,
                0.36280885,
                0.29872113,
                0.2538336,
                0.18619592,
                0.1454662,
                0.11394783,
                0.08948974,
                0.07725139,
                0.06268515,
                0.04557176,
                0.03472703,
                0.026881821,
                0.003147697,
            ]
        )

    if fc == 8000:
        fm = np.array(
            [
                9.403103,
                17.80395,
                55.790886,
                61.60936,
                66.79713,
                70.92175,
                76.48056,
                82.46687,
                90.54218,
                94.376076,
                105.48482,
                109.09549,
                122.24679,
                143.51547,
                183.9545,
                219.89703,
                266.57776,
                336.44156,
                435.79315,
                561.5252,
                1394.7712,
            ]
        )

        R = np.array(
            [
                0.03535737,
                0.09006271,
                0.40631378,
                0.42686793,
                0.43575785,
                0.4356466,
                0.42647484,
                0.40776858,
                0.3738506,
                0.35563606,
                0.29824737,
                0.2837258,
                0.2342281,
                0.17965466,
                0.11587502,
                0.08544585,
                0.05986661,
                0.04003583,
                0.026355661,
                0.017170433,
                0.0031515576,
            ]
        )

    return np.interp(fmod, fm, R)


def ref_dw(fc, fmod):
    """Give the reference value for roughness by linear interpolation from the data
    given in "Psychoacoustical roughness:implementation of an optimized model"
    by Daniel and Weber in 1997

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer
        modulation frequency

    Output
    ------
    roughness reference values from the article by Daniel and Weber
    """

    if fc == 125:
        fm = np.array(
            [
                1.0355988,
                10.355987,
                11.132686,
                13.851132,
                18.511328,
                20.064724,
                24.724918,
                31.32686,
                41.423946,
                49.967636,
                57.34628,
                64.33657,
                72.10356,
                90.74434,
                79.4822,
                86.084145,
                91.909386,
                100.45307,
            ]
        )

        R = np.array(
            [
                0.0,
                0.04359673,
                0.09468665,
                0.16416894,
                0.19482289,
                0.27656674,
                0.3113079,
                0.34196186,
                0.32356948,
                0.26226157,
                0.20299728,
                0.15803815,
                0.11512262,
                0.0619891,
                0.09264305,
                0.07016349,
                0.05177112,
                0.03950954,
            ]
        )

    if fc == 250:
        fm = np.array(
            [
                0.7373272,
                3.9324117,
                9.585254,
                14.2549925,
                16.71275,
                19.907835,
                22.611366,
                23.594471,
                29.493088,
                30.47619,
                37.112137,
                41.29032,
                47.926266,
                50.13825,
                51.121353,
                53.08756,
                54.07066,
                56.774193,
                58.248848,
                62.427036,
                61.68971,
                69.308754,
                68.57143,
                71.27496,
                73.73272,
                73.97849,
                75.207375,
                79.139786,
                79.139786,
                84.792625,
                90.19969,
                97.81874,
                104.70046,
                112.31951,
                120.92166,
                129.76959,
            ]
        )

        R = np.array(
            [
                0.00432277,
                0.00576369,
                0.06340057,
                0.16138329,
                0.17435159,
                0.26945245,
                0.32132566,
                0.3443804,
                0.42651296,
                0.44668588,
                0.47694525,
                0.4668588,
                0.42651296,
                0.46253604,
                0.41210374,
                0.4020173,
                0.43948126,
                0.37463978,
                0.39193085,
                0.3631124,
                0.3429395,
                0.3040346,
                0.28242075,
                0.27521613,
                0.259366,
                0.24207492,
                0.24351585,
                0.2204611,
                0.20461094,
                0.17146975,
                0.14697406,
                0.11815562,
                0.09942363,
                0.07636888,
                0.05619597,
                0.04322766,
            ]
        )

    if fc == 500:
        fm = np.array(
            [
                7.6375403,
                15.79288,
                20.841423,
                26.666666,
                30.93851,
                34.43366,
                40.2589,
                44.919094,
                49.190937,
                51.521034,
                57.34628,
                64.33657,
                69.77346,
                74.04531,
                81.42395,
                87.63754,
                94.23948,
                102.78317,
                116.763756,
                129.57928,
                140.84143,
                149.77347,
                160.2589,
            ]
        )

        R = np.array(
            [
                0.04972752,
                0.1253406,
                0.23569483,
                0.35013625,
                0.46457765,
                0.5258856,
                0.619891,
                0.67302454,
                0.69346046,
                0.69550407,
                0.6873297,
                0.67098093,
                0.6321526,
                0.57901907,
                0.5074932,
                0.4400545,
                0.38487738,
                0.3153951,
                0.22752044,
                0.16621253,
                0.11920981,
                0.08651226,
                0.06811989,
            ]
        )

    if fc == 1000:
        fm = np.array(
            [
                0.0,
                3.884415,
                9.7237625,
                17.147604,
                29.302307,
                37.933605,
                48.504757,
                55.145306,
                55.948395,
                57.480103,
                60.618927,
                63.314735,
                65.28852,
                67.201035,
                69.55657,
                76.14433,
                77.2943,
                82.847725,
                83.352325,
                88.26008,
                89.019806,
                93.92756,
                94.4309,
                97.78904,
                99.06719,
                104.23258,
                103.963005,
                106.03293,
                109.89504,
                111.18953,
                115.05101,
                117.38172,
                119.95311,
                125.630646,
                132.60141,
                137.24963,
                144.47617,
                151.19432,
                159.97737,
            ]
        )

        R = np.array(
            [
                0.0,
                0.00211198,
                0.03450088,
                0.1382977,
                0.40437,
                0.60555416,
                0.80238307,
                0.89103884,
                0.9516347,
                0.90182984,
                0.9753813,
                0.92339617,
                0.9969634,
                0.92983717,
                0.9882475,
                0.9556905,
                0.92104256,
                0.89138556,
                0.86107534,
                0.83503467,
                0.7960629,
                0.7700222,
                0.736826,
                0.71946436,
                0.6819286,
                0.6529984,
                0.6284707,
                0.62555665,
                0.5764418,
                0.5764243,
                0.52586645,
                0.52727795,
                0.48683867,
                0.44491437,
                0.40008652,
                0.3726063,
                0.3205599,
                0.29016566,
                0.24531329,
            ]
        )

    if fc == 2000:
        fm = np.array(
            [
                0.0,
                4.4051557,
                7.5956764,
                10.048887,
                12.017292,
                15.69636,
                17.911657,
                20.366364,
                20.619616,
                25.28251,
                27.987852,
                30.20053,
                31.18548,
                34.37525,
                34.38161,
                39.782192,
                39.298134,
                42.23989,
                42.981316,
                45.18539,
                44.95683,
                46.663754,
                48.13538,
                50.358532,
                53.04068,
                55.264206,
                56.971127,
                58.68778,
                60.890354,
                62.367218,
                62.84529,
                65.06246,
                67.00842,
                68.48715,
                71.90736,
                73.62214,
                76.79096,
                79.24305,
                81.67831,
                85.10337,
                91.45038,
                93.655945,
                96.586105,
                96.33435,
                98.04801,
                106.5901,
                107.57281,
                115.62524,
                118.07209,
                120.26419,
                121.97673,
                129.54285,
                131.255,
                134.91576,
                135.15628,
                136.87106,
                144.92911,
                159.83092,
            ]
        )

        R = np.array(
            [
                0.00271003,
                0.00538277,
                0.04194128,
                0.06631085,
                0.10694477,
                0.1407891,
                0.18955104,
                0.21934068,
                0.250504,
                0.30331025,
                0.35477808,
                0.39405492,
                0.41708192,
                0.4509304,
                0.47396567,
                0.54031587,
                0.55929023,
                0.5809457,
                0.60803974,
                0.6161512,
                0.674419,
                0.65407926,
                0.66761696,
                0.74483424,
                0.71229106,
                0.7908634,
                0.7705236,
                0.7854143,
                0.78810567,
                0.8206137,
                0.779959,
                0.83549607,
                0.79482895,
                0.83411205,
                0.8164678,
                0.8245834,
                0.78255093,
                0.8028555,
                0.76218426,
                0.76215523,
                0.7119658,
                0.7254973,
                0.7051472,
                0.67940396,
                0.6834545,
                0.6088561,
                0.62375295,
                0.5478037,
                0.549138,
                0.5138889,
                0.5138744,
                0.4487694,
                0.44739988,
                0.41484842,
                0.39994115,
                0.40805677,
                0.3524327,
                0.27371538,
            ]
        )

    if fc == 4000:
        fm = np.array(
            [
                3.1950846,
                16.221199,
                23.840246,
                29.984638,
                30.230415,
                37.112137,
                37.603687,
                45.714287,
                51.85868,
                57.265743,
                63.90169,
                68.57143,
                74.47005,
                78.156685,
                82.33487,
                88.97082,
                98.064514,
                108.14132,
                115.02304,
                123.870964,
                128.78648,
                133.21045,
                143.04147,
                151.39784,
                155.08449,
                157.29646,
                160.24577,
            ]
        )

        R = np.array(
            [
                0.00432277,
                0.11383285,
                0.23054755,
                0.29538906,
                0.31123918,
                0.39337176,
                0.41066283,
                0.50864553,
                0.5907781,
                0.62680113,
                0.6426513,
                0.65273774,
                0.64841497,
                0.6440922,
                0.6152738,
                0.5720461,
                0.5158501,
                0.45677233,
                0.41210374,
                0.3631124,
                0.34149855,
                0.3184438,
                0.2795389,
                0.24495678,
                0.24783862,
                0.23919308,
                0.24063401,
            ]
        )

    if fc == 8000:
        fm = np.array(
            [
                4.6498036,
                7.1022663,
                8.569778,
                16.16957,
                23.037289,
                24.018497,
                25.735521,
                27.451048,
                30.885843,
                33.578465,
                34.319515,
                38.48526,
                40.206398,
                42.654747,
                45.355972,
                50.995964,
                52.953144,
                55.896774,
                56.631092,
                60.54957,
                61.772808,
                63.238823,
                66.18058,
                68.86871,
                70.58611,
                72.78196,
                74.744,
                78.409225,
                80.61181,
                82.31723,
                86.23272,
                87.20532,
                90.384995,
                91.11295,
                96.73499,
                100.39909,
                106.50631,
                117.26071,
                127.28154,
                137.0596,
                145.37276,
                154.66376,
                159.55597,
            ]
        )

        R = np.array(
            [
                0.0053807,
                0.02704024,
                0.0256728,
                0.08251926,
                0.14614701,
                0.15562384,
                0.17186953,
                0.18269515,
                0.21789658,
                0.22329386,
                0.24903294,
                0.27338803,
                0.30453888,
                0.31129324,
                0.3478559,
                0.3952338,
                0.39521724,
                0.42364773,
                0.42499653,
                0.43986857,
                0.4398582,
                0.4330707,
                0.4547261,
                0.44386315,
                0.46146387,
                0.43976498,
                0.4573636,
                0.44107231,
                0.4437637,
                0.4180039,
                0.42203578,
                0.40034726,
                0.39761028,
                0.3759238,
                0.35826093,
                0.3379046,
                0.30533242,
                0.2686558,
                0.23334044,
                0.20480223,
                0.18711658,
                0.1667126,
                0.16396113,
            ]
        )

    return np.interp(fmod, fm, R)


def ref_ps(fc, fmod):
    """Give the reference value for roughness by linear interpolation from the data
    obtained by the test given on Psysound github's page

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer
        modulation frequency

    Output
    ------
    reference roughness value from psysound
    """

    if fc == 250:
        x = np.arange(20, 140, 10)

        y = np.array(
            [
                0.22274093,
                0.40159333,
                0.49485818,
                0.49003562,
                0.402682,
                0.32469746,
                0.25295672,
                0.20614693,
                0.17648213,
                0.15149577,
                0.13118783,
                0.11399959,
            ]
        )

    if fc == 1000:

        x = np.arange(20, 170, 10)

        y = np.array(
            [
                0.23987818,
                0.43430352,
                0.63348603,
                0.840501,
                0.9649883,
                1.0053802,
                0.9725802,
                0.8790393,
                0.77616817,
                0.64682287,
                0.56887937,
                0.5018503,
                0.4488377,
                0.3927176,
                0.34127373,
            ]
        )

    if fc == 4000:

        x = np.arange(20, 170, 10)

        y = np.array(
            [
                0.22429857,
                0.3782322,
                0.46526212,
                0.52741647,
                0.6067358,
                0.6222046,
                0.59563285,
                0.54726654,
                0.45841187,
                0.39915878,
                0.35237116,
                0.30403143,
                0.27594423,
                0.23695582,
                0.2213363,
            ]
        )

    return np.interp(fmod, x, y)


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
    return signal / (2 * 2 ** 0.5)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from numpy import array
    freqs = _auditory_filters_centre_freq()

    colors= ["#0069a1", "#59eb98", "#8c6dd7", "#e50a66", "#e6af00", "#69c3c5"]


    ref = array([0.2340, 0.4596, 0.7007, 0.8960, 0.9768, 1.0009, 0.9185, 0.7998, 0.6840, 0.5003, 0.3748, 0.2888, 0.2309, 0.1956, 0.0910, 0.0419])
    R_ecma = zeros((3, 16))
    R_zf = zeros((3, 16))
    R_dw = zeros((3, 16))
    R_ps = zeros((3, 16))
    fc = array([250, 1000, 4000])
    fmod = array([20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 300, 400])


    fs = 44100
    d = 1
    dB = 70

    plt.figure()
    for i in range(3):
        for j in range(16):
            print("Signal n : ", i)
            signal = signal_test(fs, d, fc[i], fmod[j], dB, mdepth=1)
            _, _, R_ecma[i,j] = roughness_ecma(signal)
            R_zf[i,j] = ref_zf(fc[i], fmod[j])
            R_dw[i,j] = ref_dw(fc[i], fmod[j])
            R_ps[i,j] = ref_ps(fc[i], fmod[j])
        
    plt.figure()
    plt.plot(fmod, R_ecma[1,:])    
    plt.plot(fmod, ref)    
    plt.show(block=True)
                
    n = 12
    # Initialization
    fig, (axs1, axs2, axs3) = plt.subplots(
        3, 1, figsize=(6, 6), constrained_layout=True
    )
    axs1.plot(
        fmod[0:n], R_zf[0, 0:n], linestyle="dotted", color="black", label="Zwicker and Fastl"
    )
    axs1.plot(fmod[0:n], R_ps[0,0:n], marker="o", color=colors[0], label="Psysound")
    axs1.plot(fmod[0:n], R_dw[0,0:n], marker="s", color=colors[1], label="Daniel and Weber")
    #axs1.plot(fmod[0:n], ref[0,0:n], marker="s", color=colors[2], label="Artemis")
    axs1.plot(fmod[0:n], R_ecma[0,0:n], marker="s", color=colors[3], label="mosqito ecma")
    
    axs1.set(xlim=(0, 170), ylim=(0, 0.7))
    axs1.set_title("Carrier frequency of 250 Hz", fontsize=11)
    axs1.legend(loc="upper right", shadow=True)
    axs1.set_ylabel("Roughness [asper]")
    axs1.set_xlabel("Modulation frequency [Hz]")
    
    axs2.plot(
        fmod[0:n], R_zf[1,0:n], linestyle="dotted", color="black", label="Zwicker and Fastl"
    )
    axs2.plot(fmod[0:n], R_ps[1,0:n], marker="o", color=colors[0], label="Psysound")
    axs2.plot(fmod[0:n], R_dw[1,0:n], marker="s", color=colors[1], label="Daniel and Weber")
    axs2.plot(fmod[0:n], ref[0:n], marker="s", color=colors[2], label="Artemis")
    axs2.plot(fmod[0:n], R_ecma[1,0:n], marker="s", color=colors[3], label="mosqito ecma")
    
    axs2.set(xlim=(0, 170), ylim=(0, 1.2))
    axs2.set_title("Carrier frequency of 1000 Hz", fontsize=11)
    axs2.legend(loc="upper right", shadow=True)
    axs2.set_ylabel("Roughness [asper]")
    axs2.set_xlabel("Modulation frequency [Hz]")
    
    axs3.plot(
        fmod[0:n], R_zf[2,0:n], linestyle="dotted", color="black", label="Zwicker and Fastl"
    )
    axs3.plot(fmod[0:n], R_ps[2,0:n], marker="o", color=colors[0], label="Psysound")
    axs3.plot(fmod[0:n], R_dw[2,0:n], marker="s", color=colors[1], label="Daniel and Weber")
    #axs3.plot(fmod[0:n], ref[2,0:n], marker="s", color=colors[2], label="Artemis")
    axs3.plot(fmod[0:n], R_ecma[2,0:n], marker="s", color=colors[3], label="mosqito ecma")
    
    axs3.set(xlim=(0, 170), ylim=(0, 0.8))
    axs3.set_title("Carrier frequency of 4000 Hz", fontsize=11)
    axs3.legend(loc="upper right", shadow=True)
    axs3.set_ylabel("Roughness [asper]")
    axs3.set_xlabel("Modulation frequency [Hz]")
    
    plt.show(block=True)

    import matplotlib.pyplot as plt
    from numpy import array
    freqs = _auditory_filters_centre_freq()

    path = [r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod20.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod30.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod40.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod50.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod60.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod70.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod80.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod90.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod100.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod120.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod140.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod160.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod180.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod200.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod300.wav",
            r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod400.wav",
            ]
    ref = array([0.2340, 0.4596, 0.7007, 0.8960, 0.9768, 1.0009, 0.9185, 0.7998, 0.6840, 0.5003, 0.3748, 0.2888, 0.2309, 0.1956, 0.0910, 0.0419])
    R = zeros((16))
    plt.figure()
    dB = 57.5
    for i in range(16):
        print("Signal n : ", i)
        signal, fs = load(path[i])
        R_spec, R_time, R[i] = roughness_ecma(signal[:int(len(signal)/2)])

    x = [20,30,40,50,60,70,80,90,100,120,140,160,180,200,300,400]
    plt.figure()
    plt.plot(x, R, 'blue', marker='o')
    plt.plot(x, ref, 'red', marker='o', linestyle='--', label='référence Artemis')
    plt.title('Global roughness for 16 different signals')
    plt.xlabel('Modulation frequency [Bark]')
    plt.ylabel('Roughness [Asper]')
    plt.grid(visible=True)
    plt.legend()
    plt.show(block=True)

    x_ref = [485.20056, 544.18116, 603.69901, 673.39525, 738.9283, 815.28005, 899.52143, 981.68271, 1077.21749, 1175.60934, 1290.01601, 1400.1749, 1519.74064, 1658.55205, 1810.04311, 1964.60889, 2132.37358, 2314.46426, 2525.86485, 2726.6215]
    y_ref = [0, 0.00781, 0.02344, 0.05468, 0.11978, 0.2285, 0.3255, 0.36976, 0.29881, 0.21418, 0.1328, 0.08137, 0.05013, 0.0306, 0.01888, 0.01042, 0.00586, 0.00325, 0.0013, 0.00065]
    
    plt.figure()
    signal, fs = load(r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_dw\input\Test_signal_fc1000_fmod70.wav")
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