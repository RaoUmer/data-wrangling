import datetime as dt

import pandas as pd

"""
Everything here is in NSA, millions of euros, nominal.
"""


def time_parse(x):
    """convert '2012Q3' -> good format
    """
    q_to_m = {'1': 3,
            '2': 6,
            '3': 9,
            '4': 12}
    l = x.split('Q')
    return dt.datetime(int(l[0]), q_to_m[l[1]], 1)


df = pd.read_csv('gdp.csv', na_values=":", parse_dates=[0], index_col=[0, 1],
    date_parser=time_parse, thousands=",")

del df['S_ADJ'], df['UNIT'], df['INDIC_NA']
df = df.rename(columns={'Value': 'gdp'})

df2 = pd.read_csv('imports.csv', na_values=":", parse_dates=[0],
 index_col=[0, 1], date_parser=time_parse, thousands=",")

df3 = pd.read_csv('exports.csv', na_values=":", parse_dates=[0],
    index_col=[0, 1], date_parser=time_parse, thousands=",")

del df2['S_ADJ'], df2['UNIT'], df2['INDIC_NA'], df3['S_ADJ'],
del df3['UNIT'], df3['INDIC_NA']

df2 = df2.rename(columns={'Value': 'imports'})
df3 = df3.rename(columns={'Value': 'exports'})

df = df.join(df2, how='outer').join(df3, how='outer')


def rename_part(x):
    d = {'European Union (27 countries)': 'EU27',
        'Germany (including  former GDR from 1991)': 'Germany',
        }
    try:
        return (x[0], d[x[1]])
    except KeyError:
        return x

l = []
for x in df.index:
    l.append(rename_part(x))

df.index = pd.MultiIndex.from_tuples(l)
df.index.names = ['quarter', 'geo']
df = df.sortlevel(1)

df.to_csv('na_accts_clean.csv')
