# MOSQITO Documentation
## How to contribute to MOSQITO

There are several ways to contribute to MOSQITO. You can:
1. Use it and report the bugs or mssing informations (ideally through a [GitHub issue](https://github.com/Eomys/MoSQITo/issues) or by sending an email at mosqito(at)framalistes.org that redirect to the maintainers). 
2. Share any idea you woud have to improve the documentation, if you are familiar with psychoacoustic (ideally through a [GitHub issue](https://github.com/Eomys/MoSQITo/issues) or by sending an email at mosqito(at)framalistes.org that redirect to the maintainers).


### Developer guideline

- Open an issue to describe 
- The computation of a metric using a certain method shall be explicit (loudness_zwicker() instead of loudness(method='zwicker')

### Checklist for the development of a new metric
Each function in the function library shall come with:
- a documentation presenting the sources used for the implementation and showing how the implementation is validated (in the [documentation folder](.)) 
- a tutorial (in the [tutorial folder](../tutorials))
- a unit test (in the [tests folder](../tests)) 