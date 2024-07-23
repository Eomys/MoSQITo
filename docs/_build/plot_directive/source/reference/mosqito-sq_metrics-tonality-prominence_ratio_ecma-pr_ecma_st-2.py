import numpy as np
import matplotlib.pyplot as plt
from mosqito.sq_metrics import pr_ecma_st
fs = 48000
d = 2
f = 1000
dB = 60
time = np.arange(0, d, 1/fs)
stimulus = np.sin(2 * np.pi * f * time) + 0.5 * np.sin(2 * np.pi * 3 * f * time)+ np.random.normal(0,0.5, len(time))
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
t_pr, pr, prom, tones_freqs = pr_ecma_st(stimulus, fs)
plt.bar(tones_freqs, pr, width=50)
plt.grid(axis='y')
plt.ylabel("PR [dB]")
plt.title("Total PR = "+ f"{t_pr[0]:.2f}" + " dB")
plt.xscale('log')
xticks_pos = list(tones_freqs) + [100,1000,10000]
xticks_pos = np.sort(xticks_pos)
xticks_label = [str(elem) for elem in xticks_pos]
plt.xticks(xticks_pos, labels=xticks_label, rotation = 30)
plt.xlabel("Frequency [Hz]")
