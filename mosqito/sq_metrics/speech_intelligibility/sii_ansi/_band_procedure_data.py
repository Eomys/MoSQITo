from numpy import array

def _get_critical_band_data():
    """ See § 3.4 of the standard ANSI S3.5. """
    CENTER_FREQUENCIES = array(
        [
            150,
            250,
            350,
            450,
            570,
            700,
            840,
            1000,
            1170,
            1370,
            1600,
            1850,
            2150,
            2500,
            2900,
            3400,
            4000,
            4800,
            5800,
            7000,
            8500
        ]
    )

    LOWER_FREQUENCIES = array(
        [
            100,
            200,
            300,
            400,
            510,
            630,
            770,
            920,
            1080,
            1270,
            1480,
            1720,
            2000,
            2320,
            2700,
            3150,
            3700,
            4400,
            5300,
            6400,
            7700
        ]
    )

    UPPER_FREQUENCIES = array(
        [
            200,
            300,
            400,
            510,
            630,
            770,
            920,
            1080,
            1270,
            1480,
            1720,
            2000,
            2320,
            2700,
            3150,
            3700,
            4400,
            5300,
            6400,
            7700,
            9500
        ]
    )
    
    IMPORTANCE = array(
        [
            0.0103,
            0.0261,
            0.0419,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0577,
            0.0460,
            0.0343,
            0.0226,
            0.0110
        ]
    )
    
    STANDARD_SPEECH_SPECTRUM_NORMAL = array(
        [
            31.44,
            34.75,
            34.14,
            34.58,
            33.17,
            30.64,
            27.59,
            25.01,
            23.52,
            22.28,
            20.15,
            18.29,
            16.37,
            13.80,
            12.21,
            11.09,
            9.33,
            5.84,
            3.47,
            1.78,
            -0.14
        ]
    )

    REFERENCE_INTERNAL_NOISE_SPECTRUM = array(
        [
            1.50,
            -3.90,
            -7.20,
            -8.90,
            -10.30,
            -11.40,
            -12.00,
            -12.50,
            -13.20,
            -14.00,
            -15.40,
            -16.90,
            -18.80,
            -21.20,
            -23.20,
            -24.90,
            -25.90,
            -24.20,
            -19.00,
            -11.70,
            -6.00
        ]
    )

    FREEFIELD2EARDRUM_TRANSFER_FUNCTION = array(
        [
        0.60,
        1.00,
        1.40,
        1.40,
        1.90,
        2.80,
        3.00,
        2.60,
        2.60,
        3.60,
        6.10,
        10.50,
        13.80,
        16.80,
        15.80,
        14.90,
        14.30,
        12.40,
        7.90,
        4.30,
        0.50
        ]
    )
    return CENTER_FREQUENCIES, LOWER_FREQUENCIES, UPPER_FREQUENCIES, IMPORTANCE, REFERENCE_INTERNAL_NOISE_SPECTRUM, STANDARD_SPEECH_SPECTRUM_NORMAL

def _get_equal_critical_band_data():
    CENTER_FREQUENCIES = array(
        [
        350,
        450,
        570,
        700,
        840,
        1000,
        1170,
        1370,
        1600,
        1850,
        2150,
        2500,
        2900,
        3400,
        4000,
        4800,
        5800,
        ]
    )

    LOWER_FREQUENCIES = array(
        [
        300,
        400,
        510,
        630,
        770,
        920,
        1080,
        1270,
        1480,
        1720,
        2000,
        2320,
        2700,
        3150,
        3700,
        4400,
        5300,
        ]
    )

    UPPER_FREQUENCIES = array(
        [
        400,
        510,
        630,
        770,
        920,
        1080,
        1270,
        1480,
        1720,
        2000,
        2320,
        2700,
        3150,
        3700,
        4400,
        5300,
        6400
        ]
    )

    IMPORTANCE = array(
        [
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        0.0588,
        ]
    )

    STANDARD_SPEECH_SPECTRUM_NORMAL = array(
        [
            34.14,
            34.58,
            33.17,
            30.64,
            27.59,
            25.01,
            23.52,
            22.28,
            20.15,
            18.29,
            16.37,
            13.80,
            12.21,
            11.09,
            9.33,
            5.84,
            3.47,
        ]
    )


    REFERENCE_INTERNAL_NOISE_SPECTRUM = array(
        [
            -7.20,
            -8.90,
            -10.30,
            -11.40,
            -12.00,
            -12.50,
            -13.20,
            -14.00,
            -15.40,
            -16.90,
            -18.80,
            -21.20,
            -23.20,
            -24.90,
            -25.90,
            -24.20,
            -19.00,
        ]
    )

    FREEFIELD2EARDRUM_TRANSFER_FUNCTION = array(
        [
        1.40,
        1.40,
        1.90,
        2.80,
        3.00,
        2.60,
        2.60,
        3.60,
        6.10,
        10.50,
        13.80,
        16.80,
        15.80,
        14.90,
        14.30,
        12.40,
        7.90,
        ]
    )
    return CENTER_FREQUENCIES, LOWER_FREQUENCIES, UPPER_FREQUENCIES, IMPORTANCE, REFERENCE_INTERNAL_NOISE_SPECTRUM, STANDARD_SPEECH_SPECTRUM_NORMAL

