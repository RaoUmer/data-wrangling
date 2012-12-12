from __future__ import division

import os
from cPickle import load

import numpy as np
import pandas as pd

# USE Table
os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/docs')
with open('clean_use_row_labels.pkl', 'r') as f:
    d_row = load(f)

with open('clean_use_col_labels.pkl', 'r') as f:
    d_col = load(f)


remove = {
        'P3': 'Final consumption expenditure',
        'P3_S13': 'Final consumption expenditure by government',
        'P3_S14': 'Final consumption expenditure by households',
        'P3_S15': 'Final consumption expenditure by non-profit organisations serving households (NPISH)',
        'P5': 'Gross capital formation',
        'P51': 'Gross fixed capital formation',
        'P52': 'Changes in inventories',
        'P52_P53': 'Changes in inventories and valuables',
        'P53': 'Changes in valuables',
        'P6': 'Exports',
        'P6_S21': 'Exports intra EU fob',
        'P6_S2111': 'Exports of goods and services EMU members (fob)',
        'P6_S2112': 'Exports of goods and services to EMU non-members (fob)',
        'P6_S22': 'Exports extra EU fob',
        'TFINU': "Final use at purchasers'prices",
        'TOTAL': 'Total',
        'TU': "Total use at purchasers' prices"
}

os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/tables')

df = pd.read_csv('clean_naio_cp16_r2.csv',
        index_col=['unit', 'geo', 'cols', 'rows'])

df = df.ix['MIO_NAC']

# Index is (Country, input), columns are industries.
df = df['2008'].unstack(level='cols')

# Control measure 1: Average value of Downstream use.
res1 = df.mean(axis=1)

# Control measure 2: Count value of Downstream use.


def mycount(x):
    return np.count_nonzero(x.dropna())

res2 = df.T.apply(mycount)


################### TESTING #####################
## Groupby mechanics:


df2 = df[['A01', 'A02', 'R93', 'S94', 'I']]
gr2 = df2.groupby(axis=0, level='geo', group_keys=False)
test = df2.ix['AT']

# measure 2:
trans = test.T.dropna(how='all')  # Only summing over columns seems to work.
trans.apply(mycount)


## Label Check:  Shows that I should switch my col labels from original (done).
hit = []
miss = []
fails = []

for k in df.columns:
    try:
        hit.append(d_row[k])
    except KeyError:
        try:
            miss.append(d_col[k])  # Should get most/all
        except KeyError:
            fails.append(k)

hit2 = []
miss2 = []
fails2 = []

for k in df.ix['AT'].index:
    try:
        hit2.append(d_row[k])  # Should get most/all
    except KeyError:
        try:
            miss2.append(d_col[k])
        except KeyError:
            fails2.append(k)
