import os
import datetime as dt

import numpy as np
import pandas as pd

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Eurostat/ind_prod_store/')
df = pd.read_csv('sts_inpr_q.tsv',
    sep=",|s*\t", na_values=[':', ' :', ': '],
    index_col=['indic_bt', 'nace_r2', 's_adj', 'geo\\time'])

df.columns = [(x.strip(' ')) for x in df.columns]

# Moves the quarters to the index and nace_r2 to the columns.
df2 = df.stack().unstack('nace_r2')
df2.index.names = df2.index.names[:2] + ['geo', 'quarter']

df2 = df2.xs(('PROD', 'GROSS'), level=('indic_bt', 's_adj'))


def time_parse(x):
    """convert '2012Q3' -> good format
    """
    q_to_m = {'1': 3,
            '2': 6,
            '3': 9,
            '4': 12}
    l = x.split('Q')
    return dt.datetime(int(l[0]), q_to_m[l[1]], 1)

# i is country, x: quarter;  Compose set comp . parse() . strip()
l = pd.DatetimeIndex([time_parse(x.rstrip()) for i, x in df2.index])

l2 = [x[0] for x in df2.index]
tup = zip(l2, l)
df2.index = pd.MultiIndex.from_tuples(tup, names=['geo', 'time'])
df2 = df2.sortlevel(0)

# WARNING: Stripping data of some provisional warnings. Mainly Q3 2012.


def strip_float(x):
    """Use with applymap to convert Maybe annotated floats (strings) to floats.
    """
    if type(x) == float:
        return x
    else:
        try:
            return float(x.split(' ')[0])
        except ValueError:
            return np.nan

df2 = df2.applymap(strip_float)
gr = df2.groupby(axis=0, level='geo')
pc = gr.pct_change(4).dropna(how='all')

pc.to_csv('ind_prod_clean.csv')


""" Lazy version using itertools (it). Can't get it to work.
f = operator.itemgetter(0)
z = it.islice(df2.index, len(df2.index))
tup = it.izip(f(z), l)
"""

""" Alternative index: Not working though
df3 = df2
lp = pd.PeriodIndex([time_parse(x.rstrip()) for i, x in df2.index], freq='Q')
tup2 = zip(l2, lp)
df3.index = pd.MultiIndex.from_tuples(tup2, names=['geo', 'time'])
df3 = df3.sortlevel(1)
"""
