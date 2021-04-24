# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 12:28:15 2020

@author: josem
"""

import numpy as np
import matplotlib as mpl
import scipy.signal as sig
import pylab as plt
from mosqito.functions.shared.load import load
from matplotlib import gridspec
from scipy.io.wavfile import write
from mosqito.functions.variant_filter.variant_filter import variant_filter

#Filter parameters
harmonic_order = 2     #harmonics 1, 2, 3, ...
att = 6

signal = "mosqito/tests/variant_filter/signals/RUN5_RunUp_60s_Track1_Rec0.UFF"
track = "mosqito/tests/variant_filter/signals/RUN5_RunUp_60s_RPM-profile_Rec0.UFF"

#Aplication of the variant_filter function
original_signal, fir_filtered_signal, Fs = variant_filter(
        signal, track,'fir', harmonic_order, att
)
original_signal, iir_filtered_signal, Fs = variant_filter(
        signal, track,'iir', harmonic_order, att
)

"""
#Playback of original and filtered signal
sd.play(original_signal, Fs)
time.sleep(40)
sd.play(filtered_signal, Fs)
"""

#Scale both signals to integers to write a wav file
scale = np.max([np.max(np.abs(original_signal)), np.max(np.abs(iir_filtered_signal))])
scaled_o = np.int16(original_signal / scale * 32767)
scaled_fir = np.int16(fir_filtered_signal / scale * 32767)
scaled_iir = np.int16(iir_filtered_signal / scale * 32767)

write('motor_signal.wav', Fs, scaled_o)
write('FIR_filtered_motor_signal_'+str(harmonic_order)+' harmonic.wav', Fs, scaled_fir)
write('IIR_filtered_motor_signal_'+str(harmonic_order)+' harmonic.wav', Fs, scaled_iir)

#RPM signal
rpm_signal, fs = load(False, track, calib = 1)
l_rpm=len(rpm_signal)
t_rpm = np.arange(0, l_rpm)/ fs # Time interval in seconds

#♣Data recopilation
f, Pxx_spec = sig.welch(
    original_signal[1200000:1224000], fs, 'flattop', 1024, scaling='spectrum'
)
plt.figure()
axes = plt.axes()
axes.set_xlim([0,3000])
plt.semilogy(f, np.sqrt(Pxx_spec), color = 'darkred')
plt.xlabel('frequency [Hz]')
plt.ylabel('Linear spectrum [V RMS]')

f, Pxx_spec = sig.welch(
    fir_filtered_signal[1200000:1224000], fs,'flattop', 1024, scaling='spectrum'
)
plt.semilogy(f, np.sqrt(Pxx_spec), color = 'darkblue', linestyle='--')
plt.xlabel('frequency [Hz]')
plt.ylabel('Linear spectrum [V RMS]')

f, Pxx_spec = sig.welch(
    iir_filtered_signal[1200000:1224000], fs,'flattop', 1024, scaling='spectrum'
)
plt.semilogy(f, np.sqrt(Pxx_spec), color='darkgreen', linestyle='--')
plt.xlabel('frequency [Hz]')
plt.ylabel('Linear spectrum [V RMS]')
plt.title('Power Spectrum')
plt.show()

#Plots

#Plot Spectrogram original signal
NFFT = 4096
noverlap = NFFT / 2
vmin = 20*np.log10(np.max(original_signal)) - 70

#Set height ratios for subplots
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

ax1 = plt.subplot(gs[0])
pxx,  freq, t, cax = plt.specgram(
    original_signal, 
    NFFT=NFFT,                                 
    Fs=Fs,
    vmin=vmin, 
    noverlap=noverlap,
    cmap = plt.cm.jet, 
    window=plt.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('Original Signal')
plt.axis([0,37,0,3000])
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
    mpl.cm.ScalarMappable(cmap = plt.cm.jet, norm=norm),
    cax=cax).set_label('PSD [dB/Hz]', labelpad=-20, y=1.1, rotation=0)

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
    window=plt.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('FIR Filtered signal')
plt.axis([0,37 ,0,3000])
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
    window=plt.window_none
)
plt.ylabel('Frequency [Hz]')
plt.title('IIR Filtered signal')
plt.axis([0,37 ,0,3000])
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

"""
#Plot Phase of a band of 5Hz between 995Hz and 1000Hz
ax3 = plt.subplot(2, 1, 1)
plt.angle_spectrum(original_signal, Fs = Fs)
plt.ylabel('Phase [Rad]')
plt.xlabel('Frequency [Hz]')
plt.axis([995, 1000, -3.2, 3.2])
plt.title('Original Signal Phase')

ax4 = plt.subplot(2, 1, 2)
plt.angle_spectrum(filtered_signal, Fs = Fs)
plt.ylabel('Phase [Rad]')
plt.xlabel('Frequency [Hz]')
plt.axis([995, 1000, -3.2, 3.2])
plt.title('Filtered Signal Phase')

plt.tight_layout()
plt.show()
"""