Installation
============

MOSQITO is available on pip. Simply type in a shell the following command: ::

  pip install mosqito
This command line should download and install MOSQITO on your computer, along with the dependencies needed to compute SQ metrics.

If you need to import .uff or .unv files, you will need the pyuff package dependency. Note that 'pyuff' is released under the GPL 
license which prevents MOSQITO from being used in other software that must be under a more permissive license. To include the 'pyuff' 
dependancy anyway, type the following command: ::

    pip install mosqito[uff]
