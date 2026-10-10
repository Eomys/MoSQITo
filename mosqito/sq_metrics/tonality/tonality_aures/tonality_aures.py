# -*- coding: utf-8 -*-

"""Aures tonality, implemented from W. Aures, Acustica 59 (1985) 130-141, section 2.3.

The tonal component extraction, the masking slopes and the threshold in quiet
come from the pitch analysis of Terhardt, Stoll and Seewann, J. Acoust. Soc.
Am. 71 (1982) 679-688, which Aures' method builds on. Equation numbers in the
comments refer to Aures (1985) unless stated otherwise.
"""

import numpy as np
from scipy.signal import welch, get_window

from mosqito.sq_metrics.loudness.loudness_zwst.loudness_zwst_freq import (
    loudness_zwst_freq,
)


P_REF = 2e-5  # Pa
FREQ_RESOLUTION = 12.5  # Hz, spectral resolution of Terhardt et al. (1982)
TONAL_THRESHOLD = 7.0  # dB, Terhardt et al. (1982) and Aures section 2.3.2
LOBE_HALF_WIDTH = 2  # bins, main lobe of the Hamming window
SINUSOID_MAX_WIDTH = 1.8  # bins, -3 dB width of a peak that still reads as a sinusoid
F_MIN = 20.0  # Hz, lower limit of the component search
MAX_REGIONS = 20  # narrowband regions extracted at most
MAX_REGION_WIDTH = 1.5  # Bark; Fig. 6 of Aures follows Gl. (7) up to 1.4 Bark
REFERENCE_TONE = (1000.0, 60.0)  # Hz, dB SPL: the sound with K = 1 (p. 137)

_calibration = {}


