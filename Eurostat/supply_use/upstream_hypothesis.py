from __future__ import division

import os

import numpy as np
import pandas as pd

os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/tables')

df = pd.read_csv('clean_naio_cp16_r2.csv',
        index_col=['unit', 'geo', 'industry', 'input'])

df = df.ix['MIO_NAC']

# Index is (Country, input), columns are industries.
df = df['2008'].unstack(level='industry')
gr = df.groupby(axis=0, level='geo')

# Control measure 1: Average value of Downstream use.
df.mean(axis=1)

# Control measure 2: Count value of Downstream use.
df.ix['AT'].apply(lambda x: np.count_nonzero(x.dropna()))
