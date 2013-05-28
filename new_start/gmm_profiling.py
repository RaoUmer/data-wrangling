"""
You have a df like:
                          'p', s, c
year, partner, product ||


GMM go!
"""
from __future__ import division, print_function, unicode_literals

import pdb

import numpy as np
import pandas as pd
from scipy import optimize
from scipy import dot

# import gmail
# from outliers_after_weighting import pre
from parse_optimize_results import opt_dict_format
from gmm_with_weighting import gen_params
#-----------------------------------------------------------------------------

import itertools as it
from cPickle import load
from datetime import datetime

base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
gmm = pd.HDFStore(base + 'for_gmm.h5')
gmm_results = pd.HDFStore(base + 'gmm_results_weighted.h5')
with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
    country_code = load(declarants)
declarants = sorted(country_code.keys())
#-----------------------------------------------------------------------------
# Main loop.  Optimize to get params for each good, for each declarant.
ctry = '001'
try:
    df = gmm.select('ctry_' + ctry)
    df = df.dropna()
    df = df[~(df == np.inf)]
    by_product = df.groupby(level='good')
except KeyError, AssertionError:
    with open('gmm_logging.txt', 'a') as f:
        f.write('Failed to open or group ctry: {}'.format(ctry))
    pass

g = by_product.groups.iteritems()

l = [df.ix[x[1]] for x in it.islice(g, 100)]
test = pd.concat(l)
gr = test.groupby(level='good')
res = {name: gen_params(group, [1, 2, 1], name, country=ctry, W=True, options={'disp': True}) for name, group in gr}
res = pd.DataFrame(res).T
for_csv, for_hd5 = opt_dict_format(res, names=['const', 't1', 't2'])
