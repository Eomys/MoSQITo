import pytest

from mosqito.functions.shared.load import load
from mosqito.functions.tonality_iso1996K.comp_tonality import comp_tonality


@pytest.mark.tonality_1996k  # to skip or run PR test
def test_ISO1996K():
    sig, fs = load(True, "tests/input/1KHZ60DB.WAV", calib=1)
    tones = comp_tonality(sig, fs)
    # assert tones ==
