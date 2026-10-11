# -*- coding: utf-8 -*-

# Optional package import
try:
    import pytest
except ImportError:
    raise RuntimeError("In order to perform the tests you need the 'pytest' package.")

import numpy as np

# Local application imports
from mosqito.sq_metrics import tonality_aures


FS = 48000


def _tone(freq, spl, duration=1):
    """Zero-phase sinusoid in [Pa] at the given level in [dB SPL]."""
    t = np.arange(int(round(FS * duration))) / FS
    return np.sqrt(2) * 2e-5 * 10 ** (spl / 20) * np.sin(2 * np.pi * freq * t)


def _band_noise(f_low, f_high, spl, seed=0, duration=1):
    """Gaussian noise limited to [f_low, f_high] Hz in [Pa] at the given level."""
    x = np.random.default_rng(seed).standard_normal(int(round(FS * duration)))
    spectrum = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(x.size, 1 / FS)
    spectrum[(freqs < f_low) | (freqs > f_high)] = 0
    y = np.fft.irfft(spectrum, n=x.size)
    return y * 2e-5 * 10 ** (spl / 20) / np.sqrt(np.mean(y**2))


@pytest.mark.tonality_aures
def test_tonality_aures_reference_tone():
    """A 1 kHz pure tone at 60 dB SPL defines 1 t.u. (Aures 1985, p. 137)."""

    assert tonality_aures(_tone(1000, 60), FS) == pytest.approx(1.0, abs=1e-3)


@pytest.mark.tonality_aures
def test_tonality_aures_tone_between_bins():
    """The result does not depend on where the tone falls between two FFT bins."""

    for freq in (1003, 1006.25, 1009):
        assert tonality_aures(_tone(freq, 60), FS) == pytest.approx(1.0, abs=0.01)


@pytest.mark.tonality_aures
def test_tonality_aures_level_independence():
    """Fig. 7: the tonality of a tone does not depend on its level."""

    for spl in (40, 60, 80):
        assert tonality_aures(_tone(1000, spl), FS) == pytest.approx(1.0, abs=0.03)


@pytest.mark.tonality_aures
def test_tonality_aures_frequency_weighting():
    """Fig. 5: pure tones follow the frequency weighting of Gl. (9)."""

    def w2(freq):
        return (1 / np.sqrt(1 + 0.2 * (freq / 700 + 700 / freq) ** 2)) ** 0.29

    for freq in (250, 4000):
        target = w2(freq) / w2(1000)
        assert tonality_aures(_tone(freq, 60), FS) == pytest.approx(target, abs=0.05)


@pytest.mark.tonality_aures
def test_tonality_aures_narrowband_noise():
    """Fig. 6: 1 kHz band noise half a Bark wide follows Gl. (7)."""

    # 0.5 Bark around 1 kHz on the Bark scale of Zwicker and Terhardt (1980)
    tonality = tonality_aures(_band_noise(961, 1040, 60, duration=2), FS)
    target = 0.13 / (0.5 + 0.13)

    assert tonality == pytest.approx(target, rel=0.15)


@pytest.mark.tonality_aures
def test_tonality_aures_white_noise():
    """White noise has no tonal component."""

    assert tonality_aures(_band_noise(20, 20000, 60), FS) == pytest.approx(0.0, abs=0.02)


@pytest.mark.tonality_aures
def test_tonality_aures_masked_tone():
    """A 1.5 kHz, 30 dB tone next to a 1 kHz, 60 dB tone is nearly masked (Gl. 8)."""

    alone = tonality_aures(_tone(1000, 60), FS)
    pair = tonality_aures(_tone(1000, 60) + _tone(1500, 30), FS)

    assert pair == pytest.approx(alone, abs=0.01)


@pytest.mark.tonality_aures
def test_tonality_aures_tone_in_noise_increases_with_level():
    """Tonality of a 1 kHz tone in one-critical-band noise rises with the tone level."""

    noise = _band_noise(912, 1088, 60)
    tonality = [tonality_aures(_tone(1000, spl) + noise, FS) for spl in (60, 70, 80)]

    assert tonality[0] < tonality[1] < tonality[2]


@pytest.mark.tonality_aures
def test_tonality_aures_invalid_input():
    """Multichannel and empty signals are rejected."""

    with pytest.raises(ValueError):
        tonality_aures(np.zeros((2, FS)), FS)
    with pytest.raises(ValueError):
        tonality_aures(np.array([]), FS)


if __name__ == "__main__":
    test_tonality_aures_reference_tone()
    test_tonality_aures_tone_between_bins()
    test_tonality_aures_level_independence()
    test_tonality_aures_frequency_weighting()
    test_tonality_aures_narrowband_noise()
    test_tonality_aures_white_noise()
    test_tonality_aures_masked_tone()
    test_tonality_aures_tone_in_noise_increases_with_level()
    test_tonality_aures_invalid_input()


@pytest.mark.tonality_aures
def test_tonality_aures_tv_reference_tone():
    """Every 250 ms frame of the reference tone gives 1 t.u., frames every 125 ms."""
    from mosqito.sq_metrics import tonality_aures_tv

    tonality, time = tonality_aures_tv(_tone(1000, 60, duration=2), FS)
    assert tonality.shape == time.shape == (15,)
    assert time[0] == pytest.approx(0.125)
    assert np.diff(time) == pytest.approx(0.125)
    assert tonality == pytest.approx(np.ones(15), abs=1e-3)


@pytest.mark.tonality_aures
def test_tonality_aures_tv_tone_switched_on():
    """A tone that starts after one second raises the tonality of the later frames only."""
    from mosqito.sq_metrics import tonality_aures_tv

    tone = _tone(1000, 60, duration=2)
    tone[:FS] = 0
    tonality, time = tonality_aures_tv(_band_noise(20, 20000, 50, duration=2) + tone, FS)
    before = tonality[time < 0.9]  # frames that end before the tone starts
    after = tonality[time > 1.1]  # frames that start after it
    assert before.max() < 0.2
    assert after.min() > 0.3
    assert after.min() > before.max() + 0.3


@pytest.mark.tonality_aures
def test_tonality_aures_tv_short_signal():
    """A signal shorter than a frame is analysed as one frame."""
    from mosqito.sq_metrics import tonality_aures_tv

    tonality, time = tonality_aures_tv(_tone(1000, 60, duration=0.2), FS)
    assert tonality.shape == (1,)
    assert time[0] == pytest.approx(0.1)
    assert tonality[0] == pytest.approx(1.0, abs=1e-3)


@pytest.mark.tonality_aures
def test_tonality_aures_tv_invalid_parameters():
    from mosqito.sq_metrics import tonality_aures_tv

    with pytest.raises(ValueError):
        tonality_aures_tv(_tone(1000, 60), FS, frame_length=0.05)
    with pytest.raises(ValueError):
        tonality_aures_tv(_tone(1000, 60), FS, hop=0)
    with pytest.raises(ValueError):
        tonality_aures_tv(np.zeros((2, 100)), FS)
