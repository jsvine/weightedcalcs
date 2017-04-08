[![Version](https://img.shields.io/pypi/v/weightedcalcs.svg)](https://pypi.python.org/pypi/weightedcalcs) [![Build status](https://travis-ci.org/jsvine/weightedcalcs.png)](https://travis-ci.org/jsvine/weightedcalcs) [![Code coverage](https://img.shields.io/coveralls/jsvine/weightedcalcs.svg)](https://coveralls.io/github/jsvine/weightedcalcs) [![Support Python versions](https://img.shields.io/pypi/pyversions/weightedcalcs.svg)](https://pypi.python.org/pypi/weightedcalcs)

# weightedcalcs

`weightedcalcs` is a `pandas`-based Python library for calculating weighted means, medians, standard deviations, and more.

## Features

- Plays well with `pandas`.
- Support for weighted means, medians, quantiles, standard deviations, and distributions.
- Support for grouped calculations, using `DataFrameGroupBy` objects.
- Raises an error when your data contains null-values.
- Full test coverage.

## Installation

```sh
pip install weightedcalcs
```

## Usage

### Getting started

Every weighted calculation in `weightedcalcs` begins with an instance of the `weightedcalcs.Calculator` class. `Calculator` takes one argument: the name of your weighting variable. So if you're analyzing a survey where the weighting variable is called `"resp_weight"`, you'd do this:

```python
import weightedcalcs as wc
calc = wc.Calculator("resp_weight")
```

### Types of calculations

Currently, `weightedcalcs.Calculator` supports the following calculations:

- `calc.mean(my_data, value_var)`: The weighted arithmetic average of `value_var`.
- `calc.quantile(my_data, value_var, q)`: The weighted quantile of `value_var`, where `q` is between 0 and 1.
- `calc.median(my_data, value_var)`: The weighted median of `value_var`, equivalent to `.quantile(...)` where `q=0.5`.
- `calc.std(my_data, value_var)`: The weighted standard deviation of `value_var`.
- `calc.distribution(my_data, value_var)`: The weighted proportions of `value_var`, interpreting `value_var` as categories.
- `calc.count(my_data)`: The weighted count of all observations, i.e., the total weight.
- `calc.sum(my_data, value_var)`: The weighted sum of `value_var`.

The `obj` parameter above should one of the following:

- A `pandas` `DataFrame` object
- A `pandas` `DataFrame.groupby` object
- A plain Python dictionary where the keys are column names and the values are equal-length lists.

### Basic example

Below is a basic example of using `weightedcalcs` to find what percentage of Wyoming residents are married, divorced, et cetera:

```python
import pandas as pd
import weightedcalcs as wc

# Load the 2015 American Community Survey person-level responses for Wyoming
responses = pd.read_csv("examples/data/acs-2015-pums-wy-simple.csv")

# `PWGTP` is the weighting variable used in the ACS's person-level data
calc = wc.Calculator("PWGTP")

# Get the distribution of marriage-status responses
calc.distribution(responses, "marriage_status").round(3).sort_values(ascending=False)

# -- Output --
# marriage_status
# Married                                0.425
# Never married or under 15 years old    0.421
# Divorced                               0.097
# Widowed                                0.046
# Separated                              0.012
# Name: PWGTP, dtype: float64
```

### More examples

[See this notebook to see examples of other calculations, including grouped calculations.](examples/notebooks/example-usage.ipynb)

### Weightedcalcs in the wild

- "[Procesando los microdatos de la Encuesta Permanente de Hogares](http://blog.jazzido.com/2017/01/09/procesando-microdatos-eph)," by Manuel Aristarán
- [BuzzFeedNews/2017-01-media-platform-and-news-trust-survey](https://github.com/BuzzFeedNews/2017-01-media-platform-and-news-trust-survey/blob/master/notebooks/platform-trust-additional-analysis.ipynb)
- [BuzzFeedNews/2016-12-transgender-rights-survey](https://github.com/BuzzFeedNews/2016-12-transgender-rights-survey/blob/master/notebooks/additional-analysis.ipynb)

## Other Python weighted-calculation libraries

- [`tinybike/weightedstats`](https://github.com/tinybike/weightedstats)
- [`nudomarinero/wquantiles`](https://github.com/nudomarinero/wquantiles/)

