""" This module includes several functions currently used for sound quality analysis :

Conversion
==========

.. toctree::
   :maxdepth: 2
   
   /source/reference/mosqito.utils.conversion.amp2db
   /source/reference/mosqito.utils.conversion.db2amp
   /source/reference/mosqito.utils.conversion.bark2freq
   /source/reference/mosqito.utils.conversion.freq2bark
   /source/reference/mosqito.utils.conversion.spectrum2dBA
   
Sine wave generator
===================

.. toctree::
   :maxdepth: 2

   /source/reference/mosqito.utils.sine_wave_generator
   
   
Time segmentation
===================

.. toctree::
   :maxdepth: 2

   /source/reference/mosqito.utils.time_segmentation
   
Threshold of quiet
===================

.. toctree::
   :maxdepth: 2
   
   /source/reference/mosqito.utils.LTQ
   
   
Signal loading
===================

.. toctree::
   :maxdepth: 2
   
   /source/reference/mosqito.utils.load

"""

__all__ = ['utils']


from mosqito.utils.load import load
from mosqito.utils.sine_wave_generator import sine_wave_generator
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.utils.conversion.amp2db import amp2db
from mosqito.utils.conversion.db2amp import db2amp
from mosqito.utils.conversion.bark2freq import bark2freq
from mosqito.utils.conversion.freq2bark import freq2bark
from mosqito.utils.conversion.spectrum2dBA import spectrum2dBA

