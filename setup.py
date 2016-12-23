from setuptools import setup

setup(
    name="weightedcalcs",
    version="0.0.0",
    description="Pandas-based utility to calculate weighted means, medians, distributions, standard deviations, and more.",
    url="http://github.com/jsvine/weightedcalcs",
    author="Jeremy Singer-Vine",
    author_email="jsvine@gmail.com",
    license="MIT",
    packages=[
        "weightedcalcs"
    ],
    install_requires=[
        "pandas>=0.19"
    ]
)
