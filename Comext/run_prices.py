from __future__ import division

import os
from cPickle import load
from datetime import datetime

import numpy as np
import pandas as pd

from get_reference2 import get_reference
from pre_gmm_process import get_prices

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')
tb = pd.HDFStore('gmm_store.h5')

with open('declarants_no_002_dict.pkl', 'r') as declarants:
    country_code = load(declarants)
declarants.closed

declarants = sorted(country_code.keys())

prices = ['p_2008', 'p_2009', 'p_2010', 'p_2011']
shares = ['s_2008', 's_2009', 's_2010', 's_2011']
cross = ['ps_2008', 'ps_2009', 'ps_2010', 'ps_2011']
cols = shares + prices + cross
start_time = datetime.now()

# Just testing for country = '001', column = 's_2008'
# for country in declarants:
country = '001'
reference_tuple = get_reference(yearly, country)
reference = reference_tuple[1]
    # for column in tb[shares]:
column = 's_2008'
# for product in tb['c_' + country][[column]].index.levels[0]:
product = '01'

refcountry = reference[product]
year = 'y' + column[-4:] + '_'
iyear = int(year[1:5] + '52')
prev = 'y' + str(int(year[1:5]) - 1) + '_'
iprev = int(prev[1:5] + '52')

ref_price = np.log(yearly[year + 'price_' + country].ix[1, iyear, product, refcountry].values)[0] - (
            np.log(yearly[prev + 'price_' + country].ix[1, iprev, product, refcountry].values)[0])

tb['c_' + country][['p_2008']].ix['01'].apply(get_prices, axis=1, args=(country, product, refcountry, year, iyear, prev, iprev))
