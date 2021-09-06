# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 12:28:15 2020

@author: josem
"""

import numpy as np
import pylab as plt
import matplotlib as mpl
import pylab as pylab
from scipy.signal import chirp
import scipy.signal as sig
from mosqito.functions.shared.load import load
from matplotlib import gridspec
from scipy.io.wavfile import write
from mosqito.functions.variant_filter.variant_filter import variant_filter

#Filter parameters
harmonic_order = 2     #harmonics 1, 2, 3, ...
att = 12

#Signal parameters
fs = 48000
n = 480000
period = n/fs

#Generating frequency signal
time = np.linspace(0, period, n)

#Acceleration ramp from 0 to 15000 Hz
freq = 400*chirp(
    time, 
    f0=20, 
    f1=15000, 
    t1=10, 
    method='linear'
) 

#Import data of the wav signal
signal_path = "mosqito/tests/variant_filter/signals/vocal_test_signal_voice.wav"
signal, fs = load(False, signal_path, calib = 2 * 2**0.5)
signal = np.float64(signal[:,1])

#Adding noise to the signal
signal_plus_ramp = signal[0:n] + freq

#Tracking signal
f = 20 + time*750

rpm_signal = [len(signal)]

rpm_signal = f*6

l_rpm=len(rpm_signal)
t_rpm = np.arange(0, l_rpm)/fs # Intervalo de tiempo en segundos

#Aplication of the variant_filter function
signal_plus_ramp, fir_filtered_signal, Fs = variant_filter(
    signal_plus_ramp, rpm_signal,'fir', harmonic_order, att
)
signal_plus_ramp, iir_filtered_signal, Fs = variant_filter(
    signal_plus_ramp, rpm_signal,'iir', harmonic_order, att
)

#Scale both signals to integers to write a wav file
scale = np.max([np.max(np.abs(signal_plus_ramp)), np.max(np.abs(iir_filtered_signal))])
scaled_o = np.int16(signal_plus_ramp / scale * 32767)
scaled_fir = np.int16(fir_filtered_signal / scale * 32767)
scaled_iir = np.int16(iir_filtered_signal / scale * 32767)

write('vocal_&_freq_signal.wav', Fs, scaled_o)
write('FIR_filtered_vocal_&_freq_signal.wav', Fs, scaled_fir)
write('IIR_filtered_vocal_&_freq_signal.wav', Fs, scaled_iir)

#Plotting results
    
#Average spectrum of 24000 samples
plt.figure()

f, Pxx_spec = sig.welch(
    signal_plus_ramp[400000:424000], fs, 'flattop', 1024, scaling='spectrum'
)

plt.semilogy(
    f, np.sqrt(Pxx_spec), color = 'darkred', label='original'
)

f, Pxx_spec = sig.welch(
    fir_filtered_signal[400000:424000], fs,'flattop', 1024, scaling='spectrum'
)
plt.semilogy(
    f, np.sqrt(Pxx_spec), color = 'darkblue', linestyle='-.', label='FIR'
)

f, Pxx_spec = sig.welch(
    iir_filtered_signal[400000:424000], fs,'flattop', 1024, scaling='spectrum'
)
plt.semilogy(
    f, np.sqrt(Pxx_spec), color='darkgreen', linestyle='--', label='IIR'
)

axes = plt.axes()
axes.set_xlim([0,15000])
plt.xlabel('Frequency [Hz]')
plt.ylabel('V RMS')
plt.title('Spectrum')
plt.legend()
plt.show()

#Plot Spectrogram of the noise and signals
NFFT = 4096
noverlap = NFFT/2
vmin = 20*np.log10(np.max(signal_plus_ramp)) - 90

#Set height ratios for subplots
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

ax1 = plt.subplot(gs[0])
pxx,  freq, t, cax = plt.specgram(
    signal_plus_ramp, 
    NFFT = NFFT,
    Fs = fs,
    vmin = vmin, 
    noverlap = noverlap,
    cmap = plt.cm.jet, 
    window = pylab.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('Original Signal')
plt.axis([0,10,0,15000])
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
    fir_filtered_signal, 
    NFFT=NFFT,
    Fs=Fs,
    vmin=vmin, 
    noverlap=noverlap,
    cmap = plt.cm.jet, 
    window=pylab.window_none
    )
plt.ylabel('Frequency [Hz]')
plt.title('Filtered signal FIR')
plt.axis([0,10,0,15000])
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
    iir_filtered_signal, 
    NFFT=NFFT,
    Fs=Fs,
    vmin=vmin, 
    noverlap=noverlap,
    cmap = plt.cm.jet, 
    window=pylab.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('Filtered signal IIR')
plt.axis([0,10,0,15000])
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
        cmap = plt.cm.jet
        ,norm=norm
    ),
    cax=cax
).set_label('PSD [dB/Hz]', labelpad=-20, y=1.1, rotation=0)

plt.show()