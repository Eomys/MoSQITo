# -*- coding: utf-8 -*-

"""Aures tonality according to the formulation summarized in Casajus-Quiros et al."""

import numpy as np
from scipy.signal import periodogram

from mosqito.sq_metrics.loudness.loudness_zwst.loudness_zwst_freq import (
    loudness_zwst_freq,
)


REF_PRESSURE = 2e-5
REF_PRESSURE_SQ = REF_PRESSURE**2
TARGET_FREQ_RES_HZ = 12.5
PROMINENCE_THRESHOLD_DB = 7.0
TONE_HALF_WIDTH_BINS = 2
MIN_BARK_SEPARATION = 0.5
CALIBRATION_CONSTANT = 1.09


def tonality_aures(signal, fs):
    """
    Compute the Aures tonality value from a time signal in Pascal.

    The implementation follows the original Aures structure as summarized in:
    Casajus-Quiros et al., "Improved Aures tonality metric for complex sounds",
    Applied Acoustics 2023.

    Parameters
    ----------
    signal : array_like
        Input time signal in [Pa].
    fs : float
        Sampling frequency in [Hz].

    Returns
    -------
    float
        Tonality value in [t.u.].
    """

    signal = np.asarray(signal, dtype=float).squeeze()
    if signal.ndim != 1:
        raise ValueError("signal must be a one-dimensional array")
    if signal.size == 0:
        raise ValueError("signal must not be empty")

    freqs, power_spectrum = _compute_power_spectrum(signal, fs)
    levels_db = 10 * np.log10(np.maximum(power_spectrum, np.finfo(float).tiny) / REF_PRESSURE_SQ)

    candidates = _find_tonal_candidates(levels_db)
    if not candidates:
        return 0.0

    bark_axis = _bark(freqs)
    candidate_mask = _build_tone_mask(power_spectrum.size, candidates)

    relevant_tones = []
    for index in candidates:
        tone = _build_relevant_tone(
            index=index,
            freqs=freqs,
            levels_db=levels_db,
            power_spectrum=power_spectrum,
            bark_axis=bark_axis,
            candidates=candidates,
            candidate_mask=candidate_mask,
        )
        if tone is not None:
            relevant_tones.append(tone)

    relevant_tones = _select_dominant_tones(relevant_tones)
    if not relevant_tones:
        return 0.0

    tonal_weight = np.sqrt(
        sum((tone["w1"] * tone["w2"] * tone["w3"]) ** 2 for tone in relevant_tones)
    )

    signal_loudness = _loudness_from_power_spectrum(power_spectrum, freqs)
    noise_spectrum = power_spectrum.copy()
    for tone in relevant_tones:
        lo, hi = _tone_bounds(tone["index"], power_spectrum.size)
        noise_spectrum[lo:hi] = 0.0

    noise_loudness = _loudness_from_power_spectrum(noise_spectrum, freqs)
    loudness_weight = 0.0
    if signal_loudness > 0:
        loudness_weight = max(0.0, 1.0 - noise_loudness / signal_loudness)

    tonality = CALIBRATION_CONSTANT * tonal_weight**0.29 * loudness_weight**0.79
    return float(min(tonality, 1.0))


def _compute_power_spectrum(signal, fs):
    nfft = max(int(round(fs / TARGET_FREQ_RES_HZ)), 8)
    freqs, power_spectrum = periodogram(
        signal,
        fs=fs,
        window="hamming",
        nfft=nfft,
        detrend=False,
        scaling="spectrum",
        return_onesided=True,
    )
    return freqs, power_spectrum


def _find_tonal_candidates(levels_db):
    candidates = []
    for index in range(3, len(levels_db) - 3):
        if levels_db[index - 1] < levels_db[index] >= levels_db[index + 1]:
            if all(
                levels_db[index] - levels_db[index + offset] >= PROMINENCE_THRESHOLD_DB
                for offset in (-3, -2, 2, 3)
            ):
                candidates.append(index)
    return candidates


