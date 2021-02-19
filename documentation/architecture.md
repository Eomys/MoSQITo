# MOSQITO Documentation
## Architecture of the toolbox

From the point of view of the user, MOSQITO can be used in two way. 

### MOSQITO as a function library 
All functions available in MOSQITO are listed in [mosqito/functions](../mosqito/functions). Each folder corresponds to one specific function. Each function can be called by the main script comp_xxx contained the folders. 

As far as the SQ metrics are concerned, the main script takes as input argument the time signal (as numpy ndarray) and some computation parameter. It returns a dictionary with the calculated metrics.

Most of the plot functions are volontarily excluded from the function library. The objective is to focus on the functions related to sound quality and make them available for integration in other applications. 

### MOSQITO as a standalone SQ tool
For the users that would like to use MOSQITO independently, a scripting interface to the functions mentionned above is proposed. This interface mainly relies on [SciDataTool](https://github.com/Eomys/SciDataTool), an open-source Python package for scientific data handling. Its objective is to provide a user-friendly, unified, flexible module to postprocess any kind of signal.

### Developer corner
Each function in the function library shall come with:
- a documentation presenting the sources used for the implementation and showing how the implementation is validated (in the [documentation folder](.)) 
- a tutorial (in the [tutorial folder](../tutorials))
- a unit test (in the [tests folder](../mosqito/tests)) 

The scripting interface, relies upon an object oriented approach. All operations on audio signals are managed through the Audio class and its methods.
