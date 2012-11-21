import os
from cPickle import load
from datetime import datetime

import pandas as pd
from smart_shares import get_shares
from smart_prices import get_prices

start_time = datetime.now()
os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

yearly = pd.HDFStore('yearly.h5')
gmm_store = pd.HDFStore('gmm_store.h5')

with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)
f.closed

years = [2007, 2008, 2009, 2010, 2011]

for country in declarants:
    for year in years[1:]:
        print 'Working on %r, %r.' % (country, year)
        print start_time - datetime.now()
        gmm_store['c' + str(year) + country] = (
            get_shares(country, year, square=1) * (
            get_prices(country, year, square=1)))
