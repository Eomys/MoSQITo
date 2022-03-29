# -*- coding: utf-8 -*-

# Local application imports
from mosqito.utils import time_segmentation
from mosqito.sq_metrics.loudness.loudness_zwst.loudness_zwst import loudness_zwst

# Optional package import
try:
    from SciDataTool import DataTime, DataLinspace, DataFreq
except ImportError:
    DataTime = None
    DataLinspace = None
    DataFreq = None


def loudness_zwst_perseg(
    signal, fs=None, nperseg=4096, noverlap=None, field_type="free", is_sdt_output=False
):
    """Zwicker-loudness calculation for stationary signals

    Calculates the acoustic loudness according to Zwicker method for
    stationary signals per signal segment.
    Normatice reference:
        ISO 532:1975 (method B)
        DIN 45631:1991
        ISO 532-1:2017 (method 1)
    The code is based on BASIC program published in "Program for
    calculating loudness according to DIN 45631 (ISO 532B)", E.Zwicker
    and H.Fastl, J.A.S.J (E) 12, 1 (1991).
    Note that due to normative continuity, as defined in the
    preceeding standards, the method is in accordance with
    ISO 226:1987 equal loudness contours (instead of ISO 226:2003)

    Parameters
    ----------
    signal : numpy.array
        Time signal values [Pa].
    fs : float, optional
        Sampling frequency, can be omitted if the input is a DataTime
        object. Default to None
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
    -------
    N : float
        The overall loudness array [sones], size (Ntime,).
    N_specific : numpy.ndarray
        The specific loudness array [sones/bark], size (Nbark, Ntime).
    bark_axis: numpy.array
        The Bark axis array, size (Nbark,).
    time_axis: numpy.array
        The time axis array, size (Ntime,) or None.

    """

    # Manage input type
    if DataTime is not None and isinstance(signal, DataTime):
        time = signal.get_along("time")["time"]
        fs = 1 / (time[1] - time[0])
        signal = signal.get_along("time")[signal.symbol]

    # Time signal segmentation
    signal, time_axis = time_segmentation(signal, fs, nperseg, noverlap)

    # Compute loudness
    N, N_specific, bark_axis = loudness_zwst(signal, fs, field_type="free")

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
            )
            time = DataLinspace(
                name="time",
                unit="s",
                initial=0,
                final=time_axis[-1],
                number=len(time_axis),
                include_endpoint=True,
            )
            N_specific = DataFreq(
                name="Specific Loudness",
                symbol="N'_{zwst}",
                axes=[bark_data, time],
                values=N_specific,
                unit="sone/Bark",
            )
            N = DataTime(
                name="Loudness",
                symbol="N_{zwst}",
                axes=[time],
                values=N,
                unit="sone",
            )

    return N, N_specific, bark_axis, time_axis
