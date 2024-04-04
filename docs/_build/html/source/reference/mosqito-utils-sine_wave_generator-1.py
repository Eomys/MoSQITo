from mosqito.utils import sine_wave_generator
import matplotlib.pyplot as plt
import numpy as np
fs = 48000
duration = 1
freq = 10
dB = 60
signal, time = sine_wave_generator(fs, duration, freq, dB)
plt.plot(time, signal)
plt.xlabel("Time axis [s]")
plt.ylabel("Amplitude signal [Pa]")
