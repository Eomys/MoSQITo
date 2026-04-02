# Aures Tonality: Validation and Implementation Notes

This directory contains the validation material associated with the Aures tonality implementation.

## Directory Structure

- `validation_tonality_aures.py`: validation entry point following the project `validations/` layout.
- `input/Tonality_Aures1985/`: local SQAT validation sounds used for Aures tonality validation.
- `output/`: generated validation figure.

The implementation under study is located in:

- `mosqito/sq_metrics/tonality/tonality_aures/tonality_aures.py`

The reusable validation utilities are located in:

- `mosqito/sq_metrics/tonality/tonality_aures/tonality_aures_validation.py`

## Validation Dataset

The validation relies on the `Tonality_Aures1985` signals distributed in Zenodo record `7933206`.

The helper module first checks for the expected `.wav` files in:

```text
validations/sq_metrics/tonality_aures/input/Tonality_Aures1985/
```

If one or more files are absent, an automatic download is attempted from:

```text
https://zenodo.org/records/7933206
```

This arrangement keeps validation assets in the `validations/` tree rather than in the library source directory.

## Validation Criteria

The current validation baseline is defined by two checks:

1. Aures reference signal:
   a `1 kHz`, `60 dB SPL` pure tone should yield approximately `1.0 t.u.`
2. SQAT trend check:
   the 9 `Tonality_Aures1985` signals should produce a monotonic non-decreasing tonality curve from `0 dB` to `80 dB` prominence.

## Mathematical Formulation

The notation below is intended to make the correspondence between the implementation and the mathematical form of the method explicit.

### 1. Spectrum and level definition

Let `x(t)` denote the stationary sound-pressure signal in Pascal. A one-sided power spectrum is first computed:

```text
P(f_k)
```

with frequency spacing:

```text
df ≈ 12.5 Hz
```

The level associated with each spectral line is expressed in dB SPL as:

```text
L_k = 10 log10(P(f_k) / p_ref^2)
```

with:

```text
p_ref = 2 × 10^-5 Pa
```

In the implementation, this quantity corresponds to the array `levels_db`.

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

This is the tonal screening condition used in the original Aures framework.

### 3. Refined center frequency

For each candidate, the center frequency is refined from the discrete peak location through local level asymmetry:

```text
f_c = f_k + 0.46 df (L_{k+1} - L_{k-1})
```

This yields a sub-bin estimate of the tonal center frequency.

### 4. Tonal component level

The tonal component level is evaluated from a 5-bin group centered on the candidate:

```text
I_t = Σ P(f_n)
for n = k-2 ... k+2
```

and converts it to a tonal level:

```text
L_t = 10 log10(I_t / p_ref^2)
```

This level is used in the subsequent masking and excess-level calculations.

### 5. Critical-band representation

The Bark transform is:

```text
z(f) = 13 arctan(0.76 f / 1000) + 3.5 arctan((f / 7500)^2)
```

Each tonal component is evaluated within a 1-Bark neighborhood:

```text
z_c - 0.5 <= z(f) < z_c + 0.5
```

where:

```text
z_c = z(f_c)
```

### 6. Masking by other tonal components

For another tonal component `j`, the excitation produced at the Bark position of tone `i` is written in level form as:

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

The tonal masking term is then summed in linear intensity form:

```text
I_tm,i = Σ 10^(L_ec,ij / 10)
```

over all other tonal candidates `j`.

### 7. Noise masking inside the critical band

Within the 1-Bark band of tone `i`, the non-tonal contribution is estimated by removing all candidate 5-bin tonal groups and summing the remaining power:

```text
I_n,i = Σ P(f) / p_ref^2
```

over all frequencies in the local critical band that are not covered by a tonal candidate mask.

The quantities `I_n,i`, `I_tm,i`, and the threshold term are therefore expressed in a common intensity reference before summation.

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

The excess level of tone `i` is then defined as:

```text
ΔL_i = L_t,i - 10 log10(I_tm,i + I_n,i + I_h,i)
```

Only tones with:

```text
ΔL_i > 0
```

are retained as relevant tones.

### 10. Bandwidth weighting

The measured 3 dB width of the tonal peak is first obtained from the discrete spectrum. In the implementation, the lower and upper frequencies are taken as the first bins around the peak for which the level drop reaches at least `3 dB`.

If `f_l` and `f_u` are those crossing frequencies, the measured width is:

```text
B_meas = f_u - f_l
```

An effective-width correction is then applied:

```text
B_eff = max(B_meas - 2 df, 0)
```

The corrected width is then converted to Bark:

```text
Δz_i = z(f_c + B_eff / 2) - z(f_c - B_eff / 2)
```

The corresponding weighting term is:

```text
w_1,i = (0.13 / (Δz_i + 0.13))^(1 / 0.29)
```

This correction compensates for analysis-window broadening and avoids attributing the FFT main-lobe width to the physical tonal bandwidth.

### 11. Frequency weighting

The frequency weighting term is:

```text
w_2,i = 1 / sqrt(1 + 0.2 (f_c / 700 + 700 / f_c)^2)
```

### 12. Excess-level weighting

The excess-level weighting term is:

```text
w_3,i = 1 - exp(-ΔL_i / 15)
```

### 13. Global tonal weight

For all relevant tones, the global tonal weight is obtained by quadratic summation:

```text
w_T = sqrt(Σ (w_1,i w_2,i w_3,i)^2)
```

In the current implementation, only the dominant relevant tone within a `0.5 Bark` neighborhood is retained, in order to avoid multiple counting of the same perceived component.

### 14. Loudness weighting

Let:

```text
N_s
```

be the loudness of the original spectrum, and:

```text
N_n
```

be the loudness after removal of the relevant tonal groups.

The loudness weight is then:

```text
w_L = max(0, 1 - N_n / N_s)
```

### 15. Final tonality

The final Aures tonality value is:

```text
K = C w_T^0.29 w_L^0.79
```

with:

```text
C = 1.09
```

The implemented value is clipped to:

```text
K <= 1.0 t.u.
```

This preserves the interpretation of the Aures reference signal as the calibration reference.

## Code-to-Equation Mapping

The correspondence between the principal formulas and the implementation is as follows:

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

## Execution

Validation helper:

```bash
PYTHONPATH=. python -m mosqito.sq_metrics.tonality.tonality_aures.tonality_aures_validation
```

Project-level validation entry point:

```bash
PYTHONPATH=. python validations/sq_metrics/tonality_aures/validation_tonality_aures.py
```

Automated test:

```bash
pytest -q tests/sq_metrics/tonality/test_tonality_aures.py
```

## Current Reference Values

The current expected values for the 9 SQAT validation files are approximately:

- `0 dB` -> `0.000000`
- `10 dB` -> `0.104714`
- `20 dB` -> `0.130652`
- `30 dB` -> `0.274639`
- `40 dB` -> `0.524800`
- `50 dB` -> `0.740900`
- `60 dB` -> `0.860003`
- `70 dB` -> `0.940890`
- `80 dB` -> `0.969318`

Reference signal:

- `1 kHz`, `60 dB SPL` pure tone -> about `0.986586 t.u.`