def _build_relevant_tone(
    index,
    freqs,
    levels_db,
    power_spectrum,
    bark_axis,
    candidates,
    candidate_mask,
):
    df = freqs[1] - freqs[0]
    center_freq = _refined_center_frequency(index, freqs, levels_db)
    bark_value = _bark(center_freq)
    tone_level_db = _tone_level_db(index, power_spectrum)

    band_mask = (bark_axis >= bark_value - 0.5) & (bark_axis < bark_value + 0.5)
    noise_intensity = np.sum(power_spectrum[band_mask & ~candidate_mask]) / REF_PRESSURE_SQ

    masking_intensity = 0.0
    for other_index in candidates:
        if other_index == index:
            continue

        other_freq = _refined_center_frequency(other_index, freqs, levels_db)
        other_level_db = _tone_level_db(other_index, power_spectrum)
        other_bark = _bark(other_freq)

        if center_freq <= other_freq:
            slope = 27.0
        else:
            slope = -24.0 - 230.0 / (other_freq + 0.2 * other_level_db)

        excitation_level_db = other_level_db - slope * (other_bark - bark_value)
        masking_intensity += 10 ** (excitation_level_db / 10)

    threshold_intensity = 10 ** (_hearing_threshold(center_freq) / 10)
    excess_level_db = tone_level_db - 10 * np.log10(
        masking_intensity + noise_intensity + threshold_intensity
    )

    if excess_level_db <= 0:
        return None

    bandwidth_bark = _effective_bandwidth_bark(index, freqs, levels_db, center_freq, df)

    return {
        "index": index,
        "freq_hz": center_freq,
        "bark": bark_value,
        "level_db": tone_level_db,
        "delta_z": bandwidth_bark,
        "delta_l": excess_level_db,
        "w1": (0.13 / (bandwidth_bark + 0.13)) ** (1 / 0.29),
        "w2": 1.0
        / np.sqrt(1.0 + 0.2 * (center_freq / 700.0 + 700.0 / center_freq) ** 2),
        "w3": 1.0 - np.exp(-excess_level_db / 15.0),
    }


def _tone_level_db(index, power_spectrum):
    lo, hi = _tone_bounds(index, power_spectrum.size)
    tone_power = np.sum(power_spectrum[lo:hi])
    return 10 * np.log10(np.maximum(tone_power, np.finfo(float).tiny) / REF_PRESSURE_SQ)


def _refined_center_frequency(index, freqs, levels_db):
    df = freqs[1] - freqs[0]
    offset = 0.46 * df * (levels_db[index + 1] - levels_db[index - 1])
    return float(np.clip(freqs[index] + offset, freqs[index - 1], freqs[index + 1]))


def _effective_bandwidth_bark(index, freqs, levels_db, center_freq, df):
    peak_level = levels_db[index]

    lower = index
    while lower > 0 and peak_level - levels_db[lower] < 3.0:
        lower -= 1

    upper = index
    while upper < len(levels_db) - 1 and peak_level - levels_db[upper] < 3.0:
        upper += 1

    measured_bandwidth_hz = max(freqs[upper] - freqs[lower], 0.0)
    effective_bandwidth_hz = max(measured_bandwidth_hz - 2.0 * df, 0.0)

    if effective_bandwidth_hz <= 0:
        return 0.0

    lower_freq = max(center_freq - effective_bandwidth_hz / 2.0, df)
    upper_freq = center_freq + effective_bandwidth_hz / 2.0
    return float(_bark(upper_freq) - _bark(lower_freq))


def _select_dominant_tones(relevant_tones):
    selected = []
    for tone in sorted(relevant_tones, key=lambda item: item["level_db"], reverse=True):
        if all(abs(tone["bark"] - kept["bark"]) >= MIN_BARK_SEPARATION for kept in selected):
            selected.append(tone)
    return selected


def _build_tone_mask(size, tone_indices):
    mask = np.zeros(size, dtype=bool)
    for index in tone_indices:
        lo, hi = _tone_bounds(index, size)
        mask[lo:hi] = True
    return mask


def _tone_bounds(index, size):
    lo = max(0, index - TONE_HALF_WIDTH_BINS)
    hi = min(size, index + TONE_HALF_WIDTH_BINS + 1)
    return lo, hi


def _loudness_from_power_spectrum(power_spectrum, freqs):
    rms_spectrum = np.sqrt(np.maximum(power_spectrum, 0.0))
    loudness, _, _ = loudness_zwst_freq(rms_spectrum, freqs)
    return float(loudness)


def _bark(freq_hz):
    freq_hz = np.asarray(freq_hz, dtype=float)
    return 13 * np.arctan(0.76 * freq_hz / 1000) + 3.5 * np.arctan((freq_hz / 7500) ** 2)


def _hearing_threshold(freq_hz):
    x = freq_hz / 1000
    return 3.64 * x**-0.8 - 6.5 * np.exp(-0.6 * (x - 3.3) ** 2) + 1e-3 * x**4
