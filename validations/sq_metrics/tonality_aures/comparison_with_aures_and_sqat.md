# Aures tonality in MoSQITo: comparison with the paper and with SQAT

This document records how the implementation of the Aures tonality in MoSQITo (`tonality_aures_st`, `tonality_aures_tv`) relates, step by step, to the method of the paper and to the implementation of the SQAT toolbox, and what the numerical comparison of the two implementations showed, down to the intermediate quantities of every processing block. The validation against the figures of the paper is summarised at the end; its full tables are in [README.md](README.md).

Direction of the judgements: the MoSQITo implementation is judged against the paper. SQAT is an independent implementation of the same paper and serves as a reference for the numbers; where the two implementations differ, both readings of the paper are given.

## 1. Sources and provenance

* W. Aures, "Berechnungsverfahren für den sensorischen Wohlklang beliebiger Schallsignale", Acustica 59 (1985) 130–141, section 2.3 and Fig. 8: the definition of the method. Equation numbers (Gl.) below refer to this paper.
* E. Terhardt, G. Stoll, M. Seewann, J. Acoust. Soc. Am. 71 (1982) 679–688: the extraction of sinusoidal components, the masking slopes and the threshold in quiet, which Aures takes over.
* E. Zwicker, E. Terhardt, J. Acoust. Soc. Am. 68 (1980) 1523–1525: the analytic critical-band rate and critical bandwidth used by Terhardt et al.
* J. Estreder et al., Applied Acoustics 204 (2023) 109238: used only as a clear restatement of the original method and of its parameters (12.5 Hz lines, k = {2, 3}, 7 dB). Its modifications (10.76 Hz, 5.5 dB, exponent of w1) are not adopted.
* SQAT (G. Felix Greco, R. Merino-Martínez, A. Osses, M. J. B. Lotinga, doi:10.5281/zenodo.7934709): `psychoacoustic_metrics/Tonality_Aures1985/Tonality_Aures1985.m` of the `main` branch at commit `11658b5` (2026-10-02; `git describe` v1.3-207-g11658b5). This is not the v1.3 release: the function was rewritten upstream between 2026-09-08 and 2026-09-15 (11 commits after v1.3, five of them breaking) and relicensed to GPL-3.0. SQAT was run, not copied: the MATLAB drivers in `comparison_sqat/` contain no SQAT code, and the intermediate quantities quoted below came from a copy of the function with logging statements added and no computation changed. All SQAT runs: MATLAB R2026a Update 2, on the author's machine.
* MoSQITo: this repository, the commit that carries this document. The implementation was written from the paper without reference to SQAT's code (GPL-3.0 against Apache-2.0); behaviour was compared, code was not. Written by Zhenxian Li with assistance from Claude (Anthropic).

## 2. The method step by step

Aures gives no pseudo-code; Fig. 8 and the text of section 2.3 are the whole specification. The flow is: spectrum, extraction of sinusoidal and narrowband components, level excess of each component (Gl. 8), tonal weighting w_T (Gl. 7, 9, 10, 11), loudness weighting w_Gr from the noise spectrum (Gl. 12), and K = c · w_T^0.29 · w_Gr^0.79 (Gl. 13).

