MoSQITo
=======

(**Mo**\ dular **S**\ ound **Q**\ uality **I**\ ntegrated **To**\ olbox)

Background
----------

Sound quality (SQ) metrics are developed by acoustic engineers and
researchers to provide an objective assessment of the pleasantness of a
sound. Different metrics exist depending on the nature of the sound to
be tested. Some of these metrics are already standardized, while some
others rely on scientific articles and are still under active
development. The calculation of some sound quality metrics are included
in major commercial acoustic and vibration measurement and analysis
software. However, some of the proposed metrics results from in-house
implementation and can be dependent from one system to another. Some
implementations may also lack of complete documentation and validation
on publicly available standardized sound samples. Several
implementations of SQ metrics in different languages can been found
online, confirming the interest of the engineering and scientific
community, but they often use Matlab signal processing commercial
toolbox.

Objectives
----------

The objective of MoSQITo is therefore to provide a unified and modular
development framework of key sound quality metrics with open-source
object-oriented technologies, favoring reproducible science and
efficient shared scripting among engineers, teachers and researchers
community.

It is written in Python, one of the most popular free programming
language in the scientific computing community. It is meant to be highly
documented (use of Jupyter notebooks, tutorials) and validated with
reference sound samples and scientific publications.

Scope
-----

The scope of the project is to implement the following first set of
metrics:

+-------------------+------------------------+---+-------+------------+
|                   | Reference              | A | Under | Waiting    |
|                   |                        | v | d     | for your   |
|                   |                        | a | evelo | co         |
|                   |                        | i | pment | ntribution |
|                   |                        | l |       |            |
|                   |                        | a |       |            |
|                   |                        | b |       |            |
|                   |                        | l |       |            |
|                   |                        | e |       |            |
+===================+========================+===+=======+============+
| Loudness for      | ISO 532B:1975 ; DIN    | x |       |            |
| steady signals    | 45631:1991 ; ISO       |   |       |            |
| (Zwicker method)  | 532-1:2017 method 1    |   |       |            |
+-------------------+------------------------+---+-------+------------+
| Loudness for      | DIN 45631/A1:2010 ;    |   | x     |            |
| non-stationary    | ISO 532-1:2017 method  |   |       |            |
| (Zwicker method)  | 2                      |   |       |            |
+-------------------+------------------------+---+-------+------------+
| Sharpness         | DIN 45692:2009         |   |       | x          |
+-------------------+------------------------+---+-------+------------+
| Roughness /       | To be defined          |   |       | x          |
| Fluctuation       |                        |   |       |            |
| Strength          |                        |   |       |            |
+-------------------+------------------------+---+-------+------------+
| Tonality (Hearing | ECMA-74:2019 annex G   |   |       | x          |
| model)            |                        |   |       |            |
+-------------------+------------------------+---+-------+------------+

As a second priority, the project could address the following metrics:

+------------------------------+--------------+---+------+-----------+
|                              | Reference    | A | U    | Waiting   |
|                              |              | v | nder | for your  |
|                              |              | a | dev  | con       |
|                              |              | i | elop | tribution |
|                              |              | l | ment |           |
|                              |              | a |      |           |
|                              |              | b |      |           |
|                              |              | l |      |           |
|                              |              | e |      |           |
+==============================+==============+===+======+===========+
| Loudness for steady signals  | ISO          |   |      | x         |
| (Moore/Glasberg method)      | 532-2:2017   |   |      |           |
+------------------------------+--------------+---+------+-----------+
| Loudness for non-stationary  | Moore, 2014  |   |      | x         |
| (Moore/Glasberg method)      |              |   |      |           |
+------------------------------+--------------+---+------+-----------+
| Sharpness (using             | Hales-Swift  |   |      | x         |
| Moore/Glasberg loudness)     | and Gee,     |   |      |           |
|                              | 2017         |   |      |           |
+------------------------------+--------------+---+------+-----------+
| Tone-to-noise ratio /        | ECMA-74:2019 |   |      | x         |
| Prominence ratio             | annex D ;    |   |      |           |
| (occupational noise,         | ISO          |   |      |           |
| discrete tones)              | 7719:2018    |   |      |           |
+------------------------------+--------------+---+------+-----------+
| Tone-to-noise ratio          | DIN 45681    |   |      | x         |
| (environmental noise,        |              |   |      |           |
| automatic tone detection)    |              |   |      |           |
+------------------------------+--------------+---+------+-----------+
| Tone-to-noise ratio          | ISO 1996-2   |   |      | x         |
| (environmental noise)        |              |   |      |           |
+------------------------------+--------------+---+------+-----------+
| Tone-to-noise ratio          | ANSI         |   |      | x         |
| (environmental noise)        | S1.13:2005   |   |      |           |
+------------------------------+--------------+---+------+-----------+

In parallel, tools for signal listening and manipulation will be
developed. The objective is to be able to apply some modification to a
signal (filtering, tone removal, etc.) and assess the impact on
different SQ metrics.

Of course, any other sound quality related implementation by anyone who
wants to contribute is welcome.

Contact
-------

You can contact us on Github by opening an issue (to request a feature,
ask a question or report a bug).

References
----------

Hales Swift, S., and Gee, K. L. (2017). “Extending sharpness calculation
for an alternative loudness metric input,” J. Acoust. Soc. Am.142,
EL549. Moore, B. C. J. (2014). “Development and Current Status of the
“Cambridge” Loudness Models,” Trends in Hearing, vol. 18: 1-29
