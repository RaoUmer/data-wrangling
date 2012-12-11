from __future__ import division

import os

import numpy as np
import pandas as pd

# Supply Table
os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/tables')

df = pd.read_csv('clean_naio_cp15_r2.csv',
        index_col=['unit', 'geo', 'input', 'industry'])

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

# Breaks things. Mutable data ftl.
# for group, df in gr:
#     df.ix[group].apply(lambda x: np.count_nonzero(x.dropna()))

# Control measure 3: Herfindahl index
