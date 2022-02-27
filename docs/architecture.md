# MOSQITO Documentation
## Architecture of MOSQITO

### From a user point of view
All the functions available in MOSQITO can be imported via the command:
```python
import mosqito
```

To import only a specific module like the sound quality metrics, the following command can be used:
```python
import mosqito.sq_metrics
```

The code of all the functions available in MOSQITO is accessible in the [mosqito](../mosqito) folder, sorted by module. Each subfolder containes one main function that is intended to be called by the user. The subfunctions are identified by a trailing underscore. Each main function is accompanied by a documentation (in the [docs](.) folder), a tutorial (in the [tutorials](../tutorials) folder) and a detailed validation of the implementation in the [validations](../validations) folder. For example, the function to compute the acoustic loudness according to the Zwicker method for stationary signals is called [loudness_zwst](../mosqito/sq_metrics/loudness/loudness_zwst/loudness_zwst.py) and can be found in the [mosqito/sq_metrics/loudness/loudness_zwst](../mosqito/sq_metrics/loudness/loudness_zwst/) folder. Its documentation is avalable in the [docs/loudness_zwst.md](../docs/loudness_zwst.md) file and the tutorial explaing how to use the function is available in the [tutorials/tuto_loudness_zwst.ipynb](../tutorials/tuto_loudness_zwst.ipynb) file. Finally the script used to validate the implementation by using the tests signals from the IS0 532-1 standard is available, together with the output of the validation process, in the [validations/sq_metrics/loudness_zwst](../validations/sq_metrics/loudness_zwst) folder.

### From a developer point of view





