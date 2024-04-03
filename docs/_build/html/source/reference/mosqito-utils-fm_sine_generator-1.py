from mosqito.utils import fm_sine_generator
import matplotlib.pyplot as plt
fs = 48000     # [Hz]
duration = 1
t = np.linspace(0, duration, int(fs*duration))
dB = 60        # [dB SPL]
fc = 50        # [Hz]
k = fc//2      # [Hz per unit amplitude of 'xm']
fm = 10        # [Hz]
xmod = np.sin(2*np.pi*t*fm)
y_fm, inst_freq, f_delta, m  = fm_sine_generator(xmod, fs, fc, k, dB, True)
plt.figure()
plt.plot(t, y_fm)
plt.xlabel("Time axis [s]")
plt.ylabel("Amplitude signal [Pa]")
plt.title(f'Modulation index = {m:.1f}')
plt.figure()
plt.xlabel("Time axis [s]")
plt.ylabel("Instantaneous frequency [Hz]")
plt.title(f'Max frequency deviation = {f_delta:.1f}')
plt.plot(t, inst_freq)
