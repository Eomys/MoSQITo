# -*- coding: utf-8 -*-

"""Frame-wise Aures tonality. The model is in ``tonality_aures_st.py``."""

import numpy as np

from mosqito.sq_metrics.tonality.tonality_aures.tonality_aures_st import (
    FREQ_RESOLUTION,
    _aures_analysis,
    _calibration_constant,
)


def tonality_aures_tv(signal, fs, field_type="free", frame_length=0.25, hop=0.125):
    """
    Compute the Aures tonality of a time-varying signal, frame by frame.

    Each frame is analysed exactly as :func:`tonality_aures_st` analyses a whole
    signal (same spectrum, component extraction, weightings and calibration),
    which gives the tonality K in [t.u.] of the sound as if it were stationary
    within the frame. Aures (1985) defines the method for stationary sounds
    and gives no rule for a time series; this function is the frame-wise
    reading of the model, the single value of :func:`tonality_aures_st` is its
    whole-signal reading, and the latter is not the mean of the former.

    Parameters
    ----------
    signal : array_like
        Input time signal in [Pa], one-dimensional.
    fs : float
        Sampling frequency in [Hz].
    field_type : {'free', 'diffuse'}, optional
        Sound field of the Zwicker loudness computation (ISO 532-1). Default
        is 'free'.
    frame_length : float, optional
        Length of the analysis frames in [s]. Default is 0.25 s. A frame must
        hold at least one segment of the spectral analysis (80 ms, the
        12.5 Hz resolution of Terhardt et al. 1982).
    hop : float, optional
        Time between the starts of consecutive frames in [s]. Default is
        0.125 s. The defaults are the frames of the SQAT toolbox, so the two
        implementations can be compared frame by frame.

    Returns
    -------
    K : numpy.ndarray
        Tonality of each frame in [t.u.].
    time : numpy.ndarray
        Time of the centre of each frame in [s].

    Notes
    -----
    What the framing changes, and what to keep in mind:

    * The spectrum of a frame is the Welch average of its 80 ms segments
      (12.5 Hz lines, Hamming window, 50 % overlap): a 250 ms frame averages
      5 segments where a 2 s signal averages 49. The noise floor read by the
      extraction of narrowband regions is therefore rougher, and K of a frame
      of noise scatters more than the whole-signal value. Longer frames
      average more, shorter frames follow the sound more closely.
    * The loudness N and N_Gr of a frame is the stationary loudness
      (ISO 532-1) of the frame's spectrum, not the time-varying loudness with
      its temporal integration.
    * Frames are not windowed as a whole, only their segments are. Frames run
      from the start of the signal, a last part shorter than a frame is
      dropped, and a signal shorter than a frame is analysed as one frame.
    * The calibration constant is the one of :func:`tonality_aures_st`: the Welch
      spectrum of the reference tone is the same in a frame as over a second,
      so a frame of the reference tone gives exactly 1 t.u.
    * A tone present during part of the signal gives a high K in its frames
      and a lower whole-signal value, where its power is averaged with the
      noise of the rest of the signal; both readings are correct, for
      different questions. Periodic test signals deserve care: a sum of
      sinusoids whose phases are linear in the line index is a pulse train,
      and its frames do not look like its long-term spectrum.

    References
    ----------
    :cite:empty:`T_aures_tv-Aures1985`
    :cite:empty:`T_aures_tv-Terhardt1982`

    .. bibliography::
        :keyprefix: T_aures_tv-

    Examples
    --------
    .. plot::
       :include-source:

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from mosqito.sq_metrics import tonality_aures_tv
        >>> from mosqito.utils import sine_wave_generator
        >>> fs = 48000
        >>> noise = np.random.default_rng(0).standard_normal(2 * fs)
        >>> noise = noise * 2e-5 * 10 ** (50 / 20) / np.std(noise)
        >>> tone = sine_wave_generator(fs, 2, 1000, 60)[0]
        >>> tone[: fs] = 0  # the tone starts after one second
        >>> K, time = tonality_aures_tv(noise + tone, fs)
        >>> plt.step(time, K, where="mid")
        >>> plt.xlabel("Time [s]")
        >>> plt.ylabel("Tonality [t.u.]")
    """

    signal = np.asarray(signal, dtype=float).squeeze()
    if signal.ndim != 1:
        raise ValueError("signal must be a one-dimensional array")
    if signal.size == 0:
        raise ValueError("signal must not be empty")
    if fs <= 0:
        raise ValueError("fs must be positive")
    n_frame = int(round(frame_length * fs))
    n_hop = int(round(hop * fs))
    n_segment = int(round(fs / FREQ_RESOLUTION))
    if n_frame < n_segment:
        raise ValueError(
            f"frame_length must be at least {n_segment / fs:.3f} s, one segment of the spectral analysis"
        )
    if n_hop < 1:
        raise ValueError("hop must be positive")

    if signal.size < n_frame:
        n_frame = signal.size
    starts = np.arange(0, signal.size - n_frame + 1, n_hop)

    c = _calibration_constant(fs, field_type)
    tonality = np.array(
        [c * _aures_analysis(signal[start : start + n_frame], fs, field_type)["K_raw"] for start in starts]
    )
    time = (starts + n_frame / 2) / fs
    return tonality, time
