# -*- coding: utf-8 -*-
import sys
sys.path.append('../../..') # Path to MoSQITo folder

from mosqito.sound_synthesis.spectro_to_sound import spectro_to_sound
from mosqito.sound_synthesis.read_spectro_xls import read_spectro_xls

file_name = "../data/spectro.xls" # Path to excel file

# Read excel file
spectrum, freqs, time = read_spectro_xls(file_name)

# Compute and write wave file
spectro_to_sound(spectrum, freqs, fs=44100, time=[time[0], time[-1]], file_name="spectro_sound.wav")