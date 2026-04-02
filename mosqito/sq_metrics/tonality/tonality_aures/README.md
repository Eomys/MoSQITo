# Aures Tonality Development Notes

This folder contains the current MoSQITo implementation of the Aures tonality metric and its local validation helpers.

## Files

- `tonality_aures.py`: main implementation of the stationary Aures tonality metric.
- `tonality_aures_validation.py`: validation helpers and report entry point.
- `validation_SQAT_v1_0/`: local copy of the SQAT validation sounds used only for validation.

## Scope

The implementation in `tonality_aures.py` is intended to follow the Aures calculation path as summarized in:

- Casajus-Quiros et al., *Applied Acoustics* (2023)

SQAT is used here as a validation target only. Its code is not the design source for the implementation.

## Current Algorithm Structure

The current `tonality_aures` pipeline is:

1. Compute a one-sided power spectrum with a target frequency resolution of `12.5 Hz`.
2. Detect tonal candidates with the classical Aures prominence rule:
   peak at bin `i` and at least `7 dB` above bins `i-3`, `i-2`, `i+2`, `i+3`.
3. Refine the center frequency with the 3-point interpolation term:
   `f_c = f_i + 0.46 * df * (L[i+1] - L[i-1])`
4. Compute tonal component level from a 5-bin group centered on the candidate.
5. Compute excess level against:
   other tonal maskers, critical-band noise, and hearing threshold.
6. Compute the three Aures weighting terms:
   `w1` from effective bandwidth,
   `w2` from frequency,
   `w3` from excess level.
7. Combine relevant tones quadratically into a global tonal weight.
8. Compute the loudness ratio term by removing relevant tones from the spectrum and comparing loudness before/after removal.
9. Return:
   `K = 1.09 * w_T^0.29 * w_L^0.79`, capped at `1.0 t.u.`

## Formula-Level Derivation

This section rewrites the implementation in a notation closer to the paper so that the code can be checked against the mathematical model.

### 1. Spectrum and level definition

Let `x(t)` be the stationary sound pressure signal in Pascal. The implementation first computes a one-sided power spectrum:

```text
P(f_k)
```

with frequency spacing:

```text
df ≈ 12.5 Hz
```

The corresponding level per spectral line is expressed in dB SPL as:

```text
L_k = 10 log10(P(f_k) / p_ref^2)
```

with:

```text
p_ref = 2 × 10^-5 Pa
```

In code, this is the `levels_db` array in `tonality_aures.py`.

### 2. Candidate tonal components

A spectral line `k` is retained as a tonal candidate if:

```text
L_{k-1} < L_k >= L_{k+1}
```

and if the prominence condition is satisfied:

```text
L_k - L_{k+m} >= 7 dB
for m in {-3, -2, 2, 3}
```

This corresponds to the classical Aures tonal screening rule in a narrow-band spectrum.

### 3. Refined center frequency

For each candidate, the center frequency is refined from the discrete peak location using the local level asymmetry:

```text
f_c = f_k + 0.46 df (L_{k+1} - L_{k-1})
```

This produces a sub-bin estimate of the tonal center frequency.

### 4. Tonal component level

The implementation does not use only the single-bin peak level. Instead, it forms the tonal component from a 5-bin group centered on the candidate:

```text
I_t = Σ P(f_n)
for n = k-2 ... k+2
```

and converts it to a tonal level:

```text
L_t = 10 log10(I_t / p_ref^2)
```

This is the quantity used later in masking and excess-level calculations.

### 5. Critical-band representation

The Bark transform is:

```text
z(f) = 13 arctan(0.76 f / 1000) + 3.5 arctan((f / 7500)^2)
```

Each tonal component is evaluated inside a 1-Bark neighborhood:

```text
z_c - 0.5 <= z(f) < z_c + 0.5
```

where:

```text
z_c = z(f_c)
```

### 6. Masking by other tonal components

For another tonal component `j`, its excitation at the Bark position of tone `i` is modeled in level form as:

```text
L_ec,ij = L_t,j - q_ij (z_j - z_i)
```

with slope:

```text
q_ij = 27
if f_i <= f_j
```

and:

```text
q_ij = -24 - 230 / (f_j + 0.2 L_t,j)
if f_i > f_j
```

The tonal masking contribution is then summed in linear intensity form:

```text
I_tm,i = Σ 10^(L_ec,ij / 10)
```

over all other tonal candidates `j`.

### 7. Noise masking inside the critical band

Inside the 1-Bark band of tone `i`, the non-tonal part is estimated by removing all candidate 5-bin tonal groups and summing the remaining power:

```text
I_n,i = Σ P(f) / p_ref^2
```

over all frequencies in the local critical band that are not covered by a tonal candidate mask.

This step is important because `I_n,i`, `I_tm,i`, and the threshold term must all be represented in the same intensity reference before they can be added.

### 8. Hearing threshold term

The hearing threshold is introduced in level form as:

```text
L_h(f) = 3.64 (f / 1000)^(-0.8)
         - 6.5 exp(-0.6 (f / 1000 - 3.3)^2)
         + 10^-3 (f / 1000)^4
```

and converted to intensity:

```text
I_h,i = 10^(L_h(f_c) / 10)
```

### 9. Excess level

The excess level of tone `i` is then written as:

```text
ΔL_i = L_t,i - 10 log10(I_tm,i + I_n,i + I_h,i)
```

