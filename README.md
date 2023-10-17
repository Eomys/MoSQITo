# ![MOSQITO Logo](https://raw.githubusercontent.com/Eomys/MoSQITo/master/logo.png) MOSQITO

## Background

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

Besides the metrics, sound quality studies requires several tool like audio signal filtering or jury testing procedure for instance.

## Objectives

The objective of MOSQITO is therefore to provide a unified and modular development framework of key sound quality tools (including key SQ metrics) with open-source object-oriented technologies, favoring reproducible science and efficient shared scripting among engineers, teachers and researchers
community. The development roadmap of the project is presented in more details in the [scope section](./docs/scope.md) of the documentation. 

It is written in Python, one of the most popular free programming language in the scientific computing community. It is meant to be highly documented (use of Jupyter notebooks, tutorials) and validated with reference sound samples and scientific publications.

## Origin of the project

[EOMYS ENGINEERING](https://eomys.com/?lang=en) initiated this open-source project in 2020 for the study of electric motor sound quality. The project is now backed by [Green Forge Coop](https://www.linkedin.com/company/greenforgecoop/) non profit organization, who also supports the development of [Pyleecan](https://www.pyleecan.org) electrical machine simulation software.

## Documentation

Tutorials are available in the [tutorials](./tutorials/) folder. Documentation and validation of the MOSQITO functions are available in the [documentation](./docs/) folder.

## Getting MOSQITO
MOSQITO is available on [pip](https://pypi.org/project/pip/). Simply type in a shell the following command:

    pip install mosqito

This command line should download and install MOSQITO on your computer, along with the dependencies needed to compute SQ metrics.

If you need to import .uff or .unv files, you will need the pyuff package dependency. Note that 'pyuff' is released under the GPL license which prevents MOSQITO from being used in other software that must be under a more permissive license. To include the 'pyuff' dependancy anyway, type the following command:

    pip install mosqito[uff]

If you want to use MOSQITO coupled with SciDataTool, you will need SDT package dependency. To install it along with MOSQITO, use the following command:

    pip install mosqito[SciDataTool]

Note that all the depencies can be installed at once using:

    pip install mosqito[all]

## Contact

You can contact us on Github by opening an issue (to request a feature, ask a question or report a bug). 

## How to cite MOSQITO

If you are using MOSQITO in your research activities, please help our scientific visibility by citing our work! You can use the following citation in APA format:

Green Forge Coop. MOSQITO [Computer software]. https://doi.org/10.5281/zenodo.5284054

If you need to cite the current release of MOSQITO, please use the "Cite this repository" feature in the "About" section of this Github repository.


## Package using MOSQITO

[Soundscapy](https://github.com/MitchellAcoustics/Soundscapy): A python library for analysing and visualising soundscape assessments.

## Publications citing MOSQITO

San Millán-Castillo, R., Latorre-Iglesias, E., Glesser, M., *“Engagement capstone projects: A collaborative approach to a case study in psychoacoustics”*, The Journal of the Acoustical Society of America **152**, 2183 (2022) https://doi.org/10.1121/10.0014693

Kenneth Ooi, Zhen-Ting Ong, Karn N. Watcharasupat, Bhan Lam, Joo Young Hong, Woon-Seng Gan, *“ARAUS: A Large-Scale Dataset and Baseline Models of Affective Responses to Augmented Urban Soundscapes”*, SUBMITTED TO IEEE TRANSACTIONS ON AFFECTIVE COMPUTING, [arXiv:2207.01078](https://arxiv.org/abs/2207.01078), 2022

Wißbrock, P., Richter, Y., Pelkmann, D., Ren, Z. and Palmer, G., *“Cutting Through the Noise: An Empirical Comparison of Psychoacoustic and Envelope-based Features for Machinery Fault Detection”*, [arXiv:2211.01704](https://arxiv.org/abs/2211.01704), 2022

Erica Gallo, Guillaume Beaulieu and Christophe F. Schram, *“Annoyance factors of a maneuvering multicopter drone”*, 28th AIAA/CEAS Aeroacoustics 2022 Conference,  June 14-17, 2022, Southampton, UK. https://doi.org/10.2514/6.2022-2837

Menegatt, W. F., *“Desempenho de métodos de avaliação subjetiva online para quantificar a irritabilidade do ruído de refrigeradores”*, Dissertação (mestrado) - Universidade Federal de Santa Catarina, , Programa de Pós-Graduação em , Florianópolis, 2022. [Available online](https://repositorio.ufsc.br/handle/123456789/241023)

M. Glesser, S. Wanty, K. Degrendele, J. Le Besnerais, and S. Ni, *“Perceived sound quality analysis of Electric Drive Units under different switching control strategies,”* in 12th Aachen Acoustic Colloquium, Aachen, Nov. 2021.

M. Glesser, S. Ni, K. Degrendele, S. Wanty, and J. Le Besnerais, *“Sound quality analysis of Electric Drive Units under different switching control strategies,”* in SIA Automotive NVH comfort, Le Mans, 2021.

San Millán-Castillo, R., Latorre-Iglesias, E., Glesser, M., Wanty, S., Jiménez-Caminero, D., & Álvarez-Jimeno, J.M. (2021). MOSQITO: an open-source and free toolbox for sound quality metrics in the industry and education. *INTER-NOISE and NOISE-CON Congress and Conference Proceedings*, 12, 1164-1175. https://doi.org/10.3397/IN-2021-1767


