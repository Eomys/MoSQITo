from mosqito.sq_metrics.loudness.loudness_ecma.loudness_ecma import loudness_ecma
from mosqito.sq_metrics.loudness.loudness_zwst.loudness_zwst import loudness_zwst
from mosqito.sq_metrics.loudness.loudness_zwtv.loudness_zwtv import loudness_zwtv
from mosqito.sq_metrics.loudness.utils.equal_loudness_contours import (
    equal_loudness_contours,
)
from mosqito.sq_metrics.tonality.prominence_ratio_ecma.prominence_ratio_ecma import (
    prominence_ratio_ecma,
)
from mosqito.sq_metrics.tonality.tone_to_noise_ecma.tone_to_noise_ecma import (
    tone_to_noise_ecma,
)
from mosqito.sq_metrics.roughness.roughness_danielweber.roughness_danielweber import (
    roughness_danielweber,
)
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din import sharpness_din
from mosqito.sq_metrics.loudness.utils.sone_to_phon import sone_to_phon

# Colors and linestyles
COLORS = [
    "#69c3c5",
    "#9969c4",
    "#c46b69",
    "#95c469",
    "#2a6c6e",
]
