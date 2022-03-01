# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError(
        "In order to perform the tests you need the 'pytest' package."
        )
import numpy as np

from mosqito.functions.noct_spectrum.comp_noct_spectrum import comp_noct_spectrum


def _dB(amp):
    return 20 * np.log10(amp / 2e-5)


@pytest.mark.noct_spectrum  # to skip or run only loudness noct_spectrum tests
def test_noct_spectrum():
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

    spec_3, freq = comp_noct_spectrum(sig, fs, 24, 12600, n=3)
    np.testing.assert_allclose(
        _dB(A_1000 / np.sqrt(2)), _dB(spec_3[freq == 1000]), rtol=0.5
    )
    np.testing.assert_allclose(
        _dB(A_4000 / np.sqrt(2)) + 3, _dB(spec_3[freq == 4000]), rtol=0.5
    )

    spec_1, freq = comp_noct_spectrum(sig, fs, 24, 12600, n=1)
    np.testing.assert_allclose(
        _dB(A_1000 / np.sqrt(2)), _dB(spec_1[freq == 1000]), rtol=0.5
    )
    np.testing.assert_allclose(
        _dB(A_4000 / np.sqrt(2)) + 3, _dB(spec_1[freq == 4000]), rtol=0.5
    )


# test de la fonction
if __name__ == "__main__":
    test_noct_spectrum()