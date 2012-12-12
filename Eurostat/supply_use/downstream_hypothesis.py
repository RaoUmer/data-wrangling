from __future__ import division

import os

import numpy as np
import pandas as pd

# Supply Table
os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/docs')
with open('clean_use_row_labels.pkl', 'r') as f:
    d_row = load(f)

with open('clean_use_col_labels.pkl', 'r') as f:
    d_col = load(f)

# Remove will differ.
# remove = {
#         'P3': 'Final consumption expenditure',
#         'P3_S13': 'Final consumption expenditure by government',
#         'P3_S14': 'Final consumption expenditure by households',
#         'P3_S15': 'Final consumption expenditure by non-profit organisations serving households (NPISH)',
#         'P5': 'Gross capital formation',
#         'P51': 'Gross fixed capital formation',
#         'P52': 'Changes in inventories',
#         'P52_P53': 'Changes in inventories and valuables',
#         'P53': 'Changes in valuables',
#         'P6': 'Exports',
#         'P6_S21': 'Exports intra EU fob',
#         'P6_S2111': 'Exports of goods and services EMU members (fob)',
#         'P6_S2112': 'Exports of goods and services to EMU non-members (fob)',
#         'P6_S22': 'Exports extra EU fob',
#         'TFINU': "Final use at purchasers'prices",
#         'TOTAL': 'Total',
#         'TU': "Total use at purchasers' prices"
# }

os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/tables')

df = pd.read_csv('clean_naio_cp15_r2.csv',
        index_col=['unit', 'geo', 'cols', 'rows'])

# Drop second measure.  Should be ok.  I tested a couple.
# I think identical for euro countries.  Only non-euro (UK, etc) change.
df = df.ix['MIO_NAC']
# Gives the table for (unit, country) pairs. Work with this.

# Index is (Country, input), columns are industries.
df = df['2008'].unstack(level='cols')
gr = df.groupby(axis=0, level='geo')

# Control measure 1: Average value of Downstream use.
df.mean(axis=1)

# Control measure 2: Count value of Downstream use.
df.ix['AT'].apply(lambda x: np.count_nonzero(x.dropna()))

# Breaks things. Mutable data ftl.
# for group, df in gr:
#     df.ix[group].apply(lambda x: np.count_nonzero(x.dropna()))

# Control measure 3: Herfindahl index
