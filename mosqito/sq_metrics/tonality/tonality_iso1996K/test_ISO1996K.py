import pytest

from mosqito.functions.shared.load import load
from comp_tonality import comp_tonality


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

    #-- CORRECTO --
    """----PRUEBA--TONO--100-Hz----"""
    sig, fs = load(True, "tests\input\TONE100HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {100.0: 84.85146128088218}

    #-- CORRECTO --
    """----PRUEBA--TONO--200-Hz----"""
    sig, fs = load(True, "tests\input\TONE200HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {200.0: 84.85835085762665}

    #-- CORRECTO --
    """----PRUEBA--TONO--1-KHz----"""
    sig, fs = load(True, "tests/input/1KHZ60DB.WAV", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {1000.0: 63.962211067656554}

    #-- CORRECTO --
    """----PRUEBA--TONO--2-KHz----"""
    sig, fs = load(True, "tests\input\TONE2000HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {2000.0: 84.95769475723816}

    #-- CORRECTO --
    """----PRUEBA--TONO--4-KHz----"""
    sig, fs = load(True, "tests\input\TONE4000HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {4000.0: 84.95769513303429}

    #-- CORRECTO --
    """----PRUEBA--TONO--5000-Hz----"""
    sig, fs = load(True, "tests\input\TONE5000HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    assert tones == {5000.0: 84.95769534548218}
