# MOSQITO Documentation
## Sound level meter functions

### Introduction

There are operations that are important. We need to be able to perform them to have a better understanding of the data with which we work and to be able to use them to calculate data of interest. For this are the sonometer functions.

A step by step description of how to use MOSQITO to use the sonometer functions is given in [this tutorial](../tutorials/tuto_sound_level_meter.ipynb)

### Validation of the implementation

This section of the MoSQITo repository are mathematical accounts. For this reason, the validations have consisted of comparing two results: the results of the software and the simulated results in Excel.

Accounts are backed by regulations. Among them we have ISO 1996 part 1, ISO 1996 part 2 and the international standard IEC 61672: 2014 (This is for the A weighting and the C weighting).

We have taken three signals to carry out the calculations. These signals are located at ../tests/input and These are a white noise (349315__newagesoup__white-noise-10s.wav), a pink noise (349312__newagesoup__pink-noise-10s.wav) and a pure tone at 1000 Hz (554329__patobottos__beep-sound-of-1000-hz).

For the functions that work with Thirds of an Octave, the three signals (input array) were introduced to the program. In the same way, the data of the signals are entered in an Excel in which the desired operation of the function has been replicated. If the function and Excel return the same result, it is shown that the function works well and returns the correct result.

In the case of functions that work with temporary samples, only one of these three signals is entered and the procedure is the same, results are compared between the function and Excel.

### References

ISO 1996 - 1: Description, measurement and evaluation of environmental noise Part 1: Basic magnitudes and evaluation methods.

ISO 1996 - 2: Description, measurement and evaluation of environmental noise Part 2: determination of sound pressure levels.

IEC 61672-1:2014, Electroacoustics - Sound level meters - Part 1: Specifications.