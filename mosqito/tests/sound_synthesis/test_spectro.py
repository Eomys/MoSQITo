# -*- coding: utf-8 -*-

# Standard library imports

# Third party imports
import pytest

# Local application imports
from mosqito.functions.sound_synthesis.spectro_to_sound import spectro_to_sound
from mosqito.functions.sound_synthesis.read_spectro_xls import read_spectro_xls

@pytest.mark.sound_synth  # to skip or run only loudness zwicker time-varying tests
def test_spectro():
    file_name = "mosqito/tests/sound_synthesis/spectro.xls" # Path to excel file

    # Read excel file
    spectrum, freqs, time = read_spectro_xls(file_name)

    # Compute and write wave file
    spectro_to_sound(spectrum, freqs, fs=44100, time=[time[0], time[-1]], file_name="spectro_sound.wav")