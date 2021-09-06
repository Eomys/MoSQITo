# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 17:52:53 2021

@author: josem
"""

import numpy as np
import matplotlib.pyplot as plt
import pylab as pylab
import matplotlib as mpl
from scipy import signal
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

#Parameters
rho=1
fs = 48000
n = 480000
period = n/fs
time = np.linspace(0, period, n)

#Filter parameters
harmonic_order = 1     #harmonics 1, 2, 3, ...
att = 6

#White noise generation
white_noise = white_noise(rho, fs, n, mu=0)
#Pure tones generation
tone_1 = 500*np.sin(2*np.pi*1000*time)

tone_2 = 500*np.sin(2*np.pi*5000*time)

tone_3 = 500*np.sin(2*np.pi*10000*time)


#Adding the tone to the noise
noise_plus_signal = []
noise_plus_signal[0:168000] = white_noise + tone_1

noise_plus_signal[168001:384000] = white_noise + tone_2

noise_plus_signal[384001:480000] = white_noise + tone_3

#Generating tracking signal
rpm_signal = [480000]
rpm_signal[0:169000] = np.full(169001, 6000)
rpm_signal[169001:385000] = np.full(215999, 30000)
rpm_signal[385001:480000] = np.full(95999, 60000)

l_rpm=len(rpm_signal)
t_rpm = np.arange(0, l_rpm)/fs # Intervalo de tiempo en segundos

#Filtering signal

original_signal, filtered_signal_fir, Fs = variant_filter(
    noise_plus_signal, rpm_signal,'fir', harmonic_order, att
)
original_signal, filtered_signal_iir, Fs = variant_filter(
    noise_plus_signal, rpm_signal,'iir', harmonic_order, att
)

#Scale both signals to integers to write a wav file
scale = np.max([np.max(np.abs(noise_plus_signal)), np.max(np.abs(filtered_signal_fir))])
scaled_o = np.int16(original_signal / scale * 32767)
scaled_fir = np.int16(filtered_signal_fir / scale * 32767)
scaled_iir = np.int16(filtered_signal_iir / scale * 32767)

write('tones_test_signal.wav', Fs, scaled_o)
write('FIR_filtered_tones_test_signal.wav', Fs, scaled_fir)
write('IIR_filtered_tones_test_signal.wav', Fs, scaled_iir)

#Plotting results

#Plot Spectrogram of the noise and signals
NFFT = 4096
noverlap = NFFT/2
vmin = 20*np.log10(np.max(noise_plus_signal)) - 70

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

norm = mpl.colors.Normalize(vmin=-25, vmax=30)
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
    filtered_signal_fir, 
    NFFT=NFFT,
    Fs=Fs,
    vmin=vmin, 
    noverlap=noverlap,
    cmap = plt.cm.jet, 
    window=pylab.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('Filtered signal FIR')
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

#Plot Spectrogram filtered signal IIR
ax1 = plt.subplot(gs[0])
pxx,  freq, t, cax = plt.specgram(
    filtered_signal_iir, 
    NFFT=NFFT,
    Fs=Fs,
    vmin=vmin,
    noverlap=noverlap,
    cmap = plt.cm.jet, 
    window=pylab.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('Filtered signal IIR')
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