def _get_octave_band_data():
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
    return CENTER_FREQUENCIES, LOWER_FREQUENCIES, UPPER_FREQUENCIES, BANDWIDTH_ADJUSTEMENT, IMPORTANCE, REFERENCE_INTERNAL_NOISE_SPECTRUM, STANDARD_SPEECH_SPECTRUM_NORMAL

def _get_third_octave_band_data():
    CENTER_FREQUENCIES = array(
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
        8000
        ]
        )

    LOWER_FREQUENCIES = array(
        [
        141,
        178,
        224,
        282,
        355,
        447,
        562,
        708,
        891,
        1122,
        1413,
        1778,
        2239,
        2818,
        3548,
        4467,
        5623,
        7079,
        ]
        )

    UPPER_FREQUENCIES = array(
        [
        178,
        224,
        282,
        355,
        447,
        562,
        708,
        891,
        1122,
        1413,
        1778,
        2239,
        2818,
        3548,
        4467,
        5623,
        7079,
        8913,
        ]
        )

    BANDWIDTH_ADJUSTEMENT = array(
        [
        15.65,
        16.65,
        17.65,
        18.65,
        19.65,
        20.65,
        21.65,
        22.65,
        23.65,
        24.65,
        25.65,
        26.65,
        27.65,
        28.65,
        29.65,
        30.65,
        31.65,
        32.65,
        ]
    )    

    IMPORTANCE = array(
        [
        0.0083,
        0.0095,
        0.0150,
        0.0289,
        0.0440,
        0.0578,
        0.0653,
        0.0711,
        0.0818,
        0.0844,
        0.0882,
        0.0898,
        0.0868,
        0.0844,
        0.0771,
        0.0527,
        0.0364,
        0.0185,
        ]
    )

    STANDARD_SPEECH_SPECTRUM_NORMAL = array (
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
        1.13    ]
    )

    REFERENCE_INTERNAL_NOISE_SPECTRUM = array(
        [
        0.60,
        -1.70,
        -3.90,
        -6.10,
        -8.20,
        -9.70,
        -10.80,
        -11.90,
        -12.50,
        -13.50,
        -15.40,
        -17.70,
        -21.20,
        -24.20,
        -25.90,
        -23.60,
        -15.80,
        -7.10
        ]
    )

    FREEFIELD2EARDRUM_TRANSFER_FUNCTION = array(
        [
        0.00,
        0.50,
        1.00,
        1.40,
        1.50,
        1.80,
        2.40,
        3.10,
        2.60,
        3.00,
        6.10,
        12.00,
        16.80,
        15.00,
        14.30,
        10.70,
        6.40,
        1.80,
        ]
    )
    return CENTER_FREQUENCIES, LOWER_FREQUENCIES, UPPER_FREQUENCIES, BANDWIDTH_ADJUSTEMENT, IMPORTANCE, REFERENCE_INTERNAL_NOISE_SPECTRUM, STANDARD_SPEECH_SPECTRUM_NORMAL
