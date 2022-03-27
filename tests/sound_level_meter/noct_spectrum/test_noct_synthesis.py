# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
        )
import numpy as np

from scipy.fft import fft, fftfreq

from mosqito.sound_level_meter.noct_spectrum.noct_synthesis import (
    noct_synthesis,
)


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
    
       
    spectrum = fft(sig)
    freqs = fftfreq(len(spectrum))

    spec_3, freq = noct_synthesis(spectrum, freqs, fs, 24, 12600, n=3)
    np.testing.assert_allclose(
        _dB(A_1000 / np.sqrt(2)), _dB(spec_3[freq == 1000]), rtol=0.5
    )
    np.testing.assert_allclose(
        _dB(A_4000 / np.sqrt(2)) + 3, _dB(spec_3[freq == 4000]), rtol=0.5
    )

    spec_1, freq = noct_synthesis(spectrum, freqs, fs, 24, 12600, n=1)
    np.testing.assert_allclose(
        _dB(A_1000 / np.sqrt(2)), _dB(spec_1[freq == 1000]), rtol=0.5
    )
    np.testing.assert_allclose(
        _dB(A_4000 / np.sqrt(2)) + 3, _dB(spec_1[freq == 4000]), rtol=0.5
    )

# test de la fonction
if __name__ == "__main__":
    test_noct_synthesis()