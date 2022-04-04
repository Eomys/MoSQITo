# -*- coding: utf-8 -*-

# Third party imports
import numpy as np

# Local application imports
from mosqito.sound_level_meter import noct_spectrum
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import _main_loudness
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import _calc_slopes
from mosqito.utils.conversion import amp2db

# Optional package import
try:
    from SciDataTool import DataTime, DataLinspace, DataFreq
except ImportError:
    DataTime = None
    DataLinspace = None
    DataFreq = None


def loudness_zwst(signal, fs=None, field_type="free", is_sdt_output=False):
    """Zwicker-loudness calculation for stationary signals

    Calculates the acoustic loudness according to Zwicker method for
    stationary signals.
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
    signal : numpy.array or DataTime object
        Signal time values [Pa]
    fs : float, optional
        Sampling frequency, can be omitted if the input is a DataTime
        object. Default to None
    field_type : str
        Type of soundfield corresponding to spec_third ("free" by
        default or "diffuse").
    is_sdt_output : Bool, optional
        If True, the outputs are returned as SciDataTool objects.
        Default to False

    Outputs
    -------
    N : float or numpy.array
        The overall loudness array [sones], size (Ntime,).
    N_specific : numpy.ndarray or DataFreq object
        The specific loudness array [sones/bark], size (Nbark, Ntime).
    bark_axis: numpy.array
        The Bark axis array, size (Nbark,).
    """

    # Manage SciDataTool input type
    if DataTime is not None and isinstance(signal, DataTime):
        time = signal.get_along("time")["time"]
        fs = 1 / (time[1] - time[0])
        signal = signal.get_along("time")[signal.symbol]

    # Compute third octave band spectrum
    spec_third, _ = noct_spectrum(signal, fs, fmin=24, fmax=12600)

    # Compute dB values
    spec_third = amp2db(spec_third, ref=2e-5)

    # Compute main loudness
    Nm = _main_loudness(spec_third, field_type)

    # Computation of specific loudness pattern and integration of overall
    # loudness by attaching slopes towards higher frequencies
    N, N_specific = _calc_slopes(Nm)

    # Define Bark axis
    bark_axis = np.linspace(0.1, 24, int(24 / 0.1))

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
            N_specific = DataFreq(
                name="Specific Loudness",
                symbol="N'_{zwst}",
                axes=[bark_data],
                values=N_specific,
                unit="sone/Bark",
            )

    return N, N_specific, bark_axis
