MOSQITO documentation
===================================

**Version**: |version|

.. toctree::
   :maxdepth: 1
   :hidden:

   User guide </source/user_guide/index>
   API reference </source/reference/index>
   Contribution </source/contribution/index>


The objective of MOSQITO is to provide a unified and modular development framework of key sound quality tools 
(including key SQ metrics), favoring reproducible science and efficient shared scripting among engineers, teachers and researchers
community. The development roadmap of the project is presented in more details in the :ref:`scope` of the documentation. 

It is written in Python, one of the most popular free programming language in the scientific computing community. 
It is meant to be highly documented and validated with reference sound samples and scientific publications.



Background
----------

Sound quality (SQ) metrics are developed by acoustic engineers and researchers to provide an objective assessment of the pleasantness of a
sound. Different metrics exist depending on the nature of the sound to be tested. Some of these metrics are already standardized, while some
others rely on scientific articles and are still under active development. The calculation of some sound quality metrics are included
in major commercial acoustic and vibration measurement and analysis software. However, some of the proposed metrics results from in-house
implementation and can be dependent from one system to another. Some implementations may also lack of complete documentation and validation
on publicly available standardized sound samples. Several implementations of SQ metrics in different languages can been found
online, confirming the interest of the engineering and scientific community, but they often use Matlab signal processing commercial
toolbox. Besides the metrics, sound quality studies requires several tool like audio signal filtering or jury testing procedure for instance.



Contact
-------

You can contact us on Github by opening an issue (to request a feature, ask a question or report a bug).
https://github.com/Eomys/MoSQITo


How to cite MOSQITO
---------------------

If you are using MOSQITO in your research activities, please help our scientific visibility by citing our work! You can use the following citation in APA format:

Green Forge Coop. MOSQITO (Version 1.1.1). https://doi.org/10.5281/zenodo.10629475
If you need to cite the current release of MOSQITO, please use the "Cite this repository" feature in the "About" section of the `Github repository <https://github.com/Eomys/MoSQITo>`_.


Packages using MOSQITO
------------------------

`Soundscapy <https://github.com/MitchellAcoustics/Soundscapy>`_: A python library for analysing and visualising soundscape assessments.

`miniDSP <https://www.minidsp.com/applications/acoustic-measurements/psychoacoustic-measurements-with-mosqito>`_: An acquisition tool with psychoacoustic parameters estimation.

Publications citing MOSQITO
----------------------------

:cite:empty:`FA2023` 
:cite:empty:`JASA23` 
:cite:empty:`internoise23` 
:cite:empty:`IEEE2022` 
:cite:empty:`ICASSP2023` 
:cite:empty:`AIAA2022` 
:cite:empty:`menegatt`
:cite:empty:`AAC2021`
:cite:empty:`SIA2021` 
:cite:empty:`internoise21`

.. bibliography::