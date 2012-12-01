import os
from cPickle import load
from datetime import datetime

import numpy as np
import pandas as pd
from get_reference2 import get_reference

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')


def get_prices(country, year, square=2, name='p_', store=yearly):
    """
    Use to fill prices for gmm calc.

    Parameters
    --------
    country : string.  Probably from an outer loop.
    year : int.
    square : whether to square the result or not. Defaults to true (i.e. 2).
    name : string. For the returned column name.
    store : HDFStore.
    Returns
    -------
    A dataframe w/ col name name_YYYY
    """

    year1 = 'y' + str(year) + '_'
    year0 = 'y' + str(year - 1) + '_'

    df1 = yearly[year1 + 'price_' + country]
    df0 = yearly[year0 + 'price_' + country]

    df1.name = 'p' + str(year)
    df0.name = 'p' + str(year - 1)

    gr1 = df1.groupby(axis=0, level='PRODUCT_NC')
    gr0 = df0.groupby(axis=0, level='PRODUCT_NC')

    l1 = []
    drops1 = []
    for product in gr1.groups.keys():
        try:
            l1.append((product, ref_dict[product]))
        except KeyError:
            drops1.append(product)

    l0 = []
    drops0 = []
    for product in gr0.groups.keys():
        try:
            l0.append((product, ref_dict[product]))
        except KeyError:
            drops0.append(product)

    return pd.DataFrame((np.log(df1) - np.log(df0) - (
            np.log(df1.ix[l1].reset_index(level='PARTNER')['p' + str(year)].reindex(df1.index, level='PRODUCT_NC')) - (
            np.log(df0.ix[l0].reset_index(level='PARTNER')['p' + str(year - 1)].reindex(df0.index, level='PRODUCT_NC'))))), columns=[name + str(year)]) ** square


start_time = datetime.now()
os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

# Globals

yearly = pd.HDFStore('yearly.h5')
gmm_store = pd.HDFStore('gmm_store.h5')
with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)

with open('references_dict.pkl', 'r') as f:
    ref_dict_all = load(f)

years = [2007, 2008, 2009, 2010, 2011]

for country in sorted(declarants):
    ref_dict = ref_dict_all[country]
    for year in years[1:]:
        print 'Working on %r, %r.' % (country, year)
        print datetime.now() - start_time
        if year == 2008:
            gmm_store['p_' + country] = get_prices(country, year)
        else:
            gmm_store['p_' + country] = gmm_store['p_' + country].merge(
                get_prices(country, year),
                how='outer', left_index=True, right_index=True)

##############################################################################
#TESTING

# os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
# yearly = pd.HDFStore('yearly.h5')
# country = '001'

# df07 = yearly['y2007_price_001'].head(500)
# df08 = yearly['y2008_price_001'].head(500)

# df07.name = 'p2007'
# df08.name = 'p2008'

# gr07 = df07.groupby(axis=0, level='PRODUCT_NC')
# gr08 = df08.groupby(axis=0, level='PRODUCT_NC')

# with open('references_dict.pkl', 'r') as f:
#     ref_dict = load(f)

# l1 = gr08.groups.keys()
# l2 = []
# drops08 = []
# for product in l1:
#     try:
#         l2.append((product, ref_dict['001'][product]))
#     except KeyError:
#         drops08.append(product)

# l3 = gr07.groups.keys()
# l4 = []
# drops07 = []
# for product in l3:
#     try:
#         l4.append((product, ref_dict['001'][product]))
#     except KeyError:
#         drops07.append(product)

# ydiff = np.log(df08) - np.log(df07)

# kdiff = np.log(df08.ix[l2].reset_index(level='PARTNER')['p2008'].reindex(df08.index, level='PRODUCT_NC')) - (
#         np.log(df07.ix[l4].reset_index(level='PARTNER')['p2007'].reindex(df07.index, level='PRODUCT_NC')))

# x = ydiff - kdiff
