# -*- coding: utf-8 -*-
import sys
sys.path.append('../../..')

from pandas import ExcelFile, read_excel
from mosqito.sound_synthesis.spectro_to_sound import spectro_to_sound
from numpy import delete


xls_file = ExcelFile("../data/PR0139_order_analysis.xlsx")
# First row = speeds
freqs = delete(read_excel(xls_file, sheet_name="Frequency", header=None, nrows=122, squeeze=True).to_numpy(), 0, 0)
spectrum = delete(read_excel(xls_file, sheet_name="Amplitude", header=None, nrows=122, squeeze=True).to_numpy(), 0, 0)

spectro_to_sound(spectrum, freqs, cut_indices=[67], time=[0,3.4,10], fs=44100, file_name="PR0139_sound.wav")