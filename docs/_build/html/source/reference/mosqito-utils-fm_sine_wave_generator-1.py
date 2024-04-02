from mosqito.utils import fm_sine_wave_generator
import matplotlib.pyplot as plt
import numpy as np
fs=48000
d = 1
dB=60
fc=50
fmod=10
k = fc//2
time = np.arange(0, d, 1/fs)
sine_wave = np.sin(2*np.pi*fmod*time)
signal, inst_freq, f_delta, MI = fm_sine_wave_generator(fs, sine_wave, fc, k, dB, True)
plt.figure()
plt.plot(time, signal)
plt.xlabel("Time axis [s]")
plt.ylabel("Amplitude signal [Pa]")
plt.title(f'Modulation index = {MI:.1f}')
plt.figure()
plt.xlabel("Time axis [s]")
plt.ylabel("Instantaneous frequency [Hz]")
plt.title(f'Max frequency deviation = {f_delta:.1f}')
plt.plot(time, inst_freq)