def tonality_aures(signal, fs, field_type="free"):
    """
    Compute the Aures tonality of a stationary signal.

    Tonality (Klanghaftigkeit) K in tonality units [t.u.] according to Aures
    (1985), section 2.3, with the tonal components extracted as in Terhardt
    et al. (1982). The sinusoidal components and the narrowband regions of the
    spectrum are weighted by their level excess over the masking by the other
    components, the noise in their critical band and the threshold in quiet
    (w3), by their frequency (w2) and by their bandwidth (w1); the loudness of
    the remaining noise relative to the total loudness gives the second factor
    w_Gr. By definition a 1 kHz pure tone at 60 dB SPL has K = 1.

    Parameters
    ----------
    signal : array_like
        Input time signal in [Pa], one-dimensional. The signal is analysed as
        a whole: the spectrum is averaged over the full duration.
    fs : float
        Sampling frequency in [Hz]. Any rate is accepted; the Zwicker loudness
        used for w_Gr covers 24 Hz to 24 kHz and fills the bands above fs/2
        with zeros.
    field_type : {'free', 'diffuse'}, optional
        Sound field of the Zwicker loudness computation (ISO 532-1). Default
        is 'free'.

    Returns
    -------
    K : float
        Tonality in [t.u.]. Not limited to 1: Aures reports computed values up
        to 1.2 for complex tones (Fig. 9).

    Warning
    -------
    The method is defined for stationary sounds (one spectrum, one value).
    For time-varying sounds, analyse segments.

    Notes
    -----
    Steps, with the equations of Aures (1985):

    1. Power spectrum with a resolution of 12.5 Hz (Welch, Hamming window,
       50 % overlap, averaged over the whole signal).
    2. Sinusoidal components: local maxima at least 7 dB above the spectral
       lines two and three bins away on both sides (Terhardt et al. 1982, eq. 1),
       with the -3 dB width of the analysis window; frequency and level from a
       parabolic fit of the three central lines. Their bandwidth is
       :math:`\\Delta z = 0`.
    3. Narrowband regions (section 2.3.2): in the residual spectrum, regions
       narrower than a critical band whose critical band is at least 7 dB
       above both neighbouring critical bands. Centre frequency, level and
       bandwidth :math:`\\Delta z` in Bark are kept; the regions are removed
       from the residual, which is the noise spectrum of the model.
    4. Level excess of each component (Gl. 8):

       .. math::
           \\Delta L_i = L_i - 10\\lg\\Big\\{\\Big[\\sum_{k \\ne i} A_{Ek}(f_i)\\Big]^2
           + E_{Gr}(f_i) + E_{HS}(f_i)\\Big\\}

       with the excitation amplitudes :math:`A_{Ek}` of the other components
       from the masking slopes of Terhardt et al. (1982), 27 dB/Bark below a
       masker and :math:`-24 - 230\\,\\mathrm{Hz}/f_k + 0.2 L_k` dB/Bark above
       it, the noise intensity :math:`E_{Gr}` in the critical band of the
       component and the threshold in quiet :math:`E_{HS}`.
    5. Weights (Gl. 7, 9, 10) and tonal weighting (Gl. 11) over the components
       with :math:`\\Delta L_i > 0`:

       .. math::
           w_1(\\Delta z) = \\frac{0.13}{\\Delta z/\\mathrm{Bark} + 0.13},\\quad
           w_2(f) = \\Big[\\frac{1}{\\sqrt{1 + 0.2\\,(f/0.7\\,\\mathrm{kHz} + 0.7\\,\\mathrm{kHz}/f)^2}}\\Big]^{0.29},\\quad
           w_3(\\Delta L) = \\Big[1 - e^{-\\Delta L/15\\,\\mathrm{dB}}\\Big]^{0.29}

       .. math::
           w_T = \\sqrt{\\sum_i \\big[w_1^{1/0.29}(\\Delta z_i)\\, w_2^{1/0.29}(f_i)\\, w_3^{1/0.29}(\\Delta L_i)\\big]^2}

    6. Loudness weighting (Gl. 12) from the Zwicker loudness N of the signal
       and :math:`N_{Gr}` of the noise spectrum: :math:`w_{Gr} = 1 - N_{Gr}/N`.
    7. Tonality (Gl. 13): :math:`K = c\\, w_T^{0.29}\\, w_{Gr}^{0.79}`, with c
       computed once per sampling rate so that the reference tone gives
       exactly 1 t.u. (about 1.1).

    Choices the paper leaves open, made here: the window, the Welch averaging
    and the search range (20 Hz to fs/2; Terhardt's pitch analysis stops at
    5 kHz, but Aures' Fig. 5 includes tones up to 8 kHz); the shape test that
    tells a sinusoid from a narrow band (the -3 dB width of the peak must not
    exceed 1.8 bins, the window's main lobe being 1.3 bins wide); frequency
    and level of a sinusoid from the main-lobe shape of the window, and the
    removal of its leakage from the spectrum before the noise is read; the
    geometry of the narrowband regions (contiguous bins more than 6 dB above
    the floor of the surrounding critical bands, second-moment bandwidth of
    the power above that floor); the analytic Bark scale and critical
    bandwidth of Zwicker and Terhardt (1980) used by Terhardt et al. (1982).
    The validation in ``validations/sq_metrics/tonality_aures`` reproduces
    Fig. 5, 6 and 7 of the paper with synthetic signals.

    References
    ----------
    :cite:empty:`T_aures-Aures1985`
    :cite:empty:`T_aures-Terhardt1982`
    :cite:empty:`T_aures-Estreder2023`

    .. bibliography::
        :keyprefix: T_aures-

    Examples
    --------
    .. plot::
       :include-source:

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from mosqito.sq_metrics import tonality_aures
        >>> from mosqito.utils import sine_wave_generator
        >>> fs = 48000
        >>> noise = np.random.default_rng(0).standard_normal(fs)
        >>> noise = noise * 2e-5 * 10 ** (60 / 20) / np.std(noise)
        >>> levels = np.arange(40, 85, 5)
        >>> K = [tonality_aures(sine_wave_generator(fs, 1, 1000, L)[0] + noise, fs) for L in levels]
        >>> plt.plot(levels, K, marker="o")
        >>> plt.xlabel("Level of a 1 kHz tone in 60 dB SPL white noise [dB SPL]")
        >>> plt.ylabel("Tonality [t.u.]")
    """

    signal = np.asarray(signal, dtype=float).squeeze()
    if signal.ndim != 1:
        raise ValueError("signal must be a one-dimensional array")
    if signal.size == 0:
        raise ValueError("signal must not be empty")
    if fs <= 0:
        raise ValueError("fs must be positive")

    analysis = _aures_analysis(signal, fs, field_type)
    return float(_calibration_constant(fs, field_type) * analysis["K_raw"])


