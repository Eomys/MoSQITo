""" This module includes several functions currently used for sound quality analysis :

Conversion
==========

.. toctree::
   :maxdepth: 1

   /source/mosqito.utils.conversion
   
Sine wave generator
===================

.. toctree::
   :maxdepth: 1

   /source/mosqito.utils.sine_wave_generator
   
   
Time segmentation
===================

.. toctree::
   :maxdepth: 1

   /source/mosqito.utils.time_segmentation
   
Threshold of quiet
===================

.. toctree::
   :maxdepth: 1
   
   /source/mosqito.utils.LTQ
   
Check compliance with ISO
===================

.. toctree::
   :maxdepth: 1
   
   /source/mosqito.utils.isoclose
   
Signal loading
===================

.. toctree::
   :maxdepth: 1
   
   /source/mosqito.utils.load

"""

__all__ = ['utils']


from mosqito.utils.conversion import amp2db, db2amp, bark2freq, freq2bark, spectrum2dBA
from mosqito.utils.isoclose import isoclose
from mosqito.utils.load import load
from mosqito.utils.sine_wave_generator import sine_wave_generator
from mosqito.utils.time_segmentation import time_segmentation


