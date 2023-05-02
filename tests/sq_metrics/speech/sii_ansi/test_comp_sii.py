from numpy import array
import matplotlib.pyplot as plt
from mosqito.sq_metrics.speech.sii_ansi.comp_sii import comp_sii

# Inputs to compute the speech intelligibility index
freq_vector = array(
    [
        160,
        200,
        250,
        315,
        400,
        500,
        630,
        800,
        1000,
        1250,
        1600,
        2000,
        2500,
        3150,
        4000,
        5000,
        6300,
        8000,
    ]
)

y_speech = array(
    [
        32.41,
        34.48,
        34.75,
        33.98,
        34.59,
        34.27,
        32.06,
        28.30,
        25.01,
        23.00,
        20.15,
        17.32,
        13.18,
        11.55,
        9.33,
        5.31,
        2.59,
        1.13,
    ]
)

y_speech_2 = array(
    [54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54]
)


y_noise = array(
    [
        0.00,
        0.00,
        10.00,
        20.00,
        30.00,
        33.00,
        40.00,
        36.00,
        22.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
    ]
)

y_noise_2 = array(
    [
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
    ]
)

speech_vect = array(10 ** (y_speech / 20) * 2e-5, dtype=complex)
noise_vect = array(10 ** (y_noise / 20) * 2e-5, dtype=complex)

# Computing speech intelligibility index for the speech and noise given

sii_from_speech, sii_spec_from_speech = comp_sii(
    method="third_octave_bands",
    noise=noise_vect,
    speech_type=speech_vect,
    threshold=None,
)
sii_from_noise, sii_spec_from_noise = comp_sii(
    method="third_octave_bands",
    noise=noise_vect,
    speech_type="normal",
    threshold="zwicker",
)

# Plotting results
plt.figure()
plt.bar(
    freq_vector,
    sii_from_noise,
    color="#0097BA",
    label="Standard ANSI S3.5",
)
# plt.bar(
#     freq_vector ,
#     ref,
#     width=width,
#     color="#A5D867",
#     label="SQMetrics",
# )
plt.xlabel("Frequency [Hz]")
plt.ylabel("Specific values")
plt.legend(fontsize=12)
title = "Global SII"  # = %.3f" % (sum(sii_from_noise)) + ", standard = 0.996"
plt.title(title, fontsize=14)
plt.show()
print("done")
