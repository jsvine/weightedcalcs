import unittest
import weightedcalcs
import pandas as pd
import sys, os

C = weightedcalcs.Calculator
c_default = C("weights")

class WCTest(unittest.TestCase):

    def test_mean(self):
        # Example via https://en.wikipedia.org/wiki/Weighted_arithmetic_mean
        assert(c_default.mean(pd.DataFrame({
            "values": [ 80, 90 ],
            "weights": [ 20, 30 ],
        }), "values") == 86)

    def test_quantile(self):
        # Example via https://en.wikipedia.org/wiki/Weighted_median
        df = pd.DataFrame({
            "values": [ 0.1, 0.35, 0.05, 0.1, 0.15, 0.05, 0.2 ],
            "weights": [ 0.1, 0.35, 0.05, 0.1, 0.15, 0.05, 0.2 ],
        })
        assert(df["values"].median() == 0.1)
        assert(c_default.quantile(df, "values", 0.5) == 0.2)
        assert(c_default.median(df, "values") == 0.2)

    def test_std(self):
        # Example via http://www.itl.nist.gov/div898/software/dataplot/refman2/ch2/weightsd.pdf
        assert(c_default.std(pd.DataFrame({
            "values": [  2, 3, 5, 7, 11, 13, 17, 19, 23 ],
            "weights": [ 1, 1, 0, 0, 4, 1, 2, 1, 0 ],
        }), "values").round(2) == 5.82)

    def test_distribution(self):
        dist = c_default.distribution(pd.DataFrame({
            "values": [ "a", "b", "b", "b", "c" ],
            "weights": [ 3, 2, 0, 1, 2 ],
        }), "values")
        assert(dist["a"] == 0.375)
        assert(dist["b"] == 0.375)
        assert(dist["c"] == 0.250)

if __name__ == '__main__':
    unittest.main()
