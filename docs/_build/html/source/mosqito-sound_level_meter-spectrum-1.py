from mosqito.sound_level_meter import spectrum
import matplotlib.pyplot as plt
import numpy as np
fs=48000
d=0.2
dB=60
time = np.arange(0, d, 1/fs)
f = 1000
stimulus = 1 + 0.5*np.sin(2 * np.pi * f * time) + 0.1*np.sin(20 * np.pi * f * time)
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
spec_db, freq_axis = spectrum(stimulus, fs, db=True)
plt.step(freq_axis, spec_db)
plt.xlabel("Center frequency [Hz]")
plt.ylabel("Amplitude [dB]")
