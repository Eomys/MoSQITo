# MOSQITO Documentation
## Tone-to-noise ratio (TNR) and Prominence ratio (PR) according to ECMA 74

### Introduction

The acoustic tonality metrics calculation was introduced in the ECMA 74. The calculation is based upon the comparison between the level of each tonal candidate and the  level of the surrounding spectrum. 

The detection of the tonal candidates is not included in the ECMA 74. Two different methods have been added to detect the potential tonal components:
 - the method by Sottek using a smoothed spectrum,
 - the classic method by Aures/Terhardt using the close frequency neighbours.

### Total evaluation of multiple tones

The ECMA TR/108 has confirmed the reliability of the use of global values T-TNR and T-PR. They are calculated as the sum of individual tonal values.

### Validation of the implementation

The standard doesn't include a validation procedure.




### References

ECMA-74, Measurement of Airborne Noise emitted by Information Technology and Telecommunications Equipment, annex D, december 2019.

W. Bray, Methods for automating prominent tone evaluation and for considering variations with time or other reference quantities, euronoise, 2008.

ECMA TR/108, Proposal of new parameters, T-TNR and T-PR for total evaluation of multiple tones, june 2019.
