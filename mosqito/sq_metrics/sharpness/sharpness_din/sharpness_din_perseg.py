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
    """Acoustic sharpness calculation according to different methods
        (Aures, Von Bismarck, DIN 45692, Fastl) from a stationary signal.

    Parameters:
    ----------
    signal: numpy.array or DataTime object
        A time signal in [Pa].
    fs : float, optional
        Sampling frequency, can be omitted if the input is a DataTime
        object. Default to None
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'
    nperseg: int, optional
        Length of each segment. Defaults to 4096.
    noverlap: int, optional
        Number of points to overlap between segments.
        If None, noverlap = nperseg / 2. Defaults to None.
    field_type : str
        Type of soundfield corresponding to spec_third ("free" by
        default or "diffuse").
    is_sdt_output : Bool, optional
        If True, the outputs are returned as SciDataTool objects.
        Default to False

    Outputs
    ------
    S : ndarray or DataTime object
        Sharpness value, size(nseg).

    """

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
