import setuptools
import platform

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

python_requires = ">= 3.5"

# Pyleecan dependancies
install_requires = [
    "setuptools",
    "numpy>=1.18.1",
    "scipy>=1.4.1",
    "matplotlib>=3.1.3",
    "pandas",
]

tests_require = ["pytest>=5.4.1"]

setuptools.setup(
    name="mosqito",
    version="0.1.0",
    author="MoSQITo Developers",
    author_email="martin.glesser@eomys.com",
    description="Modular Sound Quality Integrated Toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eomys/MoSQITo",
    download_url="https://github.com/Eomys/MoSQITo/archive/0.1.0.tar.gz",
    packages=setuptools.find_packages(exclude=["documentation", "tutorials"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=python_requires,
    install_requires=install_requires,
    tests_require=tests_require,
)
