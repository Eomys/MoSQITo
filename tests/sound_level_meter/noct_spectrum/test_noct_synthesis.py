# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
        )
import numpy as np
from scipy.fft import fft

from mosqito.sound_level_meter.noct_spectrum.noct_synthesis import noct_synthesis
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.load import load


def _dB(amp):
    return 20 * np.log10(amp / 2e-5)


@pytest.mark.noct_synthesis  # to skip or run only loudness noct_synthesis tests
def test_noct_synthesis():
    fs = 51200  # sampling freq
    d = 1  # duration
    t = np.arange(0, d, 1 / fs)  # Time axis
    sig = np.random.normal(0, 1, size=len(t))
    A_1000 = 1 * np.sqrt(2)  # Amp = 1 Pa rms
    sig += A_1000 * np.sin(2 * np.pi * 1000 * t)
    A_4000 = 0.5 * np.sqrt(2)  # Amp = 1 Pa rms
    sig += A_4000 * np.sin(2 * np.pi * 3950 * t)
    sig += A_4000 * np.sin(2 * np.pi * 4050 * t)
    sig += 0.75 * np.sin(2 * np.pi * 250 * t)
    
       
    # frequency domain
    nseg = len(sig)
    window = np.hanning(nseg)
    window = window / np.sum(window)

    # Creation of the spectrum by FFT
    spectrum = fft(sig * window)[0:nseg//2] * 1.42
    freqs = np.arange(0, nseg//2, 1) * (fs / nseg)

    spec_3, freq = noct_synthesis(spectrum, freqs, fmin=24, fmax=12600, n=3)
    np.testing.assert_allclose(
        _dB(A_1000 / np.sqrt(2)), _dB(spec_3[freq == 1000]), rtol=0.5
    )
    np.testing.assert_allclose(
        _dB(A_4000 / np.sqrt(2)) + 3, _dB(spec_3[freq == 4000]), rtol=0.5
    )

    spec_1, freq = noct_synthesis(spectrum, freqs, fmin=24, fmax=12600, n=1)
    np.testing.assert_allclose(
        _dB(A_1000 / np.sqrt(2)), _dB(spec_1[freq == 1000]), rtol=0.5
    )
    np.testing.assert_allclose(
        _dB(A_4000 / np.sqrt(2)) + 3, _dB(spec_1[freq == 4000]), rtol=0.5
    )
    
@pytest.mark.noct_synthesis  # to skip or run only loudness noct_synthesis tests
def test_noct_comparison_spectrum_synthesis():
    sig, fs = load("tests\input\Test signal 5 (pinknoise 60 dB).wav", wav_calib=2*2**0.5)
    

    spec_3t, freq_3t = noct_spectrum(sig, fs, fmin=24, fmax=12600, n=3)

    spec_1t, freq_1t = noct_spectrum(sig, fs, fmin=24, fmax=12600, n=1)
   
    # frequency domain
    n = len(sig)
    window = np.blackman(n)
    window = window / np.sum(window)

    # Creation of the spectrum by FFT
    spectrum = fft(sig * window)[0:n//2] * 1.42
    freqs = np.arange(0, n//2, 1) * (fs / n)


    spec_3f, freq_3f = noct_synthesis(spectrum, freqs, fmin=24, fmax=12600, n=3)

    spec_1f, freq_1f = noct_synthesis(spectrum, freqs, fmin=24, fmax=12600, n=1)

    # plt.figure()
    # plt.plot(freq_3t, _dB(spec_3t), label='noct spectrum')
    # plt.plot(freq_3f, _dB(np.abs(spec_3f)), label='noct synth')
    # plt.legend()
    
    # plt.figure()
    # plt.plot(freq_1t, _dB(spec_1t), label='noct spectrum')
    # plt.plot(freq_1f, _dB(np.abs(spec_1f)), label='noct synth')
    # plt.legend()

    

# test de la fonction
if __name__ == "__main__":
    test_noct_synthesis()