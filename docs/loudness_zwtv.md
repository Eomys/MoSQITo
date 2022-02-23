# MOSQITO Documentation
## Loudness: Zwicker method for time varying signals

### Introduction
The acoustic loudness computation according to Zwicker method was initially introduced for [stationary signals](./loudness_zwst.md). It was extended to arbitrary non-stationary sounds as an appendix of DIN 45631 standard (DIN 45631/A1:2010). In 2017, this method is included in the revision of ISO 532 (as section 6 of part 1, dedicated to Zwicker method). Note that, for normative continuity, the method is still in accordance with ISO 226:1987 equal loudness contours (instead of newer ISO 226:2003 definition).

In MOSQITO, the code is based on the C++ program published with ISO 532-1:2017.

### Validation of the implementation
The ISO 532-1:2017 standard provides a set of synthetic and technical signals covering representative applications to be used to validate any of its implementation. The standards also provides the compliance requirements. A step by step description of how to use MOSQITO to compute the loudness and the specific loudness is given in [this tutorial](../tutorials/tuto_loudness_zwtv.ipynb).

Annex B4 of the standard provides .wav files of synthetic signals to be used as input for time-varying loudness computation. The plots below compare the MOSQITO loudness computations for the test signal n°6 to the compliance requirements of the standards. MOSQITO implementation passes successfully the 8 tests from annex B4 (all compliance plots can be found in [this folder](../validations/sq_metrics/loudness_zwtv/output)). 

![](../validations/sq_metrics/loudness_zwtv/output/validation_loudness_zwtv_Test_signal_6_(tone_250_Hz_30_dB_-_80_dB)_Loudness.png)
![](../validations/sq_metrics/loudness_zwtv/output/validation_loudness_zwtv_Test_signal_6_(tone_250_Hz_30_dB_-_80_dB)_Specific.png)

*Loudness computation for ISO 532-1 test signal n°6 (A 250 Hz tone with a time-varying sound pressure level starting with 30 dB and increasing linearly to 80 dB). Top: overall loudness, Bottom: specific loudness at 2.5 Barks*

Annex B5 of the standard provides .wav files of technical signals to be used as input for time-varying loudness computation. The plot below compares the MOSQITO loudness computations for the test signal n°14 to the compliance requirements of the standards. MOSQITO implementation passes successfully 11 tests over the 12 from annex B4 (all compliance plots can be found in [this folder](../validations/sq_metrics/loudness_zwtv/output)). 

![](../validations/sq_metrics/loudness_zwtv/output/validation_loudness_zwtv_Test_signal_14_(propeller-driven_airplane)_Loudness.png)

*Loudness computation for ISO 532-1 test signal n°14 (Propeller-driven airplane noise)*

The test on signal 16 fails because the 5% tolerance limit is exceeded for more than 1% of the time at the end of the signal, during the decay from hairdryer noise to silence (see figure below). This issue is currently under investigation.

![](../validations/sq_metrics/loudness_zwtv/output/FAILED_validation_loudness_zwtv_Test_signal_16_(hairdryer)_Loudness.png)

*Loudness computation for ISO 532-1 test signal n°14 (Hairdryer noise)*

### References
DIN 45631:1991, Berechnung des Lautstärkepegels und der Lautheit aus dem Geräuschspektrum; Verfahren nach E. Zwicker (computation of loudness level and loudness from the sound spectrum; Zwicker method)

ISO 532-1:2017, Acoustics — Methods for calculating
loudness — Part 1: Zwicker method
