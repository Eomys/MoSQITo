# MOSQITO Documentation
## How to contribute to MOSQITO

### Become part of the MOSQITO community

There are several ways to contribute to MOSQITO. You can:
1. Use it and report the bugs or mssing informations. 
2. Share any idea you would have to improve the documentation, if you are familiar with psychoacoustic.
3. Share any sound quality related implementation you could have developed (even in another programing language). 
4. Start contributing by tackling one of the issues labeled with ["good first issue"](https://github.com/Eomys/MoSQITo/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)
5. Implement one of the function listed in the [scope section](scope.md) of the documentation.

In any case, please let the community know about your [future] contribution ideally through a [GitHub issue](https://github.com/Eomys/MoSQITo/issues) or by sending an email at mosqito(at)framalistes.org that redirect to the maintainers. 

### Developer guideline

- Open an issue to describe the feature you want to add
- Make a fork of MOSQITO on your GitHub account
- On the fork, we advice to keep the master untouched and make your nex development on a branch. This way, if needed, you will be able to start another parallel development in a third branch created from the master.
- The computation of a metric using a certain method shall be explicit (loudness_zwicker() instead of loudness(method='zwicker')

### Checklist for the development of a new metric
Each function in the function library shall come with:
- a documentation presenting the sources used for the implementation and showing how the implementation is validated (in the [documentation folder](.)) 
- a tutorial (in the [tutorial folder](../tutorials))
- a unit test (in the [tests folder](../tests)) 