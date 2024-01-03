import matplotlib.pyplot as plt
from numpy import linspace, log10, array

from mosqito.utils.LTQ import LTQ
from mosqito.utils.hearing_threshold import hearing_threshold
from mosqito.utils._hearing_threshold_data import f_iso226 as f_axis
from mosqito.utils.conversion import freq2bark, bark2freq
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._LTH import _LTH

# TODO : include equal_loudness_contour and compare with ISO 226:2003
#           (hearing_threshold could call equal_loudness_contour)

f_axis = array(f_axis)
bark_axis = freq2bark(f_axis)

lth_zwicker = LTQ(bark_axis)
lth_roughness = LTQ(bark_axis, reference="roughness")

lth_tonality_ecma = _LTH(f_axis)

lth_iso226 = hearing_threshold(f_axis)

plt.semilogx(f_axis, lth_zwicker, label="Zwicker")
plt.semilogx(f_axis, lth_roughness, label="Roughness")
plt.semilogx(f_axis, lth_tonality_ecma, label="Tonality Ecma")
plt.semilogx(f_axis, lth_iso226, label="ISO 226:2003")
plt.legend()
plt.xlabel("Frequency")
plt.ylabel("SPL")
plt.show(block=True)

print("done")
