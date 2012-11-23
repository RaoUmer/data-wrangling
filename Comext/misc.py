import os
from cPickle import load
import itertools as it

import pandas as pd

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

gmm_store = pd.HDFStore('gmm_store.h5')
with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)

f.closed
years = [2007, 2008, 2009, 2010, 2011]
declarants.pop('EU')

df_s = gmm_store['s_001']
df_p = gmm_store['p_001']

gr_s = df_s.groupby(axis=0, level='PRODUCT_NC')
gr_p = df_p.groupby(axis=0, level='PRODUCT_NC')


# Grouby & Iteration.
# Works for small set?

for group in gr_p:
    df_s = df_s.join(group[1], how='outer')

for name, group in gr_p:
    if name == '01':
        pass
    else:
        pd.concat([df_s, group], axis=1, join='outer')

for name, group in gr_p:
    if name == '01':
        pass
    else:
        df_s.update(group)

## Method 2; Too much memory.

for i, (product, group) in enumerate(gr_s):
    if i == 0:  # Initialization
        df3 = pd.merge(df_s.ix[product], df_p.ix[product],
        how='outer', left_index=True, right_index=True)
    else:
        df3 = pd.concat([df3, pd.merge(df_s.ix[product], df_p.ix[product],
            left_index=True, right_index=True)])


df3 = pd.merge(df_s.ix['01'], df_p.ix['01'], how='outer',
    left_index=True, right_index=True)

df3 = pd.concat([df3, pd.merge(df_s.ix['01011010'], df_p.ix['01011010'],
    how='outer', left_index=True, right_index=True)])

# Zip first. Check for same product, then merge.


# With itertools
# This iterator yields ((product, df_s), (product, df_p)) tuples.

iz = it.izip(gr_s, gr_p)
df = pd.DataFrame()
for i in iz:
    df = pd.concat([df, pd.merge(i[0][1], i[1][1], how='outer', left_index=True, right_index=True)])

df.index = pd.MultiIndex.from_tuples(df.index, names=['product', 'partner'])

