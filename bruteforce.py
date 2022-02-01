#!/usr/bin/env python3

import sys
import pandas as pd


if len(sys.argv) < 2:
    print("You must specify a dataframe file  as argument.")
elif len(sys.argv) != 2:
    print("There are too many arguments specified.")
else:
    try:
        df_stocks = pd.read_csv(sys.argv[1], header=0)
        print(df_stocks)
    except FileNotFoundError:
        print(f"No such file or directory: '{sys.argv[1]}'")