def _aures_analysis(signal, fs, field_type="free"):
    """Run the model without the calibration constant; returns all intermediate values."""

    freqs, pxx, enbw, lobe = _spectrum(signal, fs)
    df = freqs[1] - freqs[0]
    levels = 10 * np.log10(np.maximum(pxx, np.finfo(float).tiny) / P_REF**2)
    bark = _bark(freqs)
    k_min = int(np.ceil(F_MIN / df))
    k_max = pxx.size - 1 - 3

    # step 2: sinusoidal components, removed from the residual with their leakage
    sinusoids, residual = _find_sinusoids(levels, pxx, freqs, lobe, k_min, k_max)

    # step 3: narrowband regions of the residual, removed as well
    regions, noise = _find_regions(residual, freqs, bark, enbw, lobe, k_min, k_max)

    components = sinusoids + regions
    components.sort(key=lambda c: c["freq"])

    # step 4: level excess (Gl. 8)
    for i, comp in enumerate(components):
        comp["dL"] = _level_excess(i, components, noise, bark, enbw)

    # step 5: tonal weighting (Gl. 7, 9, 10, 11)
    w_t = _tonal_weight(components)

    # step 6: loudness weighting (Gl. 12)
    n_total = _loudness(pxx, freqs, enbw, field_type)
    n_noise = _loudness(noise, freqs, enbw, field_type)
    w_gr = 0.0
    if n_total > 0:
        w_gr = max(0.0, 1.0 - n_noise / n_total)

    return {
        "freqs": freqs,
        "levels": levels,
        "noise_levels": 10 * np.log10(np.maximum(noise, np.finfo(float).tiny) / P_REF**2),
        "components": components,
        "w_T": w_t,
        "w_Gr": w_gr,
        "N": n_total,
        "N_Gr": n_noise,
        "K_raw": w_t**0.29 * w_gr**0.79,  # Gl. (13) without c
    }


def _calibration_constant(fs, field_type):
    """c of Gl. (13): the reference tone (1 kHz, 60 dB SPL, p. 137) gives K = 1."""

    key = (float(fs), field_type)
    if key not in _calibration:
        freq, spl = REFERENCE_TONE
        t = np.arange(int(round(fs))) / fs
        tone = np.sqrt(2) * P_REF * 10 ** (spl / 20) * np.sin(2 * np.pi * freq * t)
        k_raw = _aures_analysis(tone, fs, field_type)["K_raw"]
        if k_raw <= 0:
            raise RuntimeError("the reference tone gives no tonality; calibration failed")
        _calibration[key] = 1.0 / k_raw
    return _calibration[key]


def _spectrum(signal, fs):
    """Welch power spectrum, 12.5 Hz spacing, Hamming window, 50 % overlap.

    Scaled so that a sinusoid reads its power at its peak bin; sums over bins
    must be divided by ``enbw`` (equivalent noise bandwidth of the window in
    bins) to read the band power. Signals shorter than one segment are
    zero-padded to keep the frequency spacing.
    """

    nfft = max(int(round(fs / FREQ_RESOLUTION)), 8)
    nperseg = min(nfft, signal.size)
    window = get_window("hamming", nperseg)
    enbw = nperseg * np.sum(window**2) / np.sum(window) ** 2
    freqs, pxx = welch(
        signal,
        fs=fs,
        window=window,
        nperseg=nperseg,
        noverlap=nperseg // 2,
        nfft=nfft,
        detrend=False,
        scaling="spectrum",
        return_onesided=True,
    )
    return freqs, pxx, enbw, _lobe_template(nperseg, nfft)


_LOBE_OVERSAMPLING = 64
_lobe_cache = {}


