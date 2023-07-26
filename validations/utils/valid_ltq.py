import matplotlib.pyplot as plt
from numpy import linspace, log10, array

from mosqito.utils.LTQ import LTQ
from mosqito.utils.hearing_threshold import hearing_threshold
from mosqito.utils._hearing_threshold_data import f_iso226 as f_axis
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_ecma_data import ltq_z
from mosqito.utils.conversion import freq2bark, bark2freq
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._LTH import _LTH

f_axis = array(f_axis)
bark_axis = freq2bark(f_axis)

bark_ecma = linspace(0.5, 26.5, num=53, endpoint=True)
f_ecma = bark2freq(bark_ecma)

lth_zwicker = LTQ(bark_axis)
lth_roughness = LTQ(bark_axis, reference="roughness")

lth_tonality_ecma = _LTH(f_axis)

lth_iso226 = hearing_threshold(f_axis)

plt.plot(f_axis, lth_zwicker, label="Zwicker")
plt.plot(f_axis, lth_roughness, label="Roughness")
plt.plot(f_ecma, 20 * log10(array(ltq_z) / 2e-5), label="Ecma")
plt.plot(f_axis, lth_tonality_ecma, label="Tonality Ecma")
plt.plot(f_axis, lth_iso226, label="ISO 226:2003")
plt.legend()
plt.xlabel("Bark axis")
plt.ylabel("SPL")
plt.show(block=True)

print("done")
