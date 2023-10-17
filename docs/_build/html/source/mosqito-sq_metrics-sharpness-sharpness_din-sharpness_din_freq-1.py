from mosqito.sq_metrics import sharpness_din_freq
import matplotlib.pyplot as plt
import numpy as np
fs=48000
d=0.2
dB=60
time = np.arange(0, d, 1/fs)
f = np.linspace(1000,5000, len(time))
stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
spec = np.abs(np.fft.fft(stimulus))
freqs = np.linspace(0, fs//2,len(spec)//2)
S = sharpness_din_freq(spec[:len(spec)//2], freqs)
print('Sharpness value : ', S, ' acum.')
