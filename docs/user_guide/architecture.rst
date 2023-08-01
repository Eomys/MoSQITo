Architecture of the package
---------------------------

:mod:`mosqito` functions are sorted by modules.Each subfolder contains one main function that is intended to be called by the user. The subfunctions are identified by a trailing underscore. Each main function is accompanied by a documentation (in the [docs](.) folder), a tutorial (in the [tutorials](../tutorials) folder) and a detailed validation of the implementation in the [validations](../validations) folder. 

For example, considering the function to compute the acoustic loudness according to the Zwicker method for stationary signals, the following elements can be found in :mod:`mosqito`:
 * source code of the function and subfunctions in the "/mosqito/sq_metrics/loudness/loudness_zwst/" folder,
 * source code of the main function in the "/mosqito/sq_metrics/loudness/loudness_zwst/loudness_zwst.py" file,
 * documentation in the docstring of the main function,  
 * tutorial explaining how to use the function in the "/tutorials/tuto_loudness_zwst.ipynb" file,
 * script used to validate the implementation by using the tests signals from the IS0 532-1 standard is available, together with the output of the validation process, in the "/validations/sq_metrics/loudness_zwst" folder.
