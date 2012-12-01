from __future__ import division

import os
from cPickle import load
from datetime import datetime as dt

import pandas as pd

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
gmm = pd.HDFStore('gmm_store.h5')

with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)

declarants.pop('EU')
start_time = dt.now()
cols = {'c_20082008': 'c_2008',
        'c_20092009': 'c_2009',
        'c_20102010': 'c_2010',
        'c_20112011': 'c_2011'}


for country in sorted(declarants):
    try:
        gmm['f_' + country] = ((gmm['s_' + country].join(gmm['p_' + country], how='outer')).join(gmm['c_' + country], how='outer')).rename(columns=cols)
        print(dt.now() - start_time)
        print('done with %s' % country)
    except:
        print('Problem with %s' % country)
