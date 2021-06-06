# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 17:52:53 2021

@author: josem
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pylab as pylab
import scipy.signal as sig
from scipy.signal import chirp
from matplotlib import gridspec
from scipy.io.wavfile import write
from mosqito.functions.variant_filter.variant_filter import variant_filter


#White noise definition
#Parameters:
#   rhp - spectral noise density unit/SQRT(Hz)
#   sr  - sample rate
#   n   - no of points
#   mu  - mean value, optional
#Returns:
#   n points of noise signal with spectral noise density of rho

def white_noise(rho, sr, n, mu=0):
    sigma = rho * np.sqrt(sr/2)
    noise = np.random.normal(mu, sigma, n)
    return noise

#Filter parameters
harmonic_order = 2     #harmonics 1, 2, 3, ...
att = 6

#Parameters
rho=1
fs = 48000
n = 480000
period = n/fs

#White noise generation
white_noise = white_noise(rho, fs, n, mu=0)

#Generating frequency signal
time = np.linspace(0, period, n)

#Acceleration ramp from 0 to 20000 Hz
freq = 80*chirp(
    time, 
    f0=20, 
    f1=20000, 
    t1=10, 
    method='linear'
) 

#Adding noise to the signal

noise_plus_signal = white_noise + freq

#Tracking signal
f = 20 + time*1000

rpm_signal = [len(white_noise)]

rpm_signal = f*6


l_rpm=len(rpm_signal)
t_rpm = np.arange(0, l_rpm)/fs # Intervalo de tiempo en segundos

#Filtering signal

original_signal, iir_filtered_signal, Fs = variant_filter(
    noise_plus_signal, rpm_signal,'iir', harmonic_order, att
)
original_signal, fir_filtered_signal, Fs = variant_filter(
    noise_plus_signal, rpm_signal,'fir', harmonic_order, att
)

#Scale both signals to integers to write a wav file
scale = np.max([np.max(np.abs(original_signal)), np.max(np.abs(iir_filtered_signal))])
scaled_o = np.int16(original_signal / scale * 32767)
scaled_fir = np.int16(fir_filtered_signal / scale * 32767)
scaled_iir = np.int16(iir_filtered_signal / scale * 32767)

write('ramp_test_signal.wav', Fs, scaled_o)
  
write('IIR_filtered_ramp_test_signal.wav.wav', Fs, scaled_iir)
write('FIR_filtered_ramp_test_signal.wav.wav', Fs, scaled_fir)

#Plotting results

#Average spectrum of 24000 samples

plt.figure()
f, Pxx_spec_o = sig.welch(
    original_signal[120000:144000], fs, 'flattop', 1024, scaling='spectrum'
)
or_m_data = 20*np.log10(np.sqrt(Pxx_spec_o))
plt.plot(
    f, or_m_data, color = 'darkred',label="Original"
)

f, Pxx_spec_fir = sig.welch(
    fir_filtered_signal[120000:144000], fs,'flattop', 1024, scaling='spectrum'
)
fir_m_data = 20*np.log10(np.sqrt(Pxx_spec_fir))
plt.plot(
    f, fir_m_data, color = 'darkblue', linestyle='--', label="FIR"
)

f, Pxx_spec_iir = sig.welch(
    iir_filtered_signal[120000:144000], fs,'flattop', 1024, scaling='spectrum'
)
iir_m_data = 20*np.log10(np.sqrt(Pxx_spec_iir))
plt.plot(
    f, iir_m_data, color='darkgreen', linestyle='--', label="IIR"
)

plt.xlabel('Frequency [Hz]')
plt.ylabel('dBV')
plt.title('Spectrum')
plt.legend()
plt.show()

#Plot Spectrogram of the noise and signals
NFFT = 4096
noverlap = NFFT/2
vmin = 20*np.log10(np.max(noise_plus_signal)) - 60

#Set height ratios for subplots
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

ax1 = plt.subplot(gs[0])
plt.specgram(
    noise_plus_signal, 
    NFFT=NFFT,
    Fs=fs,
    vmin=vmin, 
    noverlap=noverlap,
    cmap = plt.cm.jet, 
    window=pylab.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('Original Signal')
plt.axis([0,10,0,20000])
ax1.tick_params(axis='x', direction='in')

ax2 = plt.subplot(gs[1], sharex=ax1)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.plot(t_rpm, rpm_signal)
plt.xlabel('Time [s]')
plt.ylabel('RPM')

plt.subplots_adjust(bottom=0.1, right=0.94, top=0.9, hspace=0.05)

norm = mpl.colors.Normalize(vmin=-10, vmax=20)
cax = plt.axes([0.95, 0.38, 0.025, 0.52])
plt.colorbar(
    mpl.cm.ScalarMappable(
        cmap = plt.cm.jet, 
        norm=norm
    ),
    cax=cax
).set_label('PSD [dB/Hz]', labelpad=-20, y=1.1, rotation=0)

plt.show()

#Plot Spectrogram filtered signal IIR
ax1 = plt.subplot(gs[0])
pxx,  freq, t, cax = plt.specgram(
    iir_filtered_signal, 
    NFFT=NFFT,
    Fs=Fs,
    vmin=vmin, 
    noverlap=noverlap,
    cmap = plt.cm.jet, 
    window=pylab.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('IIR Filtered signal')
plt.axis([0,10,0,20000])
ax1.tick_params(axis='x', direction='in')

ax2 = plt.subplot(gs[1], sharex=ax1)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.plot(t_rpm, rpm_signal)
plt.xlabel('Time [s]')
plt.ylabel('RPM')

plt.subplots_adjust(bottom=0.1, right=0.94, top=0.9, hspace=0.05)

cax = plt.axes([0.95, 0.38, 0.025, 0.52])
plt.colorbar(
    mpl.cm.ScalarMappable(
        cmap = plt.cm.jet, 
        norm=norm
    ),
    cax=cax
).set_label('PSD [dB/Hz]', labelpad=-20, y=1.1, rotation=0)

plt.show()

#Plot Spectrogram filtered signal FIR
ax1 = plt.subplot(gs[0])
pxx,  freq, t, cax = plt.specgram(
    fir_filtered_signal, 
    NFFT=NFFT,
    Fs=Fs,
    vmin=vmin, 
    noverlap=noverlap,
    cmap = plt.cm.jet, 
    window=pylab.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('FIR Filtered signal')
plt.axis([0,10,0,20000])
ax1.tick_params(axis='x', direction='in')

ax2 = plt.subplot(gs[1], sharex=ax1)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.plot(t_rpm, rpm_signal)
plt.xlabel('Time [s]')
plt.ylabel('RPM')

plt.subplots_adjust(bottom=0.1, right=0.94, top=0.9, hspace=0.05)

cax = plt.axes([0.95, 0.38, 0.025, 0.52])
plt.colorbar(
    mpl.cm.ScalarMappable(
        cmap = plt.cm.jet, 
        norm=norm
    ),
    cax=cax
).set_label('PSD [dB/Hz]', labelpad=-20, y=1.1, rotation=0)

plt.show()