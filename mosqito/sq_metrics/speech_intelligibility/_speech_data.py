from numpy import array

def _get_critical_band_speech_data(speech_level):

    if speech_level == "normal":
        SPEECH_SPECTRUM = array(
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
        ])
        SPEECH_LEVEL = 62.35
    elif speech_level == "raised":
        SPEECH_SPECTRUM = array(
            [
            34.06,
            38.98,
            38.62,
            39.84,
            39.44,
            37.99,
            35.85,
            33.86,
            32.56,
            30.91,
            28.58,
            26.37,
            24.34,
            22.35,
            21.04,
            19.56,
            16.78,
            12.14,
            9.04,
            6.36,
            3.44
            ])
        SPEECH_LEVEL = 68.34
    elif speech_level == "loud":

        SPEECH_SPECTRUM = array(
            [
            34.21,
            41.55,
            43.68,
            44.08,
            45.34,
            45.22,
            43.60,
            42.16,
            41.07,
            39.68,
            37.70,
            35.62,
            33.17,
            30.98,
            29.01,
            27.71,
            25.41,
            19.20,
            15.37,
            12.61,
            9.62
            ])
        SPEECH_LEVEL = 74.85
    elif speech_level == "shout":
        SPEECH_SPECTRUM = array(
        [
        28.69,
        42.50,
        47.14,
        48.46,
        50.17,
        51.68,
        51.43,
        51.31,
        49.40,
        49.03,
        47.65,
        45.47,
        43.13,
        40.80,
        39.15,
        37.30,
        34.41,
        29.01,
        25.17,
        22.08,
        18.76
        ])
        SPEECH_LEVEL = 82.30
    else:
        raise ValueError("Error: available speech levels are {'normal', 'raised', 'loud', 'shout'}")

    return SPEECH_SPECTRUM, SPEECH_LEVEL

def _get_equal_critical_band_speech_data(speech_level):
    if speech_level == "normal":
        SPEECH_SPECTRUM = array(
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
        SPEECH_LEVEL = 62.35
    elif speech_level == "raised":
        SPEECH_SPECTRUM = array(
        [
        38.62,
        39.84,
        39.44,
        37.99,
        35.85,
        33.86,
        32.56,
        30.91,
        28.58,
        26.37,
        24.34,
        22.35,
        21.04,
        19.56,
        16.78,
        12.14,
        9.04,
        ]
    )
        SPEECH_LEVEL = 68.34
    elif speech_level == "loud":
        SPEECH_SPECTRUM = array(
        [
        43.68,
        44.08,
        45.34,
        45.22,
        43.60,
        42.16,
        41.07,
        39.68,
        37.70,
        35.62,
        33.17,
        30.98,
        29.01,
        27.71,
        25.41,
        19.20,
        15.37,
        ]
    )
        SPEECH_LEVEL = 74.85
    elif speech_level == "shout":
        SPEECH_SPECTRUM = array(
        [
        47.14,
        48.46,
        50.17,
        51.68,
        51.43,
        51.31,
        49.40,
        49.03,
        47.65,
        45.47,
        43.13,
        40.80,
        39.15,
        37.30,
        34.41,
        29.01,
        25.17,
        ]
    )
        SPEECH_LEVEL = 82.30
    else:
        raise ValueError("Error: Available speech levels are {'normal', 'raised', 'loud', 'shout'}")

    return SPEECH_SPECTRUM, SPEECH_LEVEL

def _get_octave_band_speech_data(speech_level):

    if speech_level == "normal":
        SPEECH_SPECTRUM = array(
        [
        34.75,
        34.27,
        25.01,
        17.32,
        9.33,
        1.13
        ]
    )
        SPEECH_LEVEL = 62.35
    elif speech_level == "raised":
        SPEECH_SPECTRUM = array(
        [
        38.98,
        40.15,
        33.86,
        25.32,
        16.78,
        5.07
        ]
    )

        SPEECH_LEVEL = 68.34
    elif speech_level == "loud":
        SPEECH_SPECTRUM = array(
        [
        41.55,
        44.85,
        42.16,
        34.39,
        25.41,
        11.39
        ]
    )
        SPEECH_LEVEL = 74.85
    elif speech_level == "shout":
        SPEECH_SPECTRUM = array(
        [
        42.50,
        49.24,
        51.31,
        44.32,
        34.41,
        20.72
        ]
    )
        SPEECH_LEVEL = 82.30
    else:
        raise ValueError("Error: Available speech levels are {'normal', 'raised', 'loud', 'shout'}")

    return SPEECH_SPECTRUM, SPEECH_LEVEL

def _get_third_octave_band_speech_data(speech_level):
    if speech_level == "normal":
        SPEECH_SPECTRUM = array(
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
        SPEECH_LEVEL = 62.35
    elif speech_level == "raised":
        SPEECH_SPECTRUM = array(
        [
        33.81,
        33.92,
        38.98,
        38.57,
        39.11,
        40.15,
        38.78,
        36.37,
        33.86,
        31.89,
        28.58,
        25.32,
        22.35,
        20.15,
        16.78,
        11.47,
        7.67,
        5.07
        ]
    )
        SPEECH_LEVEL = 68.34
    elif speech_level == "loud":
        SPEECH_SPECTRUM = array(
        [
        35.29,
        37.76,
        41.55,
        43.78,
        43.40,
        44.85,
        45.55,
        44.05,
        42.16,
        40.53,
        37.70,
        34.39,
        30.98,
        28.21,
        25.41,
        18.35,
        13.87,
        11.39,
        ]
    )
        SPEECH_LEVEL = 74.85
    elif speech_level == "shout":
        SPEECH_SPECTRUM = array(
        [
        30.77,
        36.65,
        42.50,
        46.51,
        47.40,
        49.24,
        51.21,
        51.44,
        51.31,
        49.63,
        47.65,
        44.32,
        40.80,
        38.13,
        34.41,
        28.24,
        23.45,
        20.72,
        ]
    )
        SPEECH_LEVEL = 82.30
    else:
        raise ValueError("Error: Available speech levels are {'normal', 'raised', 'loud', 'shout'}")
    
    return SPEECH_SPECTRUM, SPEECH_LEVEL

if __name__ == "__main__":
    
    speech_level = "normal"
    speech_spectrum, _ = _get_critical_band_speech_data(speech_level)
    print(len(speech_spectrum))
    speech_spectrum, _ = _get_equal_critical_band_speech_data(speech_level)
    print(len(speech_spectrum))
    speech_spectrum, _ = _get_third_octave_band_speech_data(speech_level)
    print(len(speech_spectrum))
    speech_spectrum, _ = _get_octave_band_speech_data(speech_level)
    print(len(speech_spectrum))
    
    print('done')
