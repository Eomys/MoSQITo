# MOSQITO Documentation
## Architecture of MOSQITO

### From a user point of view
All the functions available in MOSQITO can imported via the command:
```python
import mosqito
```

To import only a specific module like the sound quality metrics, the following command can be used:
```python
import mosqito.sq_metrics
```

The code of all the functions available in MOSQITO is accessible in the [mosqitox](../mosqito) folder, sorted by module. Each subfolder containes one main function that is intended to be called by the user. The subfunctions are identified by a trailing underscore. Each main function is accompanied by a documentation (in the [docs](.) folder) and a tutorial (in the [tutorials](../tutorials) folder). For example, the function to compute the acoustic loudness according to the Zwicker method for stationary signals is called [loudness_zwst](../mosqito/sq_metrics/loudness/loudness_zwst/loudness_zwst.py) and can be found in the [mosqito/sq_metrics/loudness/loudness_zwst](../mosqito/sq_metrics/loudness/loudness_zwst/) folder. Its documentation is avalable in the [docs/loudness_zwst.md](../docs/loudness_zwst.md) file and



### MOSQITO as a standalone SQ tool
For the users that would like to use MOSQITO independently, a scripting interface to the functions mentionned above is proposed. This interface mainly relies on [SciDataTool](https://github.com/Eomys/SciDataTool), an open-source Python package for scientific data handling. Its objective is to provide a user-friendly, unified, flexible module to postprocess any kind of signal.

### Developer corner
Each function in the function library shall come with:
- a documentation presenting the sources used for the implementation and showing how the implementation is validated (in the [documentation folder](.)) 
- a tutorial (in the [tutorial folder](../tutorials))
- a unit test (in the [tests folder](../tests)) 

The scripting interface, relies upon an object oriented approach. All operations on audio signals are managed through the Audio class and its methods.
