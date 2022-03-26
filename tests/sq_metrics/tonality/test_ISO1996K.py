import pytest

from mosqito.utils.load import load
from mosqito.sq_metrics.tonality.tonality_iso1996K.comp_tonality import comp_tonality


@pytest.mark.tonality_1996k  # to skip or run PR test
def test_ISO1996K():
    """Test function for the detection of a prominent tone 
    using the inspection method described in ISO 1996-2 Annex K.

    Validation of the function "comp_tonality" with signal array
    as input. The input signals have been obtained from the website https://freesound.org/.

    Parameters
    ----------
    None

    Outputs
    -------
    None
    """

    """-----TONE--100-Hz----"""
    sig, fs = load("tests\input\TONE100HZ.wav")
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {100.0: 84.85146128088218}


    """-----TONE--200-Hz----"""
    sig, fs = load("tests\input\TONE200HZ.wav")
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {200.0: 84.85835085762665}


    """-----TONE--1-KHz----"""
    sig, fs = load("tests/input/TONE1000HZ.WAV")
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {1000.0: 63.962211067656554}


    """-----TONE--2-KHz----"""
    sig, fs = load("tests\input\TONE2000HZ.wav")
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {2000.0: 84.95769475723816}


    """-----TONE--4-KHz----"""
    sig, fs = load("tests\input\TONE4000HZ.wav")
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {4000.0: 84.95769513303429}


    """-----TONE--5-kHz----"""
    sig, fs = load("tests\input\TONE5000HZ.wav")
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {5000.0: 84.95769534548218}


    """-----MULTITONE-ALARM----"""
    sig, fs = load("tests\input\MULTITONE_ALARM.wav")
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {800.0: 53.685430439067396, 2000.0: 55.97882939521264, 3150.0: 64.05469163499629, 5000.0: 74.90550800435562}


    """-----MUTITONE-SIREN----"""
    sig, fs = load("tests\input\MULTITONE_SIREN.wav")
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {1600.0: 61.618174324534216, 2500.0: 56.86145723559116, 8000.0: 38.87188014184665}


    """-----ATONAL-SIGNAL----"""
    sig, fs = load("tests\input\WHITE_NOISE.wav")
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {}