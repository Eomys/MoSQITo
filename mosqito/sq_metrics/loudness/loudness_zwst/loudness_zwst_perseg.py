# -*- coding: utf-8 -*-

# Local application imports
from mosqito.utils import time_segmentation
from mosqito.sq_metrics.loudness.loudness_zwst.loudness_zwst import loudness_zwst

# Optional package import
try:
    from SciDataTool import DataTime, DataLinspace, DataFreq, Norm_func
except ImportError:
    DataTime = None
    DataLinspace = None
    DataFreq = None


def loudness_zwst_perseg(
    signal, fs=None, nperseg=4096, noverlap=None, field_type="free", is_sdt_output=False
):
    """
    Returns the loudness value 

    This function computes the acoustic loudness according to Zwicker method by segmentation
    of a stationary signal.

    Parameters:
    ------------
    signal: array_like
        Input time signal in [Pa].
    fs : float, optional
        Sampling frequency, can be omitted if the input is a DataTimeobject. 
        Default to None
    nperseg: int, optional
        Length of each segment. Defaults to 4096.
    noverlap: int, optional
        Number of points to overlap between segments.
        If None, noverlap = nperseg / 2. Defaults to None.
    field_type : {'free', 'diffuse'}
        Type of soundfield.
        Default is 'free'
    is_sdt_output : Bool, optional
        If True, the outputs are returned as SciDataTool objects.
        Default to False
        
    Returns
    --------
    N : float
        Overall loudness [sones], size (Ntime,). 
    N_specific : numpy.ndarray
        Specific loudness [sones/bark], size (Nbark, Ntime).
    bark_axis : numpy.ndarray
        Bark axis, size (Nbark,).
    time_axis : numpy.ndarray
        Time axis, size (Ntime,).

    See Also
    ---------
    loudness_zwst : Loudness computation for a stationary time signal
    loudness_zwst_freq : Loudness computation from a sound spectrum
    loudness_zwtv : Loudness computation for a non-stationary time signal

    Notes
    ------
    Normative reference:
        ISO 532:1975 (method B)
        DIN 45631:1991
        ISO 532-1:2017 (method 1)
    Due to normative continuity, as defined in the preceeding standards, the method is in accordance with
    ISO 226:1987 equal loudness contours (instead of ISO 226:2003).
    
    References
    -----------
    :cite:empty:`L_zw-ZF91`

    .. bibliography::
        :keyprefix: L_zw-
                    
    Examples
    ---------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import loudness_zwst_perseg
       >>> import matplotlib.pyplot as plt
       >>> import numpy as np
       >>> fs=48000
       >>> d=1
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> f = np.linspace(1000,5000, len(time))
       >>> stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> N, N_spec, bark_axis, time_axis = loudness_zwst_perseg(stimulus, fs=fs)
       >>> plt.plot(time_axis, N)
       >>> plt.xlabel("Time [s]")
       >>> plt.ylabel("Loudness [Sone]")
    """    
    if fs < 48000:
        print("[Warning] Signal resampled to 48 kHz to allow calculation. To fulfill the standard requirements fs should be >=48 kHz."
             )
        from scipy.signal import resample
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000
    

    # Manage input type
    if DataTime is not None and isinstance(signal, DataTime):
        time = signal.get_along("time")["time"]
        fs = 1 / (time[1] - time[0])
        signal = signal.get_along("time")[signal.symbol]

    # Time signal segmentation
    signal, time_axis = time_segmentation(signal, fs, nperseg, noverlap)

    # Compute loudness
    N, N_specific, bark_axis = loudness_zwst(signal, fs, field_type=field_type)

    # Manage SciDataTool output type
    if is_sdt_output:
        if DataLinspace is None:
            raise RuntimeError(
                "In order to handle Data objects you need the 'SciDataTool' package."
            )
        else:
            bark_data = DataLinspace(
                name="Critical band rate",
                unit="Bark",
                initial=0,
                final=24,
                number=int(24 / 0.1),
                include_endpoint=True,
                normalizations={
                    "Hz": Norm_func(function=lambda x: 1960 * (x + 0.53) / (26.28 - x))
                },
            )
            time = DataLinspace(
                name="time",
                unit="s",
                initial=time_axis[0],
                final=time_axis[-1],
                number=len(time_axis),
                include_endpoint=True,
            )
            N_specific = DataFreq(
                name="Specific loudness (Zwicker method for stationnary signal)",
                symbol="N'_{zwst}",
                axes=[bark_data, time],
                values=N_specific,
                unit="sone/Bark",
            )
            N = DataTime(
                name="Loudness (Zwicker method for stationnary signal)",
                symbol="N_{zwst}",
                axes=[time],
                values=N,
                unit="sone",
            )

    return N, N_specific, bark_axis, time_axis

