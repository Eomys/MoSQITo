from mosqito.sq_metrics import roughness_ecma
import matplotlib.pyplot as plt
import numpy as np
f=1000
fs=48000
d=1
dB=60
fmod = 70
fc = 1000
mdepth = 1
time = np.arange(0, d, 1/fs)
signal = (0.5* (1 + mdepth * (np.sin(2 * np.pi * fmod * time)))
        * np.sin(2 * np.pi * fc * time)
    )
rms = np.sqrt(np.mean(np.power(signal, 2)))
ampl = 0.00002 * np.power(10, dB / 20) / rms
stimulus = signal * ampl
R, R_time, R_spec, bark_axis, time_axis = roughness_ecma(stimulus, fs)
plt.step(bark_axis, R_spec)
plt.xlabel("Bark axis [Bark]")
plt.ylabel("Specific roughness [Asper/Bark]")
plt.title("Roughness = " + f"{R:.2f}" + " [Asper]")