| Step | Aures (1985) | MoSQITo | SQAT main @ 11658b5 | MoSQITo against the paper |
|---|---|---|---|---|
| 1 Spectrum | FFT; extraction as in Terhardt, whose resolution is 12.5 Hz; window, overlap and averaging not specified | Welch estimate: 80 ms Hamming segments, 50 % overlap, 12.5 Hz lines; averaged over the whole signal (`_st`) or within 250 ms frames (`_tv`); band powers corrected by the equivalent noise bandwidth of the window | Hann window of 250 ms (4 Hz lines), 125 ms hop, one FFT per frame; resampling to 44.1 or 48 kHz | not prescribed; the 12.5 Hz lines keep Terhardt's criterion as written |
| 2 Sinusoidal components | Terhardt's criterion: local maximum at least 7 dB above the lines two and three bins away (25 and 37.5 Hz) on both sides; search 20 Hz to 5 kHz | the same criterion on 12.5 Hz lines, plus a main-lobe shape test (−3 dB width at most 1.8 bins) and no candidates below the threshold in quiet; search 20 Hz to fs/2 (Fig. 5 of the paper has an 8 kHz tone) | the same criterion with the distances fixed in Hz; 20 Hz to 5 kHz; peaks below 0 dB dropped; the narrowband detector runs first and absorbs the sinusoids inside a region | agrees |
| 3 Narrowband components | after removing the sinusoids, regions of the residue narrower than a critical band whose neighbouring critical bands are at least 7 dB lower; centre frequency and Bark bandwidth kept; removed with the sinusoids; geometry not specified | residue after subtracting the leakage of the sinusoids; 3-bin smoothing; maxima in order of level; floor = median of the smoothed spectrum 0.5 to 1.5 Bark away; region = contiguous run more than 6 dB above the floor, at most 1.5 critical bandwidths each side; second-moment width with the main lobe removed in quadrature; Δz ≤ 1.5 Bark; own band at least 7 dB above both neighbours; region replaced by the floor | geometry of FindBand_V (Hastings 2004): half-power walk from the peak, floor = lowest value of the smoothed spectrum within half a critical band beyond the half-power point, region extended to that point and replaced by a line between its ends; width = span of the middle 90 % of the power / 0.9, footprint of the window removed in quadrature; the two 7 dB conditions | agrees; the geometry is a choice on both sides, validated here against Fig. 6 |
| 4 Frequency and level of a component | frequency and level of the spectral peak | sub-bin frequency and level from the shape of the window's main lobe (offset solved from the level difference of the two neighbouring bins) | bin frequency, amplitude-corrected bin level (up to 1.4 dB low between bins) | agrees |
| 5 Bandwidth Δz | sinusoids Δz = 0; regions their Bark width | sinusoids 0; regions √(12σ² − main lobe²) in Bark | √(BW² − footprint²) in Bark, so a pure tone gives 0; the width of a region grows with the share of noise in it | agrees |
| 6 Masking by the other components | [Σ A_Ek]²: amplitudes summed, then squared; slopes 27 dB/Bark below a masker, −24 − 230 Hz/f_k + 0.2 L_k dB/Bark above | the same | the same | agrees |
| 7 E_Gr and E_HS | noise intensity within ±0.5 Bark of the component after removing the tonal components; Terhardt's threshold in quiet | power of the noise spectrum (all components removed) within ±0.5 Bark, divided by the equivalent noise bandwidth; same threshold formula | residue within ±0.5 Bark, skipping the five central bins; same threshold formula. The residue has the regions bridged, so a band of noise around a tone is no longer in E_Gr (section 3.3) | agrees |
| 8 Level excess ΔL | ΔL_i = L_i − 10 lg{[ΣA]² + E_Gr + E_HS}; only ΔL > 0 counts | the same; components with ΔL ≤ 0 do not enter w_T but stay removed from the noise spectrum | the same; LX ≤ 0 gives w3 = 0 | agrees |
| 9 w1, w2, w3, w_T | Gl. (7), (9), (10), (11), exponent 1/0.29 on w1 inside the sum | algebraically the same | the same | agrees |
| 10 Noise spectrum and w_Gr | spectrum with all extracted components removed; Zwicker loudness of it and of the signal; w_Gr = 1 − N_Gr/N | sinusoids subtracted with their leakage (main-lobe template), regions replaced by the floor; N and N_Gr from the ISO 532-1 stationary loudness of the two spectra | sinusoid bins notched (at least four bins), regions bridged, inverse FFT, ISO 532-1 stationary loudness of the windowed frame (absolute loudness 4.3 dB lower, the ratio unaffected); w_Gr floored at 0 | agrees |
| 11 K and c | K = c w_T^0.29 w_Gr^0.79; c such that the reference tone (1 kHz, 60 dB SPL) gives 1; no upper limit | c calibrated per sampling rate from the reference tone (1.1055 at 48 kHz); no clipping | C = 1.1055 fixed, calibrated the same way; `abs`, no clipping | agrees |
| 12 Time | one spectrum, one K; a transient sound is analysed from a chosen instant | `tonality_aures_st`: one value for the whole signal; `tonality_aures_tv`: 250 ms frames every 125 ms, each analysed as a whole signal; statistics left to the user | frames of 250 ms every 125 ms, with statistics (mean, K5, …) | not prescribed |

