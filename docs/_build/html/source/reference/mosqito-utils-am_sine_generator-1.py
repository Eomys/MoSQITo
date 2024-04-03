from mosqito.utils import am_sine_generator
import matplotlib.pyplot as plt
import numpy as np
fs = 48000      # [Hz]
duration = 1
t = np.linspace(0, duration, int(fs*duration))
dB = 60         # [dB SPL]
fc = 100        # [Hz]
fm = 4          # [Hz]
xmod = np.sin(2*np.pi*t*fm)
y_am, m = am_sine_generator(xmod, fs, fc, dB, True)
fig, plots = plt.subplots(2, 1)
plots[0].set_title(f'Amplitude-modulated sine wave, modulation index = {m:.1f}')
plots[0].plot(t, xmod, 'C0', label='Modulating signal')
plots[0].legend(loc='upper right')
plots[0].grid()
plots[0].set_ylabel('Amplitude')
plots[0].set_xlim([0, duration])
plots[1].plot(t, y_am, '#69c3c5', label='AM signal')
plots[1].legend(loc='upper right')
plots[1].grid()
plots[1].set_ylabel('Amplitude')
plots[1].set_xlim([0, duration])
plots[1].set_xlabel('Time [s]')
fig.set_tight_layout('tight')
# >>>
