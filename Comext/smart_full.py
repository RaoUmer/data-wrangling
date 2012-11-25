import os
from cPickle import load
from datetime import datetime

import pandas as pd

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
start_time = datetime.now()

gmm_store = pd.HDFStore('gmm_store.h5')
with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)

f.closed
years = [2007, 2008, 2009, 2010, 2011]
declarants.pop('EU')

for country in sorted(declarants):
    print('Working on %s') % country
    print datetime.now() - start_time
    gmm_store['country_001'] = gmm_store['s_' + country].join(
        gmm_store['p_' + country], how='outer').join(
        gmm_store['c_' + country], how='outer')
