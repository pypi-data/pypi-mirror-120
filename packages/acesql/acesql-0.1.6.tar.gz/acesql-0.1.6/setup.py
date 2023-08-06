from setuptools import setup

with open("README.md", "r") as fn:
    long_desc = fn.read()

setup(
    name = 'acesql',
    version = '0.1.6',
    description = 'Access to ACE Databases',
    py_modules = ["acesql"],
    package_dir = {'': 'src'},
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description = long_desc,
    long_description_content_type="text/markdown",
    install_requires = [
        "pyspark ~= 3.1.2"
    ],
    url="https://git.sonova.com/ACE/acedbpp.git",
    author="Cem Bakar",
    author_email="cem.bakar@sonova.com",
)
