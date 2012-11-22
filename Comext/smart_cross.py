import os
from cPickle import load
from datetime import datetime

import pandas as pd
from smart_shares import get_shares
from smart_prices import get_prices
from get_reference2 import get_reference


start_time = datetime.now()
os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

yearly = pd.HDFStore('yearly.h5')
gmm_store = pd.HDFStore('gmm_store.h5')

with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)
f.closed

years = [2007, 2008, 2009, 2010, 2011]

for country in sorted(declarants):
    ref_dict = get_reference(yearly, country)
    for year in years[1:]:
        print 'Working on %r, %r.' % (country, year)
        print start_time - datetime.now()
        gmm_store['s_' + country] = gmm_store['s_' + country].merge(
            get_shares(country, year, square=1, name=('c_' + year)) *
            get_prices(country, year, square=1, name=('c_' + year)),
            how='outer', left_index=True, right_index=True)
