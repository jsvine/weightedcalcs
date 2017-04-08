from setuptools import setup
import os

NAME = "weightedcalcs"
HERE = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join(HERE, NAME, '__version__.py')) as f:
    exec(f.read(), {}, version_ns)

setup(
    name=NAME,
    version=version_ns['__version__'],
    description="Pandas-based utility to calculate weighted means, medians, distributions, standard deviations, and more.",
    url="http://github.com/jsvine/weightedcalcs",
    author="Jeremy Singer-Vine",
    author_email="jsvine@gmail.com",
    license="MIT",
    packages=[
        NAME
    ],
    install_requires=[
        "pandas>=0.19"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
