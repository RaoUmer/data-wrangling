from __future__ import division

import os

import numpy as np
import pandas as pd

os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/tables')

files = ['clean_naio_cp15_r2.csv',
        'clean_naio_cp16_r2.csv',
        'clean_naio_cp17_r2.csv',
        'clean_naio_cp17i_r2.csv']

df = pd.read_csv(files[0],
        index_col=['unit', 'geo', 'industry', 'input'])

# Drop second measure.  Should be ok.  I tested a couple.
# I think identical for euro countries.  Only non-euro (UK, etc) change.
df = df.ix['MIO_NAC']
# Gives the table for (unit, country) pairs. Work with this.

# Index is (Country, input), columns are industries.
df = df['2008'].unstack(level='industry')
gr = df.groupby(axis=0, level='geo')

# Control measure 1: Average value of Downstream use.
df.mean(axis=1)

# Control measure 2: Count value of Downstream use.
df.ix['AT'].apply(lambda x: np.count_nonzero(x.dropna()))

# Has to be a better way.
for group, df in gr:
    df.ix[group].apply(lambda x: np.count_nonzero(x.dropna()))

# Control measure 3: Herfindahl index
