import pytest

# Third party imports
import numpy as np

# Local imports
from mosqito.functions.shared.load import load
from LAeq_3oct import LAeq_3oct
from mosqito.functions.oct3filter.calc_third_octave_levels import calc_third_octave_levels

@pytest.mark.slm_test  # to skip or run PR test
def test_LAeq():

    #-- you have to test  --
    """----PRUEBA--TONO--100-Hz----"""
    sig, fs = load(True, "tests\input\TONE100HZ.wav", calib=1)

    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])

    LAeq = LAeq_3oct(spectrum_signal_samples, freq)
    print("----RESULT-----")
    print(LAeq)
    print("---------------")
    # assert

    #-- you have to test  --
    """----PRUEBA--TONO--200-Hz----"""
    sig, fs = load(True, "tests\input\TONE200HZ.wav", calib=1)

    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])
    
    LAeq = LAeq_3oct(spectrum_signal_samples, freq)
    print("----RESULT-----")
    print(LAeq)
    print("---------------")
    # assert

    #-- you have to test  --
    """----PRUEBA--TONO--1-KHz----"""
    sig, fs = load(True, "tests/input/1KHZ60DB.WAV", calib=1)
    
    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])
    
    LAeq = LAeq_3oct(spectrum_signal_samples, freq)
    print("----RESULT-----")
    print(LAeq)
    print("---------------")
    # assert

    #-- you have to test  --
    """----PRUEBA--TONO--2-KHz----"""
    sig, fs = load(True, "tests\input\TONE2000HZ.wav", calib=1)
    
    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])
    
    LAeq = LAeq_3oct(spectrum_signal_samples, freq)
    print("----RESULT-----")
    print(LAeq)
    print("---------------")
    # assert

    #-- you have to test  --
    """----PRUEBA--TONO--4-KHz----"""
    sig, fs = load(True, "tests\input\TONE4000HZ.wav", calib=1)
    
    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])
    
    LAeq = LAeq_3oct(spectrum_signal_samples, freq)
    print("----RESULT-----")
    print(LAeq)
    print("---------------")
    # assert 

    #-- you have to test  --
    """----PRUEBA--TONO--5000-Hz----"""
    sig, fs = load(True, "tests\input\TONE5000HZ.wav", calib=1)
    
    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])
    
    LAeq = LAeq_3oct(spectrum_signal_samples, freq)
    print("----RESULT-----")
    print(LAeq)
    print("---------------")
    # assert 