The paper prescribes the criterion of Terhardt, the two conditions on narrowband regions, the three terms of Gl. (8) with Terhardt's slopes and threshold, Gl. (7) to (13) as written, c defined by the reference tone and the Zwicker loudness. It leaves open the spectrum estimate, the sub-bin frequency and level of a sinusoid, the geometry of the narrowband regions, the removal of the leakage of a component, the search range and the handling of time. Each of these choices is validated in README.md.

## 3. Numerical comparison, block by block

### 3.1 Signals

All signals are built from the same formulas in MATLAB and Python (48 kHz, 2 s, pascals): zero-phase sinusoids, and multisines with 1 Hz line spacing for narrowband noise. For the multisines the phases come from a Park–Miller generator (seed 12345), which is exact in double precision in both languages; the samples are identical (checksums compared). A first version used a golden-ratio phase sequence, which is linear in the line index and therefore a pulse train; section 3.4 records what that showed.

SQAT's intermediate quantities are those of its fifth frame (t = 0.5 to 0.75 s); the MoSQITo values are those of the whole signal, with the frame-wise series alongside. The absolute loudness differs between the two implementations (reference tone: 3.04 sone in SQAT, 4.05 sone here) because SQAT computes the loudness of the Hann-windowed frame; the ratio w_Gr is unaffected.

### 3.2 Pure tones and tone complexes (identical blocks)

| Signal | Quantity | SQAT | MoSQITo |
|---|---|---|---|
| 1 kHz, 60 dB (reference) | ΔL / w2 / w3 | 56.63 dB / 0.9107 / 0.9933 | 56.63 dB / 0.9107 / 0.9933 |
| | w_T / w_Gr / K | 0.7077 / 1 / 1.000 | 0.7077 / 1 / 1.000 |
| 1006.25 Hz, 60 dB (between bins) | f / L / ΔL | 1008 Hz / 60.0 dB / 56.64 dB | 1006.25 Hz / 60.0 dB / 55.04 dB |
| | K | 0.9997 | 0.9989 |
| 1 kHz 60 dB + 1.5 kHz 30 dB | ΔL of the two tones | 56.63 / 2.87 dB | 56.63 / 2.87 dB |
| | w_T / K | 0.7167 / 1.0037 | 0.7167 / 1.0037 |
| 500 + 1000 + 2000 Hz, 50 dB each | ΔL of the three tones | 43.72 / 45.98 / 50.12 dB | 43.72 / 45.98 / 50.12 dB |
| | w_T / K | 1.1196 / 1.1423 | 1.1196 / 1.1423 |

The only difference is a label: in this SQAT version the narrowband detector runs before the sinusoid extraction, so a pure tone appears as a "region" whose width equals the footprint of the window (Δz = 0, the same weight as a sinusoid). The 20 deterministic signals of the CSV agree to 0.001 in K, and frame by frame to 0.007 (section 3.5).

### 3.3 Narrowband noise, and a tone in it (where the implementations differ)

