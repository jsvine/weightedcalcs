# weightedcalcs `v0.0.0`

`weightedcalcs` is a `pandas`-based Python library for calculating weighted means, medians, standard deviations, and more.

## Features

- Plays well with `pandas`.
- Built-in support for grouped calculations, using `DataFrameGroupBy` objects.
- Raises an error when your data contains null-values.

## Installation

```sh
pip install weightedcalcs
```

## Usage

### Getting started

Every weighted calculation in `weightcalcs` begins with an instance of the `weightcalcs.Calculator` class. `Calculator` takes one argument: the name of your weighting variable. So if you're analyzing a survey where the weighting variable is called `"resp_weight"`, you'd do this:

```python
import weightcalcs
wc = weightcalcs.Calculator("resp_weight")
```

### Types of calculations

Currently, `weightcalcs.Calculator` supports the following calculations:

- `wc.count(my_data)`: The weighted count of all observations, i.e., the total weight.
- `wc.sum(my_data, value_var)`: The weighted sum of `value_var`.
- `wc.mean(my_data, value_var)`: The weighted arithmetic average of `value_var`.
- `wc.quantile(my_data, value_var, q)`: The weighted quantile of `value_var`, where `q` is between 0 and 1.
- `wc.median(my_data, value_var)`: The weighted median of `value_var`, equivalent to `.quantile(...)` where `q=0.5`.
- `wc.std(my_data, value_var)`: The weighted standard deviation of `value_var`.
- `wc.distribution(my_data, value_var)`: The weighted proportions of `value_var`, interpreting `value_var` as categories.

The `obj` parameter above should be a `pandas` `DataFrame` or `DataFrame.groupby` object.

### Basic example

Below is a basic example of using `weightedcalcs` to find what percentage of Wyoming residents are married, divorced, et cetera:

```python
import pandas as pd
import weightcalcs

# Load the 2015 American Community Survey person-level responses for Wyoming
responses = pd.read_csv("examples/data/acs-2015-pums-wy-simple.csv")

# `PWGTP` is the weighting variable used in the ACS's person-level data
wc = weightcalcs.Calculator("PWGTP")

# Get the distribution of marriage-status responses
wc.distribution(responses, "marriage_status").round(3).sort_values(ascending=False)

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

## Other Python weighted-calculation libraries

- [`tinybike/weightedstats`](https://github.com/tinybike/weightedstats)
- [`nudomarinero/wquantiles/`](https://github.com/nudomarinero/wquantiles/)