def _lobe_template(nperseg, nfft):
    """Power transform of the window relative to its peak, sampled every 1/64 bin.

    ``template[i]`` is |W(i/64 bins)|^2 / |W(0)|^2: the share of a sinusoid's
    power that the Welch estimate puts into a bin i/64 bins away from the
    sinusoid. ``width_rms`` is the second-moment width of the main lobe in
    bins, the broadening the window adds to a measured bandwidth.
    """

    key = (nperseg, nfft)
    if key not in _lobe_cache:
        window = get_window("hamming", nperseg)
        spectrum = np.abs(np.fft.rfft(window, n=nfft * _LOBE_OVERSAMPLING)) ** 2
        template = spectrum / spectrum[0]
        lobe = template[: LOBE_HALF_WIDTH * _LOBE_OVERSAMPLING + 1]
        offsets = np.arange(lobe.size) / _LOBE_OVERSAMPLING
        width_rms = float(np.sqrt(12 * np.sum(lobe * offsets**2) / np.sum(lobe)))
        _lobe_cache[key] = (template, width_rms)
    return _lobe_cache[key]


def _lobe_value(template, offset_bins):
    position = np.minimum(np.abs(offset_bins) * _LOBE_OVERSAMPLING, template.size - 1)
    return np.interp(position, np.arange(template.size), template)


def _find_sinusoids(levels, pxx, freqs, lobe, k_min, k_max):
    """Terhardt et al. (1982), eq. (1): local maxima 7 dB above the lines +-2 and +-3 bins away.

    A peak is accepted as a sinusoid only if it has the width of the window's
    main lobe (parabola through the three central lines in dB); wider peaks
    are left in the residual for the narrowband search. The position of the
    sinusoid between the bins and its level follow from the main-lobe shape
    of the window: the ratio of the two neighbouring lines fixes the offset,
    the offset fixes the scalloping loss. The leakage of every sinusoid is
    then subtracted from the spectrum and its main lobe replaced by a
    straight line between the bins outside it, which leaves the residual
    without the sinusoids.
    """

    template, _ = lobe
    df = freqs[1] - freqs[0]
    n = pxx.size
    sinusoids = []
    for k in range(max(k_min, 3), min(k_max, n - 4) + 1):
        if not (levels[k - 1] < levels[k] >= levels[k + 1]):
            continue
        if any(levels[k] - levels[k + off] < TONAL_THRESHOLD for off in (-3, -2, 2, 3)):
            continue
        curvature = levels[k - 1] - 2 * levels[k] + levels[k + 1]  # dB per bin^2 (negative)
        if curvature >= 0:
            continue
        width = 2 * np.sqrt(3 / (-0.5 * curvature))  # -3 dB width of the fitted parabola, bins
        if width > SINUSOID_MAX_WIDTH:
            continue
        offset = _lobe_offset(template, levels[k + 1] - levels[k - 1])
        level = levels[k] - 10 * np.log10(_lobe_value(template, offset))  # scalloping removed
        freq = (k + offset) * df
        sinusoids.append({"kind": "sinusoid", "freq": float(freq), "bark": float(_bark(freq)),
                          "level": float(level), "dz": 0.0, "bin": k, "offset": offset})

    residual = pxx.copy()
    bins = np.arange(n)
    for comp in sinusoids:
        power = P_REF**2 * 10 ** (comp["level"] / 10)
        residual -= power * _lobe_value(template, bins - (comp["bin"] + comp["offset"]))
    residual = np.maximum(residual, 0.0)
    for comp in sinusoids:
        lo = max(comp["bin"] - LOBE_HALF_WIDTH, 0)
        hi = min(comp["bin"] + LOBE_HALF_WIDTH, n - 1)
        left = residual[lo - 1] if lo > 0 else residual[hi + 1]
        right = residual[hi + 1] if hi + 1 < n else residual[lo - 1]
        residual[lo:hi + 1] = np.linspace(left, right, hi - lo + 1)
    return sinusoids, residual


