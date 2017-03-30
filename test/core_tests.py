import unittest
import weightedcalcs as wc
import pandas as pd
import sys
import os

calc = wc.Calculator("weights")

class WCTest(unittest.TestCase):

    def test_mean(self):
        # Example via https://en.wikipedia.org/wiki/Weighted_arithmetic_mean
        assert(calc.mean(pd.DataFrame({
            "values": [ 80, 90 ],
            "weights": [ 20, 30 ],
        }), "values") == 86)

    def test_mean_non_pandas(self):
        # Example via https://en.wikipedia.org/wiki/Weighted_arithmetic_mean
        assert(calc.mean({
            "values": [ 80, 90 ],
            "weights": [ 20, 30 ],
        }, "values") == 86)

    def test_quantile(self):
        # Example via https://en.wikipedia.org/wiki/Weighted_median
        df = pd.DataFrame({
            "values": [ 0.1, 0.35, 0.05, 0.1, 0.15, 0.05, 0.2 ],
            "weights": [ 0.1, 0.35, 0.05, 0.1, 0.15, 0.05, 0.2 ],
        })
        assert(df["values"].median() == 0.1)
        assert(calc.quantile(df, "values", 0.5) == 0.2)
        assert(calc.median(df, "values") == 0.2)

    def test_quantile_split(self):
        df = pd.DataFrame({
            "values": [ 0, 1, 2, 3 ],
            "weights": [ 1, 1, 1, 1 ],
        })
        assert(calc.quantile(df, "values", 0.5) == 1.5)

    def test_bad_quantile(self):
        with self.assertRaises(Exception) as context:
            q = calc.quantile(pd.DataFrame({
                "values": [ 0.1, 0.35, 0.05, 0.1, 0.15, 0.05, 0.2 ],
                "weights": [ 0.1, 0.35, 0.05, 0.1, 0.15, 0.05, 0.2 ],
            }), "values", -1)

    def test_std(self):
        # Example via http://www.itl.nist.gov/div898/software/dataplot/refman2/ch2/weightsd.pdf
        assert(calc.std(pd.DataFrame({
            "values": [  2, 3, 5, 7, 11, 13, 17, 19, 23 ],
            "weights": [ 1, 1, 0, 0, 4, 1, 2, 1, 0 ],
        }), "values").round(2) == 5.82)

    def test_distribution(self):
        dist = calc.distribution(pd.DataFrame({
            "values": [ "a", "b", "b", "b", "c" ],
            "weights": [ 3, 2, 0, 1, 2 ],
        }), "values")
        assert(dist["a"] == 0.375)
        assert(dist["b"] == 0.375)
        assert(dist["c"] == 0.250)

    def test_count(self):
        count = calc.count(pd.DataFrame({
            "values": [ "a", "b", "b", "b", "c" ],
            "weights": [ 3, 2, 0, 1, 2 ],
        }))
        assert(count == 8)

    def test_sum(self):
        _sum = calc.sum(pd.DataFrame({
            "values": [ 1, 2, 3, 4, 5 ],
            "weights": [ 3, 2, 0, 1, 2 ],
        }), "values")
        assert(_sum == 21)

    def test_grouped(self):
        dist = calc.distribution(pd.DataFrame({
            "group": [ "x", "x", "x", "x", "x" ],
            "values": [ "a", "b", "b", "b", "c" ],
            "weights": [ 3, 2, 0, 1, 2 ],
        }).groupby("group"), "values")
        assert(dist.loc["x"]["a"] == 0.375)
        assert(dist.loc["x"]["b"] == 0.375)
        assert(dist.loc["x"]["c"] == 0.250)

    def test_multi_grouped(self):
        dist = calc.distribution(pd.DataFrame({
            "group_a": [ "x", "x", "x", "x", "x" ],
            "group_b": [ "x", "x", "x", "x", "x" ],
            "values": [ "a", "b", "b", "b", "c" ],
            "weights": [ 3, 2, 0, 1, 2 ],
        }).groupby([ "group_a", "group_b" ]), "values")
        assert(dist.loc[("x", "x")]["a"] == 0.375)

    def test_multi_grouped_two(self):
        dist = calc.distribution(pd.DataFrame({
            "group_a": [ "x", "x", "x", "y", "y" ],
            "group_b": [ "x", "x", "x", "y", "y" ],
            "values": [ "a", "b", "b", "b", "c" ],
            "weights": [ 3, 2, 0, 1, 2 ],
        }).groupby([ "group_a", "group_b" ]), "values")
        assert(dist.loc[("x", "x")]["a"] == 0.6)
        assert(dist.loc[("x", "x")]["b"] == 0.4)
        assert(dist.loc[("x", "x")]["c"] == 0)
    
    def test_null_values(self):
        with self.assertRaises(Exception) as context:
            dist = calc.distribution(pd.DataFrame({
                "values": [ None, "b", "b", "b", "c" ],
                "weights": [ 3, 2, 0, 1, 2 ],
            }), "values")

if __name__ == '__main__':
    unittest.main()
