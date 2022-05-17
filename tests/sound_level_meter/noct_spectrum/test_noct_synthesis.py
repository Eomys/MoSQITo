# -*- coding: utf-8 -*-

# Optional packages import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
    )
import matplotlib.pyplot as plt

# External library imports
import numpy as np
from numpy.fft import fft, fftfreq

# Local import
from mosqito.sound_level_meter.noct_spectrum.noct_synthesis import noct_synthesis
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.load import load


def _dB(amp):
    return 20 * np.log10(amp / 2e-5)


@pytest.mark.noct_synthesis  # to skip or run only loudness noct_synthesis tests
def test_noct_synthesis_technical():
    
    ############################## TECHNICAL SIGNAL ##########################
    sig, fs = load("tests\input\Test signal 5 (pinknoise 60 dB).wav", wav_calib=2*2**0.5)

    spec_3t, freq_3t = noct_spectrum(sig, fs, fmin=24, fmax=12600, n=3)
    spec_1t, freq_1t = noct_spectrum(sig, fs, fmin=24, fmax=12600, n=1)

    # Creation of the spectrum by FFT
    # 2* because we consider a one-sided spectrum
    # /np.sqrt(2) to go from amplitude peak to amplitude RMS
    # /n normalization for the numpy fft function
    n = len(sig)
    spectrum = 2 / np.sqrt(2) / n * fft(sig)[0:n//2]

    # Frequency axis
    freqs = fftfreq(n, 1/fs)[0:n//2]

    spec_3f, freq_3f = noct_synthesis(np.abs(spectrum), freqs, fmin=24, fmax=12600, n=3)
    spec_1f, freq_1f = noct_synthesis(np.abs(spectrum), freqs, fmin=24, fmax=12600, n=1)

    # plt.figure()
    # plt.semilogx(freq_3t, _dB(spec_3t), label='noct spectrum')
    # plt.semilogx(freq_3f, _dB(spec_3f), label='noct synth')
    # plt.legend()

    # plt.figure()
    # plt.semilogx(freq_1t, _dB(spec_1t), label='noct spectrum')
    # plt.semilogx(freq_1f, _dB(spec_1f), label='noct synth')
    # plt.legend()

    # plt.show()

    np.testing.assert_allclose(_dB(spec_3t[:, 0]), _dB(spec_3f), atol=0.3)
    np.testing.assert_allclose(_dB(spec_1t[:, 0]), _dB(spec_1f), atol=0.3)
    
    
# @pytest.mark.noct_synthesis  # to skip or run only loudness noct_synthesis tests
# def test_noct_synthesis_synthetic():

#     ########################## SYNTHETIC SIGNAL###############################
#     sig, fs = load("tests\input\white_noise_200_2000_Hz_stationary.wav", wav_calib=2*2**0.5)

#     spec_3t, freq_3t = noct_spectrum(sig, fs, fmin=24, fmax=12600, n=3)
#     spec_1t, freq_1t = noct_spectrum(sig, fs, fmin=24, fmax=12600, n=1)

#     # Creation of the spectrum by FFT
#     # 2* because we consider a one-sided spectrum
#     # /np.sqrt(2) to go from amplitude peak to amplitude RMS
#     # /n normalization for the numpy fft function
#     n = len(sig)
#     spectrum = 2 / np.sqrt(2) / n * fft(sig)[0:n//2]

#     # Frequency axis
#     freqs = fftfreq(n, 1/fs)[0:n//2]

#     spec_3f, freq_3f = noct_synthesis(np.abs(spectrum), freqs, fmin=24, fmax=12600, n=3)
#     spec_1f, freq_1f = noct_synthesis(np.abs(spectrum), freqs, fmin=24, fmax=12600, n=1)

#     plt.figure()
#     plt.semilogx(freq_3t, _dB(spec_3t), label='noct spectrum')
#     plt.semilogx(freq_3f, _dB(spec_3f), label='noct synth')
#     plt.legend()

#     plt.figure()
#     plt.semilogx(freq_1t, _dB(spec_1t), label='noct spectrum')
#     plt.semilogx(freq_1f, _dB(spec_1f), label='noct synth')
#     plt.legend()

#     plt.show()

#     np.testing.assert_allclose(_dB(spec_3t[:, 0]), _dB(spec_3f), atol=0.3)
#     np.testing.assert_allclose(_dB(spec_1t[:, 0]), _dB(spec_1f), atol=0.3)



# test de la fonction
if __name__ == "__main__":
    test_noct_synthesis_technical()
    # test_noct_synthesis_synthetic()
