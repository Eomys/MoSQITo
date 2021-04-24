# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 12:28:15 2020

@author: josem
"""

import scipy.signal as sig
from mosqito.functions.shared.load import load

#FIR filter definition
# Required input definitions are as follows;
# data:   The data to be filtered
# fs:     Sampling frecuency
# fc:   The centerline frequency to be filtered
# band:   The bandwidth around the centerline frequency that you wish to filter

def fir_notch_filter(data, fs, fc, band):
    #Order of the FIR filter
    numtaps = 999
    nyq = fs / 2    
   
    #Lower and upper filter cut-off frequencies are determined
    if fc < band / 2:
        band = fc / 2 
        low = (fc - band / 2) / nyq
        high = (fc + band / 2) / nyq
    else:
        low = (fc - band / 2) / nyq
        high = (fc + band / 2) / nyq
    
    #The coefficients of a lowpass and a highpass filters are obtained, using Hamming window
    h_l = sig.firwin(
        numtaps,low, window = 'blackman', pass_zero='lowpass'
    )
    h_h = sig.firwin(
        numtaps,high, window = 'blackman', pass_zero='highpass'
    )

    #Filters the data applying the obtained coefficients
    filtered_data = sig.filtfilt(h_l, 1, data, padlen=0) + sig.filtfilt(h_h, 1, data, padlen=0)

    return filtered_data

#IIR filter definition
# Required input defintions are as follows;
# data:   The data to be filtered
# fs:     Sampling frecuency
# fc:   The centerline frequency to be filtered
# band:   The bandwidth around the centerline frequency that you wish to filter

def iir_notch_filter(data, fs, fc, band):
   #Determines the quality factor
    Q = fc / band  
    
    #The coefficients of a band remover filter are obtained
    b, a = sig.iirnotch(fc, Q, fs = fs)
    
    #Filters the data applying the obtained coefficients
    filtered_data = sig.filtfilt(b, a, data, padlen=0)
    
    return filtered_data

#Variant filter definition
# Required input defintions are as follows;
# signal:     Signal to be filtered
# track:   Signal to track the harmonics
# ftype:   Type of filter. 'FIR' or 'IIR'
# harmonic_order:   Order of the harmonic to filter

def variant_filter(original_signal, signal_tracking, ftype, harmonic_order, att):
    #Load original and tracking data
    if(isinstance(signal_tracking, str)):
        signal_tracking, fs = load(False, signal_tracking, calib = 1)
    
    if(isinstance(original_signal, str)):
        original_signal, fs = load(False, original_signal, calib = 2 * 2**0.5 )   
    
    if not(isinstance(signal_tracking, str) or isinstance(original_signal, str)):
        fs = 48000
    
    #Band selector
    if(ftype == 'fir'):
        if(att == 3):
            band = 25     #Atenuation = 3 dB (FIR)
        if (att == 6):
            band = 140  #Atenuation = 6 dB (FIR and IIR)
        if(att == 9):
            band = 330    #Atenuation = 9 dB (FIR and IIR)
        if(att == 12):
            band = 600   #Atenuation = 12 dB (FIR)
    if(ftype == 'iir'):
        if(att == 3):
            band = 55    #Atenuation = 3 dB (IIR)
        if(att == 6):
            band = 160  #Atenuation = 6 dB (FIR and IIR)
        if(att == 9):
            band = 330    #Atenuation = 9 dB (FIR and IIR)
        if(att == 12):
            band = 500   #Atenuation = 12 dB (IIR)
                
    i = int(fs / 16)    #Segment size
    j = 0               
    h = 2*int(fs / 64)    #Segment size to overlap to avoid cuts
    filtered_signal = []
    
    while j < len(signal_tracking):
        
        #Value of RPM
        rpm = signal_tracking[j]
        
        #The center frequency is calculated
        if(rpm == 0):
            fc = 1
        else: fc = (harmonic_order * rpm) / 6
        
        #The filter is applied
        if ftype == 'fir':   
            filtered_signal[j:i] = fir_notch_filter(original_signal[j:i], fs, fc, band)
                      
        if ftype == 'iir':
            filtered_signal[j:i] = iir_notch_filter(original_signal[j:i], fs, fc, band) 
            
        j = i - h
        i = int(j + fs / 16)
    
    return original_signal, filtered_signal, fs