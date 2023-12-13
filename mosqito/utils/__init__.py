""" This module includes several functions currently used for sound quality analysis :

Conversion
==========

.. toctree::
   :maxdepth: 1

   /source/mosqito.utils.conversion.amp2db
   /source/mosqito.utils.conversion.db2amp
   /source/mosqito.utils.conversion.bark2freq
   /source/mosqito.utils.conversion.freq2bark
   /source/mosqito.utils.conversion.spectrum2dBA
   
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


from mosqito.utils.conversion.amp2db import amp2db
from mosqito.utils.conversion.db2amp import db2amp
from mosqito.utils.conversion.bark2freq import bark2freq
from mosqito.utils.conversion.freq2bark import freq2bark
from mosqito.utils.conversion.spectrum2dBA import spectrum2dBA
from mosqito.utils.isoclose import isoclose
from mosqito.utils.load import load
from mosqito.utils.sine_wave_generator import sine_wave_generator
from mosqito.utils.time_segmentation import time_segmentation


