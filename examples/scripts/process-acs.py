#!/usr/bin/env
import sys, os
import pandas as pd

responses = pd.read_csv(sys.stdin).rename(columns={
    "AGEP": "age",
    "WAGP": "income"
})

responses["marriage_status"] = responses["MAR"].apply({
    1: "Married",
    2: "Widowed",
    3: "Divorced",
    4: "Separated",
    5: "Never married or under 15 years old"
}.get)

responses["gender"] = responses["SEX"].apply({
    1: "Male",
    2: "Female"
}.get)

responses[[
    "SERIALNO",
    "PWGTP",
    "age",
    "gender",
    "marriage_status",
    "income"
]].to_csv(sys.stdout, index=False)
