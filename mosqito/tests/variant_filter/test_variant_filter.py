# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 17:16:18 2021

@author: josem
"""

# Add MoSQITo to the Python path
# import sys
# sys.path.append('..')

import time
import pylab as plt
import numpy as np
# import sounddevice as sd
from matplotlib import gridspec
from scipy.io.wavfile import write
from mosqito.functions.variant_filter.variant_filter import variant_filter
from mosqito.functions.shared.load import load

# Filter parameters
armonic_order = 1  # harmonics 1, 2, 3, ...
ftype = 1  # Filter selector: 0-->FIR, 1-->IIR
band = 40  # The bandwidth around the centerline frequency that you wish to filter
signal = "mosqito/tests/variant_filter/signals/RUN5_RunUp_60s_Track1_Rec0.UFF"
track = "mosqito/tests/variant_filter/signals/RUN5_RunUp_60s_RPM-profile_Rec0.UFF"

# Aplication of the variant_filter function
original_signal, filtered_signal, Fs = variant_filter(
    signal, track, ftype, armonic_order, band
)
"""
#Playback of original and filtered signal
sd.play(original_signal, Fs)
time.sleep(40)
sd.play(filtered_signal, Fs)
"""

# Scale both signals to integers to write a wav file
scale = np.max([np.max(np.abs(original_signal)), np.max(np.abs(filtered_signal))])
scaled_o = np.int16(original_signal / scale * 32767)
scaled_f = np.int16(filtered_signal / scale * 32767)

write("original_signal_.wav", Fs, scaled_o)
write("filtered_signal_" + str(armonic_order) + ".wav", Fs, scaled_f)

# RPM signal
rpm_signal, fs = load(False, track, calib=1)
l_rpm = len(rpm_signal)
t_rpm = np.arange(0, l_rpm) / fs  # Intervalo de tiempo en segundos

# Plots

# Plot Spectrogram original signal
NFFT = 1024
noverlap = NFFT / 2
vmin = 20 * np.log10(np.max(original_signal)) - 70

# Set height ratios for sublots
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])

ax1 = plt.subplot(gs[0])
plt.specgram(
    original_signal,
    NFFT=NFFT,
    Fs=Fs,
    vmin=vmin,
    noverlap=noverlap,
    cmap=plt.cm.jet,
    window=plt.window_none,
)
plt.ylabel("Frequency [Hz]")
plt.title("Original Signal")
plt.axis([0, 37, 0, 3000])
ax1.tick_params(axis="x", direction="in")

ax2 = plt.subplot(gs[1], sharex=ax1)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.plot(t_rpm, rpm_signal)
plt.xlabel("Time [s]")
plt.ylabel("RPM")

plt.subplots_adjust(bottom=0.1, right=0.94, top=0.9, hspace=0.05)

cax = plt.axes([0.95, 0.38, 0.025, 0.52])
plt.colorbar(cax=cax).set_label("DEP [dB/Hz]", labelpad=-20, y=1.1, rotation=0)

plt.show()

# Plot Spectrogram filtered signal
ax1 = plt.subplot(gs[0])
pxx, freq, t, cax = plt.specgram(
    filtered_signal,
    NFFT=NFFT,
    Fs=Fs,
    vmin=vmin,
    noverlap=noverlap,
    cmap=plt.cm.jet,
    window=plt.window_none,
)
plt.ylabel("Frequency [Hz]")
plt.title("Filtered signal")
plt.axis([0, 37, 0, 3000])
ax1.tick_params(axis="x", direction="in")

ax2 = plt.subplot(gs[1], sharex=ax1)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.plot(t_rpm, rpm_signal)
plt.xlabel("Time [s]")
plt.ylabel("RPM")

plt.subplots_adjust(bottom=0.1, right=0.94, top=0.9, hspace=0.05)

cax = plt.axes([0.95, 0.38, 0.025, 0.52])
plt.colorbar(cax=cax).set_label("DEP [dB/Hz]", labelpad=-20, y=1.1, rotation=0)

plt.show()
# Plot Phase of a band of 5Hz between 995Hz and 1000Hz
ax3 = plt.subplot(2, 1, 1)
plt.angle_spectrum(original_signal, Fs=Fs)
plt.ylabel("Phase [Rad]")
plt.xlabel("Frequency [Hz]")
plt.axis([995, 1000, -3.2, 3.2])
plt.title("Original Signal Phase")

ax4 = plt.subplot(2, 1, 2)
plt.angle_spectrum(filtered_signal, Fs=Fs)
plt.ylabel("Phase [Rad]")
plt.xlabel("Frequency [Hz]")
plt.axis([995, 1000, -3.2, 3.2])
plt.title("Filtered Signal Phase")

plt.tight_layout()
plt.show()
