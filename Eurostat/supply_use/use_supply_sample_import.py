from __future__ import division

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/tables')

files = ['clean_naio_cp15_r2.csv',
        'clean_naio_cp16_r2.csv',
        'clean_naio_cp17_r2.csv',
        'clean_naio_cp17i_r2.csv']

df = pd.read_csv(files[0],
        index_col=['unit', 'geo', 'industry', 'input'])

"""
Want to reproduce the table:
            Industries
           _______________________________________
 commodity|                  |      | Total
          |                  |      | Commodity
          |                  | Final| Output
          |                  | Uses |
          |                  |      |
          ----------------------------------------
          |    Value Added   | GDP  |
          ----------------------------------------
          | Total Ind Output |      | Total Output

But to deal with years we'll throw it out the outside axis
so a .ix[2008] will give that table.

Really only going to use 2008.  Lot's of nans elsewhere.

Note on indicies: "the first four digits are the classification of the
producing enterprise given by the Statistical Classification of Economic
Activities in the European Community (NACE) and the first six correspond
to the CPA.
"""