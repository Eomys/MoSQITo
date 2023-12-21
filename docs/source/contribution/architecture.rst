.. _architecture:

Architecture of the package
===========================

:mod:`mosqito` functions are sorted by modules.Each subfolder contains one main function that is intended to be called by the user. The subfunctions are identified by a trailing underscore. Each main function is accompanied by a documentation (in the [docs](.) folder), a tutorial (in the [tutorials](../tutorials) folder) and a detailed validation of the implementation in the [validations](../validations) folder. 

For example, considering the function to compute the acoustic loudness according to the Zwicker method for stationary signals, the following elements can be found in :mod:`mosqito`:
 * source code of the function and subfunctions in the metric folder: ::

      /mosqito/sq_metrics/loudness/loudness_zwst/
 * source code of the main function in the function file: ::
 
      /mosqito/sq_metrics/loudness/loudness_zwst/loudness_zwst.py
 * documentation in the docstring of the main function, including an example of how to use the function
 * script used to validate the implementation with the tests signals from the IS0 532-1 standard is available, together with the output of the validation process, in the metric validation folder: ::

      /validations/sq_metrics/loudness_zwst
