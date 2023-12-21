"""This module includes functions to estimate the sound level of a signal :

Frequency spectrum
==================

.. toctree::
   :maxdepth: 2

   /source/reference/mosqito.sound_level_meter.spectrum

N-octave spectrum
=================

.. toctree::
   :maxdepth: 2

   /source/reference/mosqito.sound_level_meter.noct_spectrum.noct_spectrum
   /source/reference/mosqito.sound_level_meter.noct_spectrum.noct_synthesis

"""

__all__ = ['sound_level_meter']

from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.sound_level_meter.noct_spectrum.noct_synthesis import noct_synthesis
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sound_level_meter.freq_band_synthesis import freq_band_synthesis
