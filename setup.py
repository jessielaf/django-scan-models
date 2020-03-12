# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

try:
    from m2r import parse_from_file

    long_description = parse_from_file("README.md")
except ImportError as e:
    long_description = ""

here = path.abspath(path.dirname(__file__))

setup(
    name="django-scan-models",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version="0.1",
    description="Django scan models: Parse django models to frontend validation",
    long_description=long_description,
    # The project's main homepage.
    url="https://github.com/jessielaf/django-scan-models",
    # Author details
    author="Jessie Liauw A Fong",
    author_email="jessielaff@live.nl",
    # Choose your license
    license="MIT",
    # See https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    # What does your project relate to?
    # todo: Add keywords and required packages
    # keywords="ansible alternative infrastructure as actual code deployment installing setup",
    packages=find_packages(),
    include_package_data=True,
)