def _lobe_offset(template, neighbour_ratio_db):
    """Offset of a sinusoid from its peak bin, from the level difference of the two neighbours."""

    def ratio(offset):
        return 10 * np.log10(_lobe_value(template, 1 - offset) / _lobe_value(template, 1 + offset))

    lo, hi = -0.5, 0.5
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if ratio(mid) < neighbour_ratio_db:
            lo = mid
        else:
            hi = mid
    return float(0.5 * (lo + hi))


def _find_regions(residual, freqs, bark, enbw, lobe, k_min, k_max):
    """Aures section 2.3.2: narrowband regions of the residual spectrum.

    A region is narrower than a critical band and its critical band stands at
    least 7 dB above both neighbouring critical bands. The paper states the
    criterion only; the geometry used here is: the maxima of the residual
    smoothed over 3 bins are visited in order of level; the floor around a
    maximum is the median level of the surrounding critical bands (0.5 to
    1.5 Bark away); the region is the run of bins more than 6 dB above that
    floor; its level is the power above the floor, its centre the power
    centroid and its bandwidth the second-moment width (sqrt(12) sigma) of
    the power above the floor, less the width of the window's main lobe.
    Accepted regions are replaced by their floor; a run wider than a
    critical band is noise and stays.
    """

    noise = residual.copy()
    df = freqs[1] - freqs[0]
    n = noise.size
    taken = np.zeros(n, dtype=bool)
    regions = []
    _, lobe_width = lobe

    for _ in range(MAX_REGIONS):
        smooth = np.convolve(noise, np.ones(3), mode="same")
        smooth_db = 10 * np.log10(np.maximum(smooth, np.finfo(float).tiny) / P_REF**2)
        best, best_level = None, -np.inf
        for k in range(max(k_min, 1), min(k_max, n - 2) + 1):
            if taken[k] or smooth_db[k] <= best_level:
                continue
            if smooth_db[k - 1] < smooth_db[k] >= smooth_db[k + 1] and smooth_db[k] > _hearing_threshold(freqs[k]):
                best, best_level = k, smooth_db[k]
        if best is None:
            break
        k = best
        taken[k] = True

        distance = np.abs(bark - bark[k])
        around = (distance > 0.5) & (distance <= 1.5) & ~taken
        if not around.any():
            continue
        floor_db = float(np.median(smooth_db[around]))
        cut = floor_db + 6.0
        reach = MAX_REGION_WIDTH * _critical_bandwidth(freqs[k]) / df  # a longer run is noise
        lo = k
        while lo > 0 and not taken[lo - 1] and smooth_db[lo - 1] > cut and k - lo < reach:
            lo -= 1
        hi = k
        while hi < n - 1 and not taken[hi + 1] and smooth_db[hi + 1] > cut and hi - k < reach:
            hi += 1
        taken[lo:hi + 1] = True  # visited once, accepted or not

        floor = 10 ** (floor_db / 10) * P_REF**2 / 3  # per bin: smooth is a sum over 3 bins
        excess = np.maximum(noise[lo:hi + 1] - floor, 0.0)
        if np.sum(excess) <= 0:
            continue
        f_reg = freqs[lo:hi + 1]
        f_c = float(np.sum(excess * f_reg) / np.sum(excess))
        sigma = np.sqrt(np.sum(excess * (f_reg - f_c) ** 2) / np.sum(excess))
        width = float(np.sqrt(max(12 * sigma**2 - (lobe_width * df) ** 2, 0.0)))
        dz = float(_bark(f_c + width / 2) - _bark(max(f_c - width / 2, df)))
        if dz > MAX_REGION_WIDTH:
            continue

        # the critical band of the region (at least one Bark around its centre)
        # against the critical bands next to its edges: both must be 7 dB lower
        z_c = float(_bark(f_c))
        z_lo = min(z_c - 0.5, float(bark[lo]))
        z_hi = max(z_c + 0.5, float(bark[hi]))
        own = (bark >= z_lo) & (bark <= z_hi)
        low = (bark >= z_lo - 1.0) & (bark < z_lo)
        upp = (bark > z_hi) & (bark <= z_hi + 1.0)
        if not (low.any() and upp.any()):
            continue

        def band_level(mask):
            return 10 * np.log10(max(np.sum(noise[mask]) / enbw, np.finfo(float).tiny) / P_REF**2)

        l_own = band_level(own)
        if l_own - band_level(low) < TONAL_THRESHOLD or l_own - band_level(upp) < TONAL_THRESHOLD:
            continue

        level = 10 * np.log10(np.sum(excess) / enbw / P_REF**2)
        if level < _hearing_threshold(f_c):
            continue

        regions.append({"kind": "region", "freq": f_c, "bark": z_c, "level": float(level),
                        "dz": dz, "bin": k, "lo": lo, "hi": hi})
        noise[lo:hi + 1] = floor
    return regions, noise


