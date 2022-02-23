# MOSQITO Documentation
## Sharpness according to DIN 45692 method

### Introduction

The acoustic sharpness computation was introduced as a standard in the DIN 45692. The computation is based upon the specific loudness distribution of the sound. The specific loudness is weighted by ponderation functions. By default, the 'din' weighting function is used in Mosqito. Several other weighting functions are implemented:
* Aures
* Von Bismarck
* Fastl

The code is based on the version of the standard published in 2009 and the loudness is calculated according to Zwicker method, as described in ISO 532:B.

### Validation of the implementation

The DIN 45692:2009 standard provides a set of synthetic signals to be used to validate any of its implementation. The standards also provides the compliance requirements. The sharpness is calculated by mosqito for the 20 broad-band signals and for the 21 narrow-band signals filtered with different center frequencies provided with the standard. The results are compared to the requirements in the figures below.

![](../validations/sq_metrics/sharpness_din/output/validation_sharpness_Broad-band_noise.png)

![](../validations/sq_metrics/sharpness_din/output/validation_sharpness_Narrow-band_noise.png)

*The validation plots and scripts can be found in [this folder](../validations/sq_metrics/sharpness_din).*

### References

DIN 45692_2009E, Messtechnische Simulation der Hörempfindung Schärfe (Measurement technique for the simulation of the auditory sensation of sharpness)

ISO 532-1:2017, Acoustics — Methods for calculating
loudness — Part 1: Zwicker method


