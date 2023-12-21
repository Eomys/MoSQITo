from mosqito.sq_metrics import roughness_dw_freq
from mosqito.sound_level_meter import spectrum
import matplotlib.pyplot as plt
import numpy as np
fc=1000
fmod=70
fs=44100
d=0.2
dB=60
time = np.arange(0, d, 1/fs)
stimulus = (
0.5
* (1 + np.sin(2 * np.pi * fmod * time))
* np.sin(2 * np.pi * fc * time))
rms = np.sqrt(np.mean(np.power(stimulus, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = stimulus * ampl
n = len(stimulus)
spec, freqs = spectrum(stimulus, fs, db=False)
R, R_specific, bark = roughness_dw_freq(spec, freqs)
plt.plot(bark, R_specific)
plt.xlabel("Bark axis [Bark]")
plt.ylabel("Specific roughness, [Asper/Bark]")
plt.title("Roughness = " + f"{R:.2f}" + " [Asper]")
