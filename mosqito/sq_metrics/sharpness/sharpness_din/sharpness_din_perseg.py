# -*- coding: utf-8 -*-

# Local imports
from mosqito.sq_metrics import loudness_zwst_perseg
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import (
    sharpness_din_from_loudness,
)

# Optional package import
try:
    from SciDataTool import DataTime, DataLinspace, DataFreq, Norm_func
except ImportError:
    DataTime = None
    DataLinspace = None
    DataFreq = None


def sharpness_din_perseg(
    signal,
    fs=None,
    weighting="din",
    nperseg=4096,
    noverlap=None,
    field_type="free",
    is_sdt_output=False,
):
    """
    Returns the sharpness value 

    This function computes the sharpness value according to different methods.

    Parameters
    ----------
    signal: array_like
        Input time signal in [Pa]
    fs : float, optional
        Sampling frequency, can be omitted if the input is a DataTime
        object. Default to None
    weighting : {'din', 'aures', 'bismarck', 'fastl'}
        Weighting function used for the sharpness computation. 
        Default is 'din'
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
    -------
    S : numpy.array
        Sharpness value in [acum], dim (nseg)
    time_axis : numpy.array
        Time axis in [s]

    See Also
    --------
    .sharpness_din_from_loudness : Sharpness computation from loudness values
    .sharpness_din_tv : Sharpness computation for a non-stationary time signal
    .sharpness_din_st : Sharpness computation for a stationary time signal
    .sharpness_din_freq : Sharpness computation from a sound spectrum

    Warning
    -------
    The sampling frequency of the signal must be >= 48 kHz to fulfill requirements.
    If the provided signal doesn't meet the requirements, it will be resampled.

    Notes
    -----
    For each segment considered, the computation consists of a specific loudness weighting employing a weighting function :math:`g(z)`:
    
    .. math::
        S=0.11\\frac{\\int_{0}^{24Bark}N'(z)g(z)\\textup{dz}}{N}
        
    with :math:`N'` the specific loudness and :math:`N` the global loudness.
    
    The different methods available with the function account for the weighting function applied:
     * DIN 45692 : weighting defined in the standard
     * Aures
     * Bismarck
     * Fastl

    References
    ----------
    :cite:empty:`S-DIN.45692:2009`
    :cite:empty:`S-ZF:9`
    :cite:empty:`S-B74`
    
    .. bibliography::
        :keyprefix: S-

    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import sharpness_din_perseg
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
       >>> S, time_axis = sharpness_din_perseg(stimulus, fs=fs)
       >>> plt.plot(time_axis, S)
       >>> plt.xlabel("Time [s]")
       >>> plt.ylabel("Sharpness [Acum]")
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

    # Compute loudness
    N, N_specific, _, time_axis = loudness_zwst_perseg(
        signal, fs, nperseg=nperseg, noverlap=noverlap, field_type=field_type
    )

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(N, N_specific, weighting=weighting)

    # Manage SciDataTool output type
    if is_sdt_output:
        if DataLinspace is None:
            raise RuntimeError(
                "In order to handle Data objects you need the 'SciDataTool' package."
            )
        else:
            time = DataLinspace(
                name="time",
                unit="s",
                initial=time_axis[0],
                final=time_axis[-1],
                number=len(time_axis),
                include_endpoint=True,
            )
            S = DataTime(
                name="Sharpness (DIN 45692)",
                symbol="S_{DIN}",
                axes=[time],
                values=S,
                unit="acum",
            )

    return S, time_axis
