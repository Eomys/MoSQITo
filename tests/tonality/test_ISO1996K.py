import pytest

from mosqito.functions.shared.load import load
from mosqito.functions.tonality_iso1996K.comp_tonality import comp_tonality


@pytest.mark.tonality_1996k  # to skip or run PR test
def test_ISO1996K():
    #-- CORRECTO --
    """----PRUEBA--TONO--100-Hz----"""
    sig, fs = load(True, "tests\input\TONE100HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--200-Hz----"""
    sig, fs = load(True, "tests\input\TONE200HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--1-KHz----"""
    sig, fs = load(True, "tests/input/1KHZ60DB.WAV", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--2-KHz----"""
    sig, fs = load(True, "tests\input\TONE2000HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--4-KHz----"""
    sig, fs = load(True, "tests\input\TONE4000HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")

    #-- CORRECTO --
    """----PRUEBA--TONO--5000-Hz----"""
    sig, fs = load(True, "tests\input\TONE5000HZ.wav", calib=1)
    tones = comp_tonality(sig, fs)
    print("----RESULT-----")
    print(tones)
    print("---------------")
    
    # assert tones ==
