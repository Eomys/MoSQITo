""" This module includes functions to compute tonality :

Prominence Ratio (ECMA 418)
==================================

.. toctree::
   :maxdepth: 4

   /source/reference/mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_st
   /source/reference/mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_freq
   /source/reference/mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_tv
   
Tone-to-noise Ratio (ISO 532B)
==================================

.. toctree::
   :maxdepth: 4


   /source/reference/mosqito.sq_metrics.tonality.tone_to_noise_ecma.tnr_ecma_st
   /source/reference/mosqito.sq_metrics.tonality.tone_to_noise_ecma.tnr_ecma_freq
   /source/reference/mosqito.sq_metrics.tonality.tone_to_noise_ecma.tnr_ecma_tv
   
"""

__all__ = ['tonality']

from mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_st import pr_ecma_st
from mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_tv import pr_ecma_tv
from mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_freq import pr_ecma_freq

from mosqito.sq_metrics.tonality.tone_to_noise_ecma.tnr_ecma_st import tnr_ecma_st
from mosqito.sq_metrics.tonality.tone_to_noise_ecma.tnr_ecma_tv import tnr_ecma_tv
from mosqito.sq_metrics.tonality.tone_to_noise_ecma.tnr_ecma_freq import tnr_ecma_freq
