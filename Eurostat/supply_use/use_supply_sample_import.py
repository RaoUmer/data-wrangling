import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Eurostat/supply_use_tables/naio_cp15_r2.tsv',
        na_values=[':', ' :', ': '], sep=',|s*\t',
        index_col=['unit', 'geo\\time', 't_cols2', 't_rows2'])
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

# Gives the table for (unit, country) pairs. Work with this.
df2 = df2.unstack(level='industry')
gr = df2.groupby(axis=0, level='geo')


def heatmap(df, cmap=plt.cm.gray_r):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    axim = ax.imshow(df.values, cmap=cmap, interpolation='nearest')
    ax.set_xlabel(df.columns.name)
    ax.set_xticks(np.arange(len(df.columns)))
    ax.set_xticklabels(list(df.columns))
    ax.set_ylabel(df.index.name)
    ax.set_yticks(np.arange(len(df.index)))
    ax.set_yticklabels(list(df.index))
    plt.colorbar(axim)

df3 = df2.ix['MIO_EUR', 'AT'].astype('float')
heatmap(df3)