| Signal | Quantity | SQAT | MoSQITo | Paper |
|---|---|---|---|---|
| multisine 961–1040 Hz, 60 dB (0.5 Bark) | component | one region, f 1030 Hz, L 55.8 dB, Δz 0.460 | one region, f 1002 Hz, L 59.9 dB, Δz 0.511 | a narrowband region |
| | w1 / ΔL / w_T | 0.220 / 52.6 dB / 0.0038 | 0.203 / 41.3 dB / 0.0028 | |
| | w_Gr | 1 (the whole band bridged, N_Gr = 0) | 0.929 (0.29 sone left outside the region) | |
| | K | 0.219 (frames 0.201 to 0.232, mean 0.215) | 0.189 (frames mean 0.196) | Gl. (7): 0.206 |
| 1 kHz 82 dB + multisine 912–1088 Hz 56 dB | components | one region, f 1000 Hz, BW 10.7 Hz, L 82.0 dB, Δz 0.008, w1 0.944 | sinusoid 1000 Hz, L 82.0 dB, Δz 0; region 1001 Hz, L 56.0 dB, Δz 1.1, masked | |
| | ΔL of the tone / w3 | 77.9 dB / 0.998 | 26.2 dB / 0.946 | Gl. (8): the noise of the band is in E_Gr |
| | w_T / w_Gr / K | 0.590 / 1 / 0.949 (mean 0.954) | 0.598 / 0.992 / 0.947 (frames mean 0.949) | |
| 1 kHz 82 dB + multisine 912–1088 Hz 76 dB | components | one region, f 1000 Hz, BW 51.5 Hz, L 82.4 dB, Δz 0.322, w1 0.288 | sinusoid 1000 Hz, Δz 0; region 76 dB, Δz 1.1, masked | |
| | ΔL of the tone / w3 | 66.1 dB / 0.996 | 6.15 dB / 0.729 | |
| | w_T / w_Gr / K | 0.0097 / 0.999 / 0.288 (frames 0.125 to 0.288, mean 0.183) | 0.244 / 0.886 / 0.667 (frames mean 0.682) | |

On the noise band alone the two agree and bracket the value of Gl. (7). On a tone inside a band of noise narrower than a critical band they part, and the cause is the geometry of SQAT's narrowband regions: the floor is the lowest point of the smoothed spectrum within half a critical band beyond the half-power points, the region extends to that point, and the whole region is replaced by a line between its ends. For a tone inside such a band the lowest point lies outside the band, so band and tone become one region and the band is bridged away: it enters neither E_Gr nor N_Gr (level excess 78 dB where the tone stands 26 dB over the band), and the width of the region grows with the share of the noise in it, which is where SQAT's K falls. The MoSQITo implementation follows the order of Fig. 8, sinusoids first and regions in the residue: the tone keeps Δz = 0 and the band enters E_Gr as Gl. (8) states. At 26 dB over the band both give the same K by different routes (SQAT loses 18 % through w1, MoSQITo 17 % through w3); at 6 dB they give 0.183 and 0.667.

The reading of Gl. (8) taken here is the literal one (E_Gr is the noise intensity in the critical band of the component). The geometry of SQAT comes from Hastings (2004), which the paper does not prescribe; which reading is closer to listening data is open, since Fig. 5 to 7 of the paper do not cover a tone in narrowband noise. The same mechanism explains the earlier differences on SQAT's own validation sounds (1 kHz tone at 82 dB SPL in one critical band of noise, data set doi:10.5281/zenodo.7933206, not shipped here): SQAT 0.13 and 0.73 where the tone stands 30 and 40 dB over the band, against 0.40 and 0.79 here, and 0.92 to 1.00 on both sides from 50 dB on. It also explains the w_Gr difference on the white noise with tones at 442 and 1768 Hz among the recordings (0.63 here, 0.70 in SQAT): the bridging lowers the noise around each tone down to the nearest minimum of the spectrum.

### 3.4 A lesson about test signals: the golden-ratio multisine is a pulse train