Only tones with:

```text
ΔL_i > 0
```

are retained as relevant tones.

### 10. Bandwidth weighting

The measured 3 dB width of the tonal peak is first obtained from the discrete spectrum. In code, the lower and upper frequencies are the first bins around the peak where the drop reaches at least `3 dB`.

If `f_l` and `f_u` are those crossing frequencies, the measured width is:

```text
B_meas = f_u - f_l
```

The current implementation then removes the analysis broadening:

```text
B_eff = max(B_meas - 2 df, 0)
```

and converts the effective width to Bark:

```text
Δz_i = z(f_c + B_eff / 2) - z(f_c - B_eff / 2)
```

The corresponding weighting term is:

```text
w_1,i = (0.13 / (Δz_i + 0.13))^(1 / 0.29)
```

This is the main place where the code introduces an explicit implementation choice to prevent pure tones from being penalized by the FFT main-lobe width.

### 11. Frequency weighting

The frequency weighting term is:

```text
w_2,i = 1 / sqrt(1 + 0.2 (f_c / 700 + 700 / f_c)^2)
```

This weights tones according to their position on the frequency axis.

### 12. Excess-level weighting

The excess-level weighting term is:

```text
w_3,i = 1 - exp(-ΔL_i / 15)
```

It tends to `0` for weakly emergent tones and tends to `1` for strongly emergent tones.

### 13. Global tonal weight

For all relevant tones, the global tonal weight is combined quadratically:

```text
w_T = sqrt(Σ (w_1,i w_2,i w_3,i)^2)
```

Before this summation, the implementation keeps only the dominant relevant tone inside a `0.5 Bark` neighborhood to avoid counting several spectral lines that belong to the same perceived component.

### 14. Loudness weighting

Let:

```text
N_s
```

be the loudness of the original spectrum and:

```text
N_n
```

be the loudness after removing the relevant tonal groups from the spectrum.

The loudness weight is then:

```text
w_L = max(0, 1 - N_n / N_s)
```

This term expresses the fraction of the total loudness associated with the retained tonal content.

### 15. Final tonality

The final Aures tonality value is:

```text
K = C w_T^0.29 w_L^0.79
```

with:

```text
C = 1.09
```

The current implementation clips the result to:

```text
K <= 1.0 t.u.
```

to preserve the expected interpretation of the Aures reference signal.

## Code-to-Equation Mapping

The most direct mapping between formulas and code is:

- spectrum and `L_k`:
  `_compute_power_spectrum` and `levels_db`
- candidate screening:
  `_find_tonal_candidates`
- refined `f_c`:
  `_refined_center_frequency`
- tonal level `L_t`:
  `_tone_level_db`
- excess level `ΔL_i`:
  `_build_relevant_tone`
- Bark width `Δz_i`:
  `_effective_bandwidth_bark`
- relevant-tone consolidation:
  `_select_dominant_tones`
- loudness term `w_L`:
  `_loudness_from_power_spectrum`
- final `K`:
  `tonality_aures`

## Important Implementation Choices

- The spectrum is handled in linear power until conversion to dB SPL is required.
- Tonal component level is based on a 5-bin energy sum, not just the single peak bin.
- Noise intensity in the excess-level calculation is converted to the same SPL reference as tonal masking and hearing threshold before summation.
- Relevant tones closer than `0.5 Bark` are reduced to the dominant one to avoid double counting the same tonal component.
- The 3 dB bandwidth is corrected by subtracting `2 * df` before converting to Bark width.
  This compensates for the analysis-window main-lobe spreading and keeps pure tones from being penalized as if they had physical bandwidth.

## Validation Policy

Validation is split into two layers:

- Reference signal check:
  `1 kHz`, `60 dB SPL` pure tone should evaluate to `1.0 t.u.` within tolerance.
- SQAT trend check:
  `Tonality_Aures1985` files from `0 dB` to `80 dB` prominence must produce a monotonic non-decreasing tonality curve.

Run the local validation report with:

```bash
PYTHONPATH=. python -m mosqito.sq_metrics.tonality.tonality_aures.tonality_aures_validation
```

Run the automated tests with:

```bash
pytest -q tests/sq_metrics/tonality/test_tonality_aures.py
```

## Current Baseline

At the time this README was written, the validation report produced:

- Reference pure tone: about `0.9866 t.u.`
- SQAT dataset trend:
  `0.0000, 0.1047, 0.1307, 0.2746, 0.5248, 0.7409, 0.8600, 0.9409, 0.9693`

This is considered acceptable for the current implementation because:

- the reference signal is within the configured tolerance;
- the SQAT dataset trend is strictly increasing;
- the global validation summary passes.

## Known Limits

- This implementation is currently written for stationary time signals.
- The relevant-tone grouping rule is pragmatic and should be revisited if a stricter interpretation of the paper is needed.
- The bandwidth correction for pure tones is an implementation choice made to preserve the reference calibration; if later documentation gives a more explicit prescription, this part should be updated first.
- The validation currently checks trend consistency against SQAT, not point-by-point equality with any external implementation.

## Next Work If Needed

- Add explicit unit tests for helper functions such as candidate detection, excess-level computation, and bandwidth correction.
- Add regression tests for multi-tone synthetic signals.
- Compare this implementation against additional literature examples beyond the SQAT validation set.
