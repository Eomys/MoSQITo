# -*- coding: utf-8 -*-

# Standard imports
import numpy as np

# Local imports
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sq_metrics.roughness.roughness_dw._roughness_dw_main_calc import (
    _roughness_dw_main_calc,
)
from mosqito.sq_metrics.roughness.roughness_dw._gzi_weighting import _gzi_weighting
from mosqito.sq_metrics.roughness.roughness_dw._H_weighting import _H_weighting

# Optional package import
try:
    from SciDataTool import DataTime, DataLinspace, DataFreq, Norm_func
except ImportError:
    DataTime = None
    DataLinspace = None
    DataFreq = None


def roughness_dw(signal, fs=None, overlap=0.5, is_sdt_output=False):
    """
    Returns the roughness according to Daniel and Weber method.

    This function computes the global and specific roughness values 
    of a signal sampled at 48 kHz.

    Parameters
    ----------
    signal : array_like or DataTime object
        Input time signal in Pa
    fs : float, optional
        Sampling frequency, can be omitted if the input is a DataTime
        object. Default to None
    overlap : float
        Overlapping coefficient for the time windows of 200ms

    Returns
    -------
    R : numpy.array
        Roughness value in [asper]
    R_spec : numpy.array
        Specific roughness over bark axis
    bark_axis : numpy.array
        Frequency axis in [bark]
    time : numpy.array
        Time axis in [s]

    Raises
    ------
    IndexError
        If `axis` is not a valid axis of `a`.

    See Also
    --------
    roughness_dw_freq : roughness computation from a sound spectrum

    Notes
    -----
    The model consists of a parallel processing structure that is made up
    of successive stages and calculates intermediate specific roughnesses R_spec,
    which are summed up to determine the total roughness R.

    References
    ----------
    .. [DW] P. Daniel and R. Weber, "Psychoacoustical roughness: 
            implementation of an optimized model", 1997

    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import roughness_dw 
       >>> import matplotlib.pyplot as plt
       >>> fc=1000
       >>> fmod=70
       >>> fs=44100
       >>> d=0.2
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> stimulus = (0.5 * (1 + np.sin(2 * np.pi * fmod * time))* np.sin(2 * np.pi * fc * time))   
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> R, R_specific, bark, time = roughness_dw(stimulus, fs=44100, overlap=0)
       >>> plt.plot(bark, R_specific)
       >>> plt.xlabel("Bark axis [Bark]")
       >>> plt.ylabel("Specific roughness [Asper/Bark]")
       >>> plt.title("Roughness = " + f"{R[0]:.2f}" + " [Asper]")
    """

    # Manage input type
    if DataTime is not None and isinstance(signal, DataTime):
        time = signal.get_along("time")["time"]
        fs = 1 / (time[1] - time[0])
        signal = signal.get_along("time")[signal.symbol]

    # Number of points within each frame according to the time resolution of 200ms
    nperseg = int(0.2 * fs)
    # Overlapping segment length
    noverlap = int(overlap * nperseg)
    # reshaping of the signal according to the overlap and time proportions
    sig, time = time_segmentation(
        signal, fs, nperseg=nperseg, noverlap=noverlap, is_ecma=False
    )
    if len(sig.shape) == 1:
        nseg = 1
    else:
        nseg = sig.shape[1]

    spec, _ = spectrum(sig, fs, nfft="default", window="blackman", db=False)

    # Frequency axis in Hertz
    freq_axis = np.arange(1, nperseg // 2 + 1, 1) * (fs / nperseg)

    # Initialization of the weighting functions H and g
    hWeight = _H_weighting(nperseg, fs)
    # Aures modulation depth weighting function
    gzi = _gzi_weighting(np.arange(1, 48, 1) / 2)

    R = np.zeros((nseg))
    R_spec = np.zeros((47, nseg))
    if len(spec.shape) > 1:
        for i in range(nseg):
            R[i], R_spec[:, i], bark_axis = _roughness_dw_main_calc(
                spec[:, i], freq_axis, fs, gzi, hWeight
            )
    else:
        R, R_spec, bark_axis = _roughness_dw_main_calc(
            spec, freq_axis, fs, gzi, hWeight
        )

    # print(np.mean(R,axis=0))

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
                initial=bark_axis[0],
                final=bark_axis[-1],
                number=len(bark_axis),
                include_endpoint=True,
                normalizations={
                    "Hz": Norm_func(function=lambda x: 1960 * (x + 0.53) / (26.28 - x))
                },
            )
            time = DataLinspace(
                name="time",
                unit="s",
                initial=time[0],
                final=time[-1],
                number=len(time),
                include_endpoint=True,
            )
            R_spec = DataFreq(
                name="Specific roughness (Daniel & Weber method)",
                symbol="R'_{dw}",
                axes=[bark_data, time],
                values=R_spec,
                unit="asper/Bark",
            )
            R = DataTime(
                name="Roughness (Daniel & Weber method)",
                symbol="R_{dw}",
                axes=[time],
                values=R,
                unit="asper",
            )

    return R, R_spec, bark_axis, time
