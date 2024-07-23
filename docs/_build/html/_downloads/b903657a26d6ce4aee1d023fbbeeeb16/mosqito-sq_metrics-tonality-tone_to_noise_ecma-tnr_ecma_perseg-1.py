import numpy as np
import matplotlib.pyplot as plt
from mosqito.sq_metrics import tnr_ecma_perseg
fs = 48000
d = 2
dB = 60
time = np.arange(0, d, 1/fs)
f1 = 1000
f2 = np.zeros((len(time)))
f2[len(time)//2:] = 1500
stimulus = 2 * np.sin(2 * np.pi * f1 * time) + np.sin(2 * np.pi * f2 * time)+ np.random.normal(0,0.5, len(time))
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
t_tnr, tnr, promi, tones_freqs, time = tnr_ecma_perseg(stimulus, fs)
plt.figure(figsize=(10,8))
plt.pcolormesh(time, tones_freqs, np.nan_to_num(tnr), vmin=0)
plt.colorbar(label = "TNR value in dB")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.ylim(90,2000)
