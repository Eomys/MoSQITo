import setuptools

# /!\ update before a release
MoSQITo_VERSION = "0.3.7"

# MoSQITo description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

python_requires = ">= 3.5"

# MoSQITo dependencies
with open("requirements.txt", "r") as file:
    requirements = file.readlines()
    install_requires = "".join(
        requirements
    ).splitlines()  # remove endline in each element

tests_require = ["pytest>=5.4.1", "pandas", "openpyxl", "SciDataTool", "matplotlib"]
uff_require = ["pyuff"]
scidatatool_require = ["SciDataTool"]
all_require = tests_require + uff_require

setuptools.setup(
    name="mosqito",
    version=MoSQITo_VERSION,
    author="MoSQITo Developers",
    author_email="martin.glesser@eomys.com",
    description="Modular Sound Quality Integrated Toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eomys/MoSQITo",
    download_url="https://github.com/Eomys/MoSQITo/archive/v{}.tar.gz".format(
        MoSQITo_VERSION
    ),
    packages=setuptools.find_packages(
        exclude=[
            "documentation",
            "tutorials",
            "validations",
            "tests",
        ]
    ),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=python_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        "testing": tests_require,
        "uff": uff_require,
        "SciDataTool": scidatatool_require,
        "all": all_require,
    },
)
