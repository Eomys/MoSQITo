from numpy import array

CENTER_FREQUENCIES = array(
    [
    250,
    500,
    1000,
    2000,
    4000,
    8000,
    ]
)

LOWER_FREQUENCIES = array(
    [
    177,
    355,
    710,
    1420,
    2840,
    5680,
    ]
)

UPPER_FREQUENCIES = array(
    [
    355,
    710,
    1420,
    2840,
    5680,
    11360,
    ]
)

BANDWIDTH_ADJUSTEMENT = array(
    [
    22.48,
    25.48,
    28.48,
    31.48,
    34.48,
    37.48,
    ]
)    


IMPORTANCE = array(
    [
    0.0617,
    0.1671,
    0.2373,
    0.2648,
    0.2142,
    0.0549
    ]
)

STANDARD_SPEECH_SPECTRUM_NORMAL = array(
    [
    34.75,
    34.27,
    25.01,
    17.32,
    9.33,
    1.13
    ]
)

OVERALL_SPEECH_LEVEL_NORMAL = 62.35

STANDARD_SPEECH_SPECTRUM_RAISED = array(
    [
    38.98,
    40.15,
    33.86,
    25.32,
    16.78,
    5.07
    ]
)

OVERALL_SPEECH_LEVEL_RAISED = 68.34

STANDARD_SPEECH_SPECTRUM_LOUD = array(
    [
    41.55,
    44.85,
    42.16,
    34.39,
    25.41,
    11.39
    ]
)

OVERALL_SPEECH_LEVEL_LOUD = 74.85

STANDARD_SPEECH_SPECTRUM_SHOUT = array(
    [
    42.50,
    49.24,
    51.31,
    44.32,
    34.41,
    20.72
    ]
)

OVERALL_SPEECH_LEVEL_SHOUT = 82.30

REFERENCE_INTERNAL_NOISE_SPECTRUM = array(
    [
    -3.90,
    -9.70,
    -12.50,
    -17.70,
    -25.90,
    -7.10
    ]
)

FREEFIELD2EARDRUM_TRANSFER_FUNCTION = array(
    [
    1.00,
    1.80,
    2.60,
    12.00,
    14.30,
    1.80
    ]
)


