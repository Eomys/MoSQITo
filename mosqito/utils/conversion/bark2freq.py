from numpy import arange, array, interp

def bark2freq(bark_axis):
    """Frequency conversion from Bark to Hertz
    
    This function does the frequency conversion between bark and hertz.
    See reference, coefficients are linearly interpolated from the values given in table 6.1.
    
    Parameters
    ----------
    bark_axis : array_like
        Bark frequencies to be converted.

    Returns
    -------
    freq_axis : array_like
        Frequencies converted in Hertz.
                 
    References
    ----------
    ..[ZF] E. Zwicker, H. Fastl: Psychoacoustics. Springer,Berlin, Heidelberg, 1990.
     The coefficients are linearly interpolated from the values given in table 6.1.
    """

    xp = arange(0, 25, 0.5)

    yp = array(
        [
            0,
            50,
            100,
            150,
            200,
            250,
            300,
            350,
            400,
            450,
            510,
            570,
            630,
            700,
            770,
            840,
            920,
            1000,
            1080,
            1170,
            1270,
            1370,
            1480,
            1600,
            1720,
            1850,
            2000,
            2150,
            2320,
            2500,
            2700,
            2900,
            3150,
            3400,
            3700,
            4000,
            4400,
            4800,
            5300,
            5800,
            6400,
            7000,
            7700,
            8500,
            9500,
            10500,
            12000,
            13500,
            15500,
            20000,
        ]
    )

    return interp(bark_axis, xp, yp)