from __future__ import division

import os
from cPickle import load

import numpy as np
import pandas as pd

# USE Table
os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/docs')
with open('clean_use_row_labels.pkl', 'r') as f:
    d_col = load(f)

with open('clean_use_col_labels.pkl', 'r') as f:
    d_row = load(f)

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


## Label Check
hit = []
miss = []
fails = []

for k in df.columns:
    try:
        hit.append(d_row[k])
    except KeyError:
        try:
            miss.append(d_col[k])
        except KeyError:
            fails.append(k)
hit2 = []
miss2 = []
fails2 = []

tf = df.ix['AT']
for k in tf.index:
    try:
        hit.append(d_row[k])
    except KeyError:
        try:
            miss.append(d_col[k])
        except KeyError:
            fails.append(k)