The first comparison used multisines with phases φ_n = 2π·frac(0.618·n). A phase linear in the line index is a time shift, so this signal is a Dirichlet-kernel pulse train with a period of 1 s (crest factor 22 dB, pulses at t ≈ 0.38 s and 1.38 s). Between the pulses the kernel's sidelobes oscillate at N/2 Hz, so a 250 ms frame away from the pulse contains a two-tone at f_c ± N/2 (960 and 1040 Hz for the 0.5 Bark band, 912 and 1088 Hz for the 1 Bark band) about 22 dB below the long-term band level. SQAT's fifth frame duly found those two sinusoids (K 0.922 for the band alone), the frames containing a pulse gave outliers (0.21), and the whole-signal Welch spectrum of MoSQITo, which for a periodic signal is the exact line spectrum, found the flat band (K 0.189). Both were right about what they analysed; the difference measured the non-stationarity of the signal, not the algorithms, and the frame-wise function reproduces SQAT's series on these signals (means 0.714 against 0.798, 0.985 against 0.980, 0.884 against 0.840 for the three signals). The stationary multisines of section 3.3 replaced them.

### 3.5 Frame by frame

`tonality_aures_tv` uses the frames of SQAT (250 ms every 125 ms from the start of the signal), so the series are compared frame by frame (`input/sqat_aures_frames.csv`, `compare_with_sqat_frames`). SQAT stamps a frame at its start, MoSQITo at its centre; the comparison matches frames by index. The 17 tone signals agree in every frame to 0.007; the 0.5 Bark band to 0.043 (RMS 0.022), the tone 26 dB over the band to 0.019 (RMS 0.008), the tone 6 dB over the band shows the difference of section 3.3 in every frame (RMS 0.50).

### 3.6 Recordings

On the 18 recordings shipped with MoSQITo (ISO 532-1 Annex B.4 and B.5 sounds and a few others, `input/sqat_aures_recordings.csv` and `..._frames.csv`), the like-for-like comparison is SQAT's frame statistics against those of `tonality_aures_tv`. The frame means agree within 0.01 on most files, the propeller aircraft (0.249 against 0.256, RMS of the frame difference 0.045) and the traffic recording (0.012 against 0.014) included. The door creak (0.107 against 0.068) and the white noise with tones at 442 and 1768 Hz (0.718 against 0.776) are the exceptions, the second for the reason given in section 3.3. The whole-file value of `tonality_aures_st` agrees with the frame mean only for stationary sounds and is higher for the propeller aircraft (0.360) and the door creak (0.147), where the tonal components are present during part of the file only: the two readings answer different questions.

## 4. Validation against the paper (summary)

Targets are the formulas of the paper; the signals are synthetic (`tonality_aures_validation.py`); full tables and the figure are in README.md.

| Check | Signal | Target | Obtained | Tolerance | Pass |
|---|---|---|---|---|---|
| Reference tone | 1 kHz, 60 dB SPL | 1.000 | 1.000 | 0.001 | yes |
| Tone between bins | 990 to 1010 Hz every 2.5 Hz, 60 dB | 1.000 | 0.999 to 1.000 | 0.010 | yes |
| Fig. 5, frequency | 250 / 500 / 2000 / 4000 / 8000 Hz, 60 dB | 0.937 / 1.001 / 0.934 / 0.813 / 0.679 | 0.932 / 0.999 / 0.935 / 0.815 / 0.679 | 0.050 | yes |
| Fig. 6, bandwidth | 1 kHz band noise 0.2 / 0.3 / 0.5 / 0.7 / 1.0 / 1.4 Bark, 60 dB | 0.394 / 0.302 / 0.206 / 0.157 / 0.115 / 0.085 | 0.368 / 0.291 / 0.201 / 0.147 / 0.105 / 0.079 | 15 % | yes |
| Fig. 7, level | 1 kHz, 40 / 50 / 60 / 70 / 80 dB | 1.000 | 0.981 / 0.993 / 1.000 / 1.003 / 1.005 | 0.030 | yes |
| White noise | 20 Hz to 20 kHz, 60 dB | 0.000 | 0.000 | 0.020 | yes |
| Tone in one-critical-band noise | 1 kHz 82 dB, tone 0 to 80 dB over the band | monotonic rise | 0.088 to 1.000 | – | yes |
| Frame-wise reference tone | 2 s, fifteen 250 ms frames | 1.000 in every frame | 1.000 | 0.001 | yes |

