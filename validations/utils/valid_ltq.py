import matplotlib.pyplot as plt
from numpy import linspace, log10, array

from mosqito.utils.LTQ import LTQ
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_ecma_data import ltq_z

z_axis = linspace(0.001, 25, 100)
lth_zwicker = LTQ(z_axis)
lth_roughness = LTQ(z_axis, reference="roughness")

bark_axis = linspace(0.5, 26.5, num=53, endpoint=True)

plt.plot(z_axis, lth_zwicker, label="Zwicker")
plt.plot(z_axis, lth_roughness, label="Roughness")
plt.plot(bark_axis, 20 * log10(array(ltq_z) / 2e-5), label="Ecma")
plt.legend()
plt.show(block=True)

print("done")
