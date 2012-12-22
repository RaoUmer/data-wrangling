from __future__ import division

import pandas as pd
import matplotlib.pyplot as plt
import GrandRegression

df = pd.read_csv('/Users/tom/TradeData/data-wrangling/Eurostat/national-accounts/namq_gdp_c-1/na_accts_clean.csv',
    index_col=['geo', 'quarter'], parse_dates=[0])


def max_drop(x):
    return (x.index[x.pct_change(4).dropna().argmin()],
        x.pct_change(4).dropna().min())


def use_max_drop(col):
    x = df[col].unstack(0).apply(max_drop)
    x = pd.DataFrame(x, columns=['tups'])
    l1 = []
    for t in x['tups']:
        l1.append(str(t[0].year) + 'Q' + str(t[0].quarter))
    x['max_drop'] = l1

    return x

x = use_max_drop('gdp')
fig_gdp = x['max_drop'].value_counts().plot(
    kind='bar', rot=45, color='k', alpha=.7)
plt.ylim(0.0, 15.)
plt.title(u'Quarter of Largest Drop in GDP')
plt.xlabel('Quarter')
plt.ylabel('Number of Countries')

plt.figure()
x = use_max_drop('imports')
fig_imp = x['max_drop'].value_counts().plot(
    kind='bar', rot=45, color='k', alpha=.7)
plt.ylim(0.0, 28.)
plt.title(u'Quarter of Largest Drop in Imports')
plt.xlabel('Quarter')
plt.ylabel('Number of Countries')

plt.figure()
x = use_max_drop('exports')
fig_exp = x['max_drop'].value_counts().plot(
    kind='bar', rot=45, color='k', alpha=.7)
plt.ylim(0.0, 23.)
plt.title(u'Quarter of Largest Drop in Exports')
plt.xlabel('Quarter')
plt.ylabel('Number of Countries')

# How about together? Run max drop for each on join.

#
gr = df.groupby(axis=0, level='geo')
fig = plt.figure()
p = 0
for ctry in df.index.levels[0]:
    if ctry == 'EU27':
        pass
    else:
        p += 1
        ax = fig.add_subplot(6, 5, p)
        gr.pct_change().ix[ctry].plot()

r = grandRegression('004', [2008, 6])x = r.endog
y = r.endog

x = r.exog['size']

plt.scatter(x, y)

plt.xlabel('Product Size')

plt.ylabel('Percent Change')
plt.grid()