Known properties: components narrower than about 25 Hz cannot be told from a sinusoid at 12.5 Hz lines; a 30 dB SPL pure tone gives 0.954 because w3 drops as the level excess approaches the threshold in quiet (the paper's Fig. 7 covers 2 to 28 sone); the criterion of Terhardt works in absolute hertz, so the tolerance to frequency modulation within an 80 ms segment is about ±12 Hz at any frequency (a tone with ±0.5 % vibrato keeps 0.93 of its value at 1 kHz and 0.64 at 8 kHz, where it becomes a narrow region); a slow drift is handled by the frame-wise function (an 8 kHz tone drifting 100 Hz in 2 s: 0.44 whole-signal, 0.665 frame mean).

## 5. Changes relative to the first version of the pull request

The first version (PR #97 as opened) differed from the paper in seven places, found by this comparison and all corrected in the rewrite: the upper masking slope had its bracket misplaced (−24 − 230/(f + 0.2 L) instead of −24 − 230/f + 0.2 L); the maskers were summed in intensity instead of amplitude; the bandwidth of every candidate was estimated from its −3 dB width, which gave a 60 dB tone between two bins K = 0.54; the narrowband regions of section 2.3.2 were missing (Fig. 6 gave 0 above 0.3 Bark); the noise spectrum kept the masked components; c was fixed at 1.09 and K clipped at 1; the sub-bin frequency interpolation overshot. The whole-signal values before and after, for 35 signals, are in the validation report; the reference tone went from 0.987 to 1.000, the 1006.25 Hz tone from 0.536 to 0.999, the 0.5 Bark band from 0.000 to 0.201 (target 0.206), the three-tone complex from 1.000 (clipped) to 1.142 (SQAT 1.142).

## 6. Reproduction

* MoSQITo side: `python validations/sq_metrics/tonality_aures/validation_tonality_aures.py` prints every table and writes `output/validation_tonality_aures.png`; the SQAT comparisons read the CSV files in `input/`.
* SQAT side: `comparison_sqat/compare_sqat_aures.m` (deterministic signals, one row per signal and one per frame) and `comparison_sqat/compare_sqat_aures_recordings.m` (the recordings shipped with MoSQITo) take the folder of a SQAT clone and write the CSV files; the header line of each CSV names the SQAT commit, the MATLAB version and the date of the run.
* Licences: MoSQITo is Apache-2.0, SQAT is GPL-3.0. SQAT was only executed; no SQAT code is in this repository, and the CSV files are outputs of running it. The nine validation sounds of the SQAT v1.x data set are not shipped (doi:10.5281/zenodo.7933206).

## References

* W. Aures, "Berechnungsverfahren für den sensorischen Wohlklang beliebiger Schallsignale", Acustica 59 (1985) 130–141.
* E. Terhardt, G. Stoll, M. Seewann, "Algorithm for extraction of pitch and pitch salience from complex tonal signals", J. Acoust. Soc. Am. 71 (1982) 679–688, doi:10.1121/1.387544.
* E. Zwicker, E. Terhardt, "Analytical expressions for critical-band rate and critical bandwidth as a function of frequency", J. Acoust. Soc. Am. 68 (1980) 1523–1525, doi:10.1121/1.385079.
* J. Estreder, G. Piñero, M. de Diego, J. Rämö, V. Välimäki, "Improved Aures tonality metric for complex sounds", Applied Acoustics 204 (2023) 109238, doi:10.1016/j.apacoust.2023.109238.
* A. Hastings, "Sound quality of diesel engines", Ph.D. thesis, Purdue University, 2004, ProQuest AAI3154642 (appendix A.3.8, FindBand_V).
* G. Felix Greco, R. Merino-Martínez, A. Osses, M. J. B. Lotinga, SQAT: a sound quality analysis toolbox for MATLAB, doi:10.5281/zenodo.7934709.
