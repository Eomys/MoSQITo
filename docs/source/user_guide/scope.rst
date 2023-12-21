.. _scope:

Scope of the project
====================


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
     - ISO 532B:1975 
       | DIN 45631:1991
       | ISO 532-1:2017 §5 
     - X 
     - X 
     - 
     - 
   * - Loudness for non-stationary (Zwicker method)
     - DIN 45631/A1:2010
       | ISO 532-1:2017 §6
     - X 
     - X 
     - 
     - 
   * - Loudness for non-stationary (ECMA method)
     - ECMA 418-2:2019 section 5, Sottek, 2016
     - X 
     - X 
     - 
     - 
   * - Sharpness 
     - DIN 45692:2009
     - X 
     - X 
     - 
     - 
   * - Roughness (Daniel and Weber)
     - Daniel and Weber, 1997
     - X 
     - X 
     - 
     - 
   * - Roughness (ECMA method)
     - ECMA-418-2:2020
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
     - ECMA-74:2019 annex G
     -  
     -  
     - X
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
     - ISO 532-2:2017
     -  
     -  
     - 
     - X 
   * - Loudness for non-stationary (Moore/Glasberg method)
     - Moore, 2014
     -   
     -   
     - 
     - X
   * - Sharpness (using Moore/Glasberg loudness)
     - Hales-Swift and Gee, 2017
     -  
     -  
     - 
     - X 
   * - Tone-to-noise ratio / Prominence ratio (occupational noise, discrete tones)
     - ECMA-74:2019 annex D ISO 7719:2018
     -  
     - X 
     - 
     - 
   * - Tone-to-noise ratio (environmental noise, automatic tone detection)
     - DIN 45681
     -  
     -  
     - 
     - X

   * - Audibility of tone in noise (Engineering method)
     - ISO 1996-2 annex J
     -  
     -  
     - 
     - X
   * - Audibility of tone in noise (Survey method)    
     - ISO 1996-2 annex K
     -  
     -  
     - X
     - 
   * - Tone-to-noise ratio (environmental noise) 
     - ANSI S1.13:2005
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

Daniel, P., and Weber, R. (1997). “Psychoacoustical Roughness: Implementation 
of an Optimized Model”, Acta Acustica, Vol. 83: 113-123

Hales Swift, S., and Gee, K. L. (2017). “Extending sharpness calculation
for an alternative loudness metric input,” J. Acoust. Soc. Am.142,
EL549. 

Moore, B. C. J. et al. (2016) ‘A Loudness Model for Time-Varying Sounds Incorporating Binaural Inhibition’, Trends in Hearing. [doi: 10.1177/2331216516682698](https://doi.org/10.1177/2331216516682698).

Sottek, R. (2016) A Hearing Model Approach to Time-Varying Loudness, Acta Acustica united with Acustica, vol. 102, no. 4, pp. 725-744.