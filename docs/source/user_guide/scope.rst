.. _scope:

Scope of the project
====================

SQ metrics
----------

The scope of the project is to implement the following first set of metrics:

.. list-table:: 
   :header-rows: 1

   * -  
     - Reference
     - Validated
     - Available
     - Under dev.
     - To do
   * - Loudness for steady signals (Zwicker method)
     - :footcite:t:`ISO.532B:1975` 
       | :footcite:t:`DIN.45631:1991`
       | :footcite:t:`ISO.532B-1:2017`
     - X 
     - X 
     - 
     - 
   * - Loudness for non-stationary (Zwicker method)
     - :footcite:t:`DIN.45631/A1:2010-03`
       | :footcite:t:`ISO.532B-1:2017`
     - X 
     - X 
     - 
     - 
   * - Loudness for non-stationary (ECMA method)
     - :footcite:t:`ECMA 418-2:2022`
     - X 
     - X 
     - 
     - 
   * - Sharpness 
     - :footcite:t:`DIN.45692:2009`
     - X 
     - X 
     - 
     - 
   * - Roughness (Daniel and Weber)
     - :footcite:t:`roughnessDW`
     - X 
     - X 
     - 
     - 
   * - Roughness (ECMA method)
     - :footcite:t:`ECMA 418-2:2022`
     -  
     -  
     - X
     - 

   * - Fluctuation Strength
     - To be defined
     -  
     -  
     - 
     - X
   * - Tonality (Hearing model)
     - :footcite:t:`ECMA-74`
     -  
     -  
     - X
     - 
   * - Speech Intelligibility index
     - :footcite:t:`ANSI.S3.5:2017`  
     - X
     - X
     -
     -

As a second priority, the project could address the following metrics:

.. list-table:: 
   :header-rows: 1

   * -  
     - Reference
     - Validated
     - Available
     - Under dev.
     - To do
   * - Loudness for steady signals (Moore/Glasberg method)
     - :footcite:t:`ISO.532B-1:2017`
     -  
     -  
     - 
     - X 
   * - Loudness for non-stationary (Moore/Glasberg method)
     - :footcite:t:`loudnessMoore`
     -   
     -   
     - 
     - X
   * - Sharpness (using Moore/Glasberg loudness)
     - :footcite:t:`sharpnessSG`
     - 
     -  
     - 
     - X 
   * - Tone-to-noise ratio / Prominence ratio (occupational noise, discrete tones)
     - :footcite:t:`ECMA-74`
     -  
     - X 
     - 
     - 
   * - Tone-to-noise ratio (environmental noise, automatic tone detection)
     - :footcite:t:`DIN.45681:2005-03`
     -  
     -  
     - 
     - X

   * - Audibility of tone in noise (Engineering method)
     - :footcite:t:`ISO.1996-2:2017`
     -  
     -  
     - 
     - X
   * - Audibility of tone in noise (Survey method)    
     - :footcite:t:`ISO.1996-2:2017`
     -  
     -  
     - X
     - 
   * - Tone-to-noise ratio (environmental noise) 
     - :footcite:t:`ANSI.S1.13-2005`
     -  
     -  
     - 
     - X 

Other SQ tools
--------------

In parallel, tools for signal listening and manipulation will be
developed. The objective is to be able to apply some modification to a
signal (filtering, tone removal, etc.) and assess the impact on
different SQ metrics. The integration of tools to define jury tests and 
analyze the results is also planned.

Of course, any other sound quality related implementation by anyone who
wants to contribute is welcome.

References
--------------
.. footbibliography::

