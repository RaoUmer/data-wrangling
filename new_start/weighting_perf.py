from __future__ import division, print_function, unicode_literals

from cPickle import load

import pandas as pd

from gmm_with_weighting import gen_params

base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
gmm = pd.HDFStore(base + 'gmm_store.h5')
gmm_results = pd.HDFStore(base + 'gmm_results.h5')
with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
    country_code = load(declarants)

ctry = '002'
df = gmm.select('by_ctry_' + ctry)

sub = df[:1000]
sub_pp = sub.dropna().groupby(level=['PRODUCT_NC', 'PARTNER'])

# Python version
res = {name: gen_params(group, x0=[2, 1]) for name, group
       in by_product_partner}

# %timeit res = {name: gen_params(group, x0=[2, 1]) for name, group in sub_pp}
# 1 loops, best of 3: 36.9 s per loop
