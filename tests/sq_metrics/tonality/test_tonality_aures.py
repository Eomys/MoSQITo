# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

import numpy as np

# Local application imports
from mosqito.sq_metrics import tonality_aures
from mosqito.utils import sine_wave_generator


FS = 48000


def _white_noise(spl_level, seed=0):
    """Return 1 s of white noise in [Pa] at the given level in [dB SPL]."""
    noise = np.random.default_rng(seed).standard_normal(FS)
    return noise * 2e-5 * 10 ** (spl_level / 20) / np.std(noise)


@pytest.mark.aures_tonality
def test_tonality_aures_reference_tone():
    """A 1 kHz pure tone at 60 dB SPL defines 1 t.u."""

    signal, _ = sine_wave_generator(FS, 1, 1000, 60)

    assert tonality_aures(signal, FS) == pytest.approx(1.0, abs=0.1)


@pytest.mark.aures_tonality
def test_tonality_aures_white_noise():
    """White noise has no tonal component."""

    assert tonality_aures(_white_noise(60), FS) < 0.1


@pytest.mark.aures_tonality
def test_tonality_aures_increases_with_tone_level():
    """Tonality of a 1 kHz tone in noise increases with the tone level."""

    noise = _white_noise(60)
    tonality = [
        tonality_aures(sine_wave_generator(FS, 1, 1000, level)[0] + noise, FS)
        for level in (40, 60, 80)
    ]

    assert tonality[0] < tonality[1] < tonality[2]


@pytest.mark.aures_tonality
def test_tonality_aures_invalid_input():
    """Multichannel and empty signals are rejected."""

    with pytest.raises(ValueError):
        tonality_aures(np.zeros((2, FS)), FS)
    with pytest.raises(ValueError):
        tonality_aures(np.array([]), FS)


if __name__ == "__main__":
    test_tonality_aures_reference_tone()
    test_tonality_aures_white_noise()
    test_tonality_aures_increases_with_tone_level()
    test_tonality_aures_invalid_input()
