from mosqito.utils import am_sine_wave_generator
import matplotlib.pyplot as plt
import numpy as np
fs=48000
d=1
dB=60
fc=100
fmod=4
mdepth = 1
time = np.arange(0, d, 1/fs)
signal = am_sine_wave_generator(d, fs, fc, fmod, mdepth , dB)
plt.plot(time, signal)
plt.xlabel("Time axis [s]")
plt.ylabel("Amplitude signal [Pa]")
