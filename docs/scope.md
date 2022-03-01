# Scope of the project

## Sound quality metrics
The scope of the project is to implement the following first set of
metrics:

|                                                    | Reference                                            | Validated                                          | Available                                     | Under dev. | To do |
|:-------------------------------------------------- |:---------------------------------------------------- |:-------------------------------------------:|:---------------------------------------------:|:----------:|:-----:|
| Loudness for<br>steady signals<br>(Zwicker method) | ISO 532B:1975<br>DIN 45631:1991<br>ISO 532-1:2017 §5 | [x](./loudness_zwst.md)               | x |  |  |
| Loudness for non-stationary<br>(Zwicker method)    | DIN 45631/A1:2010<br>ISO 532-1:2017 §6               | [x](./loudness_zwtv.md)             | x |  |  |
| Loudness for non-stationary<br>(ECMA method)       | ECMA 418-2:2019 section 5<br>Sottek, 2016            | [x](./loudness_ecma.md)                     | x |  |  |
| Roughness                                          | Daniel and Weber, 1997                               | [x](./roughness_dw.md)   | x |  |  |
| Roughness                                          | ECMA-418-2:2020                                      |                                             |  |  | x |
| Fluctuation Strength                               | To be defined                                        |                                             |  |  | x |
| Sharpness                                          | DIN 45692:2009                                       | [x](./sharpness_din.md)                         | x |  |  |
| Tonality (Hearing model)                           | ECMA-74:2019 annex G                                 |                                             |  |   | x |

As a second priority, the project could address the following metrics:

|                                                                                     | Reference                             | Validated | Available | Under dev. | To do |
|:----------------------------------------------------------------------------------- |:------------------------------------- |:---------:|:---------:|:----------:|:-----:|
| Loudness for steady signals<br>(Moore/Glasberg method)                              | ISO 532-2:2017                        |           |           |            | x     |
| Loudness for non-stationary<br>(Moore/Glasberg method)                              | Moore, 2014                           |           |           |            | x     |
| Sharpness (using <br>Moore/Glasberg loudness)                                       | Hales-Swift<br>and Gee, 2017          |           |           |            | x     |
| Tone-to-noise ratio / Prominence <br> ratio (occupational noise,<br>discrete tones) | ECMA-74:2019 annex D<br>ISO 7719:2018 |           | x         |            |       |
| Tone-to-noise ratio<br>(environmental noise,<br>automatic tone detection)           | DIN 45681                             |           |           |            | x     |
| Audibility of tone in noise <br>(Engineering method)                                | ISO 1996-2 annex J                    |           |           |             |   x   |
| Audibility of tone in noise <br>(Survey method)                                     | ISO 1996-2 annex K                    |           |           |       x     |       |
| Tone-to-noise ratio<br>(environmental noise)                                        | ANSI S1.13:2005                       |           |           |            | x     |


## Other SQ tools
In parallel, tools for signal listening and manipulation will be
developed. The objective is to be able to apply some modification to a
signal (filtering, tone removal, etc.) and assess the impact on
different SQ metrics. The integration of tools to define jury tests and 
analyze the results is also planned.

Of course, any other sound quality related implementation by anyone who
wants to contribute is welcome.

## References

Daniel, P., and Weber, R. (1997). “Psychoacoustical Roughness: Implementation 
of an Optimized Model”, Acta Acustica, Vol. 83: 113-123

Hales Swift, S., and Gee, K. L. (2017). “Extending sharpness calculation
for an alternative loudness metric input,” J. Acoust. Soc. Am.142,
EL549. 

Moore, B. C. J. et al. (2016) ‘A Loudness Model for Time-Varying Sounds Incorporating Binaural Inhibition’, Trends in Hearing. [doi: 10.1177/2331216516682698](https://doi.org/10.1177/2331216516682698).

Sottek, R. (2016) A Hearing Model Approach to Time-Varying Loudness, Acta Acustica united with Acustica, vol. 102, no. 4, pp. 725-744.