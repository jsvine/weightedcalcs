import pandas as pd

def groupby_deco(func):
    def func_wrapper(self, thing, *args, **kwargs):
        if isinstance(thing, pd.core.groupby.DataFrameGroupBy):
            agg = thing.apply(lambda x: func(self, x, *args, **kwargs))
            is_series = isinstance(agg, pd.core.series.Series)
            has_multiindex = isinstance(agg.index, pd.indexes.multi.MultiIndex)
            if is_series and has_multiindex:
                return agg.unstack()
            else:
                return agg
        return func(self, thing, *args, **kwargs)
    return func_wrapper

def fillna_deco(val):
    def deco(func):
        def func_wrapper(self, thing, *args, **kwargs):
            return func(self, thing, *args, **kwargs).fillna(val)
        return func_wrapper
    return deco

def check_nulls(series):
    if series.isnull().sum() > 0:
        raise ValueError("value_var contains null values")
    return series

class Calculator(object):
    def __init__(self, weight_var):
        self.weight_var = weight_var

    @groupby_deco
    def count(self, thing):
        return thing[self.weight_var].sum()

    @groupby_deco
    def sum(self, thing, value_var):
        weights = thing[self.weight_var]
        values = check_nulls(thing[value_var])
        return (values * weights).sum()
    
    @groupby_deco
    def mean(self, thing, value_var):
        weights = thing[self.weight_var]
        total_weight = weights.sum()
        values = check_nulls(thing[value_var])
        return (values * weights).sum() / total_weight
    
    @groupby_deco
    def std(self, thing, value_var):
        weights = thing[self.weight_var]
        n_nonzero_weights = (weights > 0).sum()
        if (n_nonzero_weights) < 2: return pd.np.nan
        values = check_nulls(thing[value_var])
        mean = self.mean(thing, value_var)
        numerator = (weights * (values - mean).pow(2)).sum()
        denominator = (n_nonzero_weights - 1) * weights.sum() / n_nonzero_weights
        return pow(numerator / denominator, 0.5)

    @groupby_deco
    def quantile(self, thing, value_var, q):
        if q < 0 or q > 1:
            raise ValueError("q must be between 0 and 1")
        df = pd.DataFrame({
            "weights": thing[self.weight_var],
            "values": check_nulls(thing[value_var])
        }).sort_values("values")
        df["cumul_prop"] = df["weights"].cumsum() / df["weights"].sum()
        shaved = df[df["cumul_prop"] >= q]
        if shaved.iloc[0]["cumul_prop"] == q:
            return shaved.head(2)["values"].mean()
        else:
            return shaved.iloc[0]["values"]

    @groupby_deco
    def median(self, thing, value_var):
        return self.quantile(thing, value_var, 0.5)

    @fillna_deco(0)
    @groupby_deco
    def distribution(self, thing, value_var):
        weights = thing[self.weight_var]
        total_weight = weights.sum()
        check_nulls(thing[value_var])
        return thing.groupby(value_var)[self.weight_var].sum() / total_weight 
    
