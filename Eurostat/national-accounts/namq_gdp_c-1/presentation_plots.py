import pandas as pd

df = pd.read_csv('/Users/tom/TradeData/data-wrangling/Eurostat/national-accounts/namq_gdp_c-1/na_accts_clean.csv',
    index_col=['geo', 'quarter'], parse_dates=[0])
gr = df.groupby(axis=0, level='geo')

# Summary Plots for change in gdp & imports for a subset.
subset = ['Germany', 'France', 'Greece', 'Italy', 'Spain', 'United Kingdom']
df['gdp'].ix[subset].unstack(level=0).pct_change(4).plot(grid=True, xlim=('2007-03-01', '2012-06-01'))

for country in subset:
    df[['gdp', 'imports']].ix[country].pct_change(4).plot(
        title='Percent Change for %s' % country, grid=True, xlim=('2007-03-01', '2012-06-01'))


def max_drop(x):
    return (x.index[x.pct_change(4).dropna().argmin()], x.pct_change(4).dropna().min())

df['gdp'].unstack(0).apply(max_drop)
df['imports'].unstack(0).apply(max_drop)
df['exports'].unstack(0).apply(max_drop)

gr_g = df['gdp'].groupby(axis=0, level='geo')

# Get frequencies for quarter of maximum decline.
# Usefull but needs to be cleaned.

x = df['gdp'].unstack(0).apply(max_drop)
x = pd.DataFrame(x, columns=['tups'])
l1 = []
for t in x['tups']:
    l1.append(str(t[0].year) + 'Q' + str(t[0].quarter))

x['max_drop'] = l1
x['max_drop'].value_counts().plot(kind='bar', rot=45)

##### Heatmap for Supply Use ##########
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Eurostat/supply_use_tables/naio_cp15_r2.tsv',
        na_values=[':', ' :', ': '], sep=',|s*\t',
        index_col=['unit', 'geo\\time', 't_cols2', 't_rows2'])

df.columns = [int(x.strip(' ')) for x in df.columns]
df.index.names = ['unit', 'geo', 'industry', 'input']
df2 = df[2008]
df2 = df2.unstack(level='industry')


def heatmap(df, cmap=plt.cm.gray_r):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    axim = ax.imshow(df.values, cmap=cmap, interpolation='nearest')
    ax.set_xlabel(df.columns.name)
    ax.set_xticks(3 * np.arange(len(df.columns) / 3))
    ax.set_xticklabels(list(df.columns))
    ax.set_ylabel(df.index.name)
    ax.set_yticks(3 * np.arange(len(df.index) / 3))
    ax.set_yticklabels(list(df.index))
    plt.colorbar(axim)

df3 = df2.ix['MIO_EUR', 'AT'].astype('float')
heatmap(df3)
