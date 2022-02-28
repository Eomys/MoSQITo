# MOSQITO Documentation
## How to contribute to MOSQITO


### Developer guideline

- The computation of a metric using a certain method shall be explicit (loudness_zwicker() instead of loudness(method='zwicker')

### Checklist for the development of a new metric
Each function in the function library shall come with:
- a documentation presenting the sources used for the implementation and showing how the implementation is validated (in the [documentation folder](.)) 
- a tutorial (in the [tutorial folder](../tutorials))
- a unit test (in the [tests folder](../tests)) 