def _level_excess(i, components, noise, bark, enbw):
    """Gl. (8) with the masking slopes of Terhardt et al. (1982)."""

    comp = components[i]
    amplitude = 0.0
    for k, other in enumerate(components):
        if k == i:
            continue
        if comp["freq"] > other["freq"]:
            # above the masker: slope -24 - 230 Hz / f_k + 0.2 L_k in dB/Bark
            slope = -24.0 - 230.0 / other["freq"] + 0.2 * other["level"]
            excitation = other["level"] + slope * (comp["bark"] - other["bark"])
        else:
            # below the masker: slope 27 dB/Bark
            excitation = other["level"] - 27.0 * (other["bark"] - comp["bark"])
        amplitude += 10 ** (excitation / 20)

    in_band = np.abs(bark - comp["bark"]) <= 0.5
    noise_intensity = np.sum(noise[in_band]) / enbw / P_REF**2
    threshold_intensity = 10 ** (_hearing_threshold(comp["freq"]) / 10)
    return float(comp["level"] - 10 * np.log10(amplitude**2 + noise_intensity + threshold_intensity))


def _tonal_weight(components):
    """Gl. (11) with the weights of Gl. (7), (9) and (10); only components with dL > 0."""

    total = 0.0
    for comp in components:
        if comp["dL"] <= 0:
            continue
        w1 = 0.13 / (comp["dz"] + 0.13)  # Gl. (7)
        w2 = 1.0 / np.sqrt(1.0 + 0.2 * (comp["freq"] / 700.0 + 700.0 / comp["freq"]) ** 2)  # Gl. (9) base
        w3 = 1.0 - np.exp(-comp["dL"] / 15.0)  # Gl. (10) base
        # Gl. (11): w'_1 = w_1^(1/0.29); w'_2 and w'_3 are the bases of Gl. (9) and (10)
        total += (w1 ** (1 / 0.29) * w2 * w3) ** 2
    return float(np.sqrt(total))


def _loudness(pxx, freqs, enbw, field_type):
    """Zwicker loudness (ISO 532-1, stationary) from the power spectrum."""

    rms = np.sqrt(np.maximum(pxx, 0.0) / enbw)
    if freqs[-1] < 24000:
        df = freqs[1] - freqs[0]
        extra = np.arange(freqs[-1] + df, 24000 + df, df)
        freqs = np.concatenate([freqs, extra])
        rms = np.concatenate([rms, np.zeros(extra.size)])
    loudness, _, _ = loudness_zwst_freq(rms, freqs, field_type=field_type)
    return float(loudness)


def _bark(freq_hz):
    """Critical band rate, Zwicker and Terhardt (1980)."""

    f = np.asarray(freq_hz, dtype=float) / 1000
    return 13 * np.arctan(0.76 * f) + 3.5 * np.arctan((f / 7.5) ** 2)


def _critical_bandwidth(freq_hz):
    """Critical bandwidth in Hz, Zwicker and Terhardt (1980)."""

    return 25 + 75 * (1 + 1.4 * (freq_hz / 1000) ** 2) ** 0.69


def _hearing_threshold(freq_hz):
    """Threshold in quiet in dB SPL, Terhardt et al. (1982)."""

    f = max(float(freq_hz), 1e-3) / 1000
    return 3.64 * f**-0.8 - 6.5 * np.exp(-0.6 * (f - 3.3) ** 2) + 1e-3 * f**4
