from mosqito.utils import am_broadband_noise_generator
import matplotlib.pyplot as plt
import numpy as np
fs=48000
d = 1
dB=60
fmod=4
mdepth = 1
time = np.arange(0, d, 1/fs)
sine_wave = np.sin(2*np.pi*fmod*time)
signal, MI = am_broadband_noise_generator(sine_wave, dB, True)
plt.plot(time, signal)
plt.xlabel("Time axis [s]")
plt.ylabel("Amplitude signal [Pa]")
plt.title(f'Modulation index = {MI}')
