# Swaps on the join.

from __future__ import division

import gc
import os
from cPickle import load

import numpy as np
import pandas as pd


"""
The plan for this one is to avoid concatination/merges as much as possible.
We'll use a similar strategy as smart_*, but build in if/else handling.
Some upfront cost since I'll need to compute and hold in memory the reference
values for BOTH shares and price, but it may be worth it later.
"""

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')
gmm_store = pd.HDFStore('gmm_store.h5')
with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)

f.close()
with open('references_dict.pkl', 'r') as f:
    d = load(f)

f.close()
years = [2007, 2008, 2009, 2010, 2011]


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
    iyear1 = int(str(year) + '52')
    iyear0 = int(str(year - 1) + '52')

    df1 = yearly[year1 + 'price_' + country][0].ix[1]  # Need [0] to get Series
    df0 = yearly[year0 + 'price_' + country][0].ix[1]

    df1.name = 'p' + str(year)
    df0.name = 'p' + str(year - 1)

    l1 = []
    drops1 = []
    for product in df1.groupby(axis=0, level='PRODUCT_NC').groups.keys():
        try:
            l1.append((iyear1, product, ref_dict[product]))
        except KeyError:
            drops1.append(product)

    l0 = []
    drops0 = []
    for product in df0.groupby(axis=0, level='PRODUCT_NC').groups.keys():
        try:
            l0.append((iyear0, product, ref_dict[product]))
        except KeyError:
            drops0.append(product)

    return pd.DataFrame((np.log(df1.ix[iyear1]) - np.log(df0.ix[iyear0]) - (
            np.log(df1.ix[l1].ix[iyear1].reset_index(level='PARTNER')['p' + str(year)].reindex(df1.index, level='PRODUCT_NC').ix[iyear1]) - (
            np.log(df0.ix[l0].ix[iyear0].reset_index(level='PARTNER')['p' + str(year - 1)].reindex(df0.index, level='PRODUCT_NC').ix[iyear0])))), columns=[name + str(year)]) ** square


def get_shares(country, year, square=2, name='s_', store=yearly):
    """
    Use to fill in the table for gmm calculation.

    Parameters
    ----------
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
    iyear1 = int(str(year) + '52')
    iyear0 = int(str(year - 1) + '52')

    df1 = yearly[year1 + country]['VALUE_1000ECU'].ix[1]
    df0 = yearly[year0 + country]['VALUE_1000ECU'].ix[1]

    l1 = []
    drop1 = []
    for product in df1.groupby(axis=0, level='PRODUCT_NC').groups.keys():
        try:
            l1.append((iyear1, product, ref_dict[product]))
        except KeyError:
            drop1.append(product)

    l0 = []
    drop0 = []
    for product in df0.groupby(axis=0, level='PRODUCT_NC').groups.keys():
        try:
            l0.append((iyear0, product, ref_dict[product]))
        except KeyError:
            drop0.append(product)

    return pd.DataFrame(
        np.log(df1 / df1.groupby(axis=0, level='PRODUCT_NC').sum().reindex(df1.index, level='PRODUCT_NC')).ix[iyear1] - (
        np.log(df0 / df0.groupby(axis=0, level='PRODUCT_NC').sum().reindex(df0.index, level='PRODUCT_NC')).ix[iyear0]) - (
        np.log(df1.ix[l1].ix[iyear1].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df1.index, level='PRODUCT_NC').ix[iyear1] / df1.groupby(axis=0, level='PRODUCT_NC').sum().reindex(df1.index, level='PRODUCT_NC').ix[iyear1]) - (
        np.log(df0.ix[l0].ix[iyear0].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df0.index, level='PRODUCT_NC').ix[iyear0] / df0.groupby(axis=0, level='PRODUCT_NC').sum().reindex(df0.index, level='PRODUCT_NC').ix[iyear0])
        )
        ), columns=[name + str(year)]
        ) ** square


gc.collect()
for country in sorted(declarants):
    ref_dict = d[country]
    for year in years[1:]:
        if year == 2008:
            print('Starting %s, %s') % (country, year)
            df1 = get_prices(country, year)
            gc.collect()
            print('Starting shares for %s, %s') % (country, year)
            df2 = get_shares(country, year)
            gc.collect()
            print('Starting join for %s, %s') % (country, year)
            df3 = df2.join(df1, how='outer')
            df3.dropna()
            del df1, df2
            gc.collect()
        else:
            print('Starting %s, %s') % (country, year)
            df1 = get_prices(country, year)
            gc.collect()
            print('Starting shares for %s, %s') % (country, year)
            df2 = get_shares(country, year)
            gc.collect()
            print('Starting join for %s, %s') % (country, year)
            df3 = df3.join(df2.join(df1), how='outer')
            df3.dropna(how='all')
            del df1, df2
            gc.collect()
    print('Done with %s') % country
