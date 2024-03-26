from mosqito.sq_metrics import loudness_zwst_perseg
import matplotlib.pyplot as plt
import numpy as np
fs=48000
d=1
dB=60
time = np.arange(0, d, 1/fs)
f = np.linspace(1000,5000, len(time))
stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
N, N_spec, bark_axis, time_axis = loudness_zwst_perseg(stimulus, fs=fs)
plt.plot(time_axis, N)
plt.xlabel("Time [s]")
plt.ylabel("Loudness [Sone]")
