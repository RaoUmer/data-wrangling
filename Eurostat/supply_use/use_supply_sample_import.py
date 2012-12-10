from __future__ import division

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/tables')
df = pd.read_csv('clean_naio_cp15_r2.csv',
        index_col=['unit', 'geo', 'industry', 'input'])


# ,|s* is a regex to find a comma OR arbitrary white space then tab.
# I don't think na_vavlues takes regex's.

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

df.columns = [int(x.strip(' ')) for x in df.columns]
df.index.names = ['unit', 'geo', 'industry', 'input']
df2 = df[2008]

# Drop second measure.  Should be ok.  I tested a couple.
# I think identical for euro countries.  Only non-euro (UK, etc) change.
df2 = df2.ix['MIO_EUR']
# Gives the table for (unit, country) pairs. Work with this.

# Index is (Country, input), columns are industries.
df = df['2008'].unstack(level='industry')
gr = df.groupby(axis=0, level='geo')
df.ix['AT'].mean(1)  # Does it for a country.  Now use groupby.

# Control measure 1: Average value of Downstream use.


def heatmap(df, a=4, cmap=plt.cm.gray_r):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    axim = ax.imshow(df.values, cmap=cmap, interpolation='nearest')
    ax.set_xlabel(df.columns.name)
    ax.set_xticks(a * np.arange(len(df.columns) / a))
    ax.set_xticklabels(list(df.columns))
    ax.set_ylabel(df.index.name)
    ax.set_yticks(a * np.arange(len(df.index)/ a))
    ax.set_yticklabels(list(df.index))
    plt.colorbar(axim)

for country in df.index.levels[0]:
    try:
        heatmap(np.log(df.ix[country]))
    except:
        pass