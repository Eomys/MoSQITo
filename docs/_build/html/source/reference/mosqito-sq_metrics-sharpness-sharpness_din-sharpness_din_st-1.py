from mosqito.sq_metrics import sharpness_din_st
import matplotlib.pyplot as plt
import numpy as np
f=1000
fs=48000
d=0.2
dB=60
time = np.arange(0, d, 1/fs)
stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
S = sharpness_din_st(stimulus, fs=fs)
plt.plot(time, stimulus)
plt.xlim(0, 0.05)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude [Pa]")
plt.title("Sharpness = " + f"{S:.2f}" + " [Acum]")
