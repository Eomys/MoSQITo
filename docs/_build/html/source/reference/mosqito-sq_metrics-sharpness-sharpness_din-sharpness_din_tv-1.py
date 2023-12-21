from mosqito.sq_metrics import sharpness_din_tv
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
S, time_axis = sharpness_din_tv(stimulus, fs=fs, skip=0.1)
plt.plot(time_axis, S)
plt.xlabel("Time [s]")
plt.ylabel("Sharpness [Acum]")
