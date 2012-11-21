import os
from cPickle import load

import numpy as np
import pandas as pd
from get_reference2 import get_reference

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

# Globals

yearly = pd.HDFStore('yearly.h5')
gmm_store = pd.HDFStore('gmm_store.h5')

with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)
f.closed

years = [2007, 2008, 2009, 2010, 2011]


def get_shares(country, year, square=2, store=yearly):
    """
    Use to fill in the table for gmm calculation.

    Parameters
    ----------
    country : string. From the list of declarants
    year : int e.g. 2008

    Returns:
    --------
    Right now just a series.
    """

    ref_dict = get_reference(yearly, country)

    year1 = 'y' + str(year) + '_'
    year0 = 'y' + str(year - 1) + '_'
    iyear1 = int(str(year) + '52')
    iyear0 = int(str(year - 1) + '52')

    df1 = yearly[year1 + country]['VALUE_1000ECU'].ix[1]
    df0 = yearly[year0 + country]['VALUE_1000ECU'].ix[1]

    gr1 = df1.groupby(axis=0, level='PRODUCT_NC')
    gr0 = df0.groupby(axis=0, level='PRODUCT_NC')

    l1 = []
    drop1 = []
    for product in gr1.groups.keys():
        try:
            l1.append((iyear1, product, ref_dict[product]))
        except KeyError:
            drop1.append(product)

    l0 = []
    drop0 = []
    for product in gr0.groups.keys():
        try:
            l0.append((iyear0, product, ref_dict[product]))
        except KeyError:
            drop0.append(product)

    # Check if return is actually what you want to do.
    return (
        np.log(df1 / gr1.sum().reindex(df1.index, level='PRODUCT_NC')).ix[iyear1] - (
        np.log(df0 / gr0.sum().reindex(df0.index, level='PRODUCT_NC')).ix[iyear0]) - (
        np.log(df1.ix[l1].ix[iyear1].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df1.index, level='PRODUCT_NC').ix[iyear1] / gr1.sum().reindex(df1.index, level='PRODUCT_NC').ix[iyear1]) - (
        np.log(df0.ix[l0].ix[iyear0].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df0.index, level='PRODUCT_NC').ix[iyear0] / gr0.sum().reindex(df0.index, level='PRODUCT_NC').ix[iyear0])
        )
        )
        ) ** square

    print('done with %r.') % country

for country in declarants:
    for year in years[1:]:
        gmm_store['y' + str(year) + '_' + country] = get_shares(country, year)

##############################################################################
# Testing

# os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
# yearly = pd.HDFStore('yearly.h5')
# country = '001'
# df07 = yearly['y2007_001'].head(500)['VALUE_1000ECU'].ix[1]
# df08 = yearly['y2008_001'].head(500)['VALUE_1000ECU'].ix[1]

# gr07 = df07.groupby(axis=0, level='PRODUCT_NC')
# gr08 = df08.groupby(axis=0, level='PRODUCT_NC')

# # Without Year
# # df = yearly['y2007_001'].head(500)['VALUE_1000ECU'].ix[1, 200752]
# # grouped = df.groupby(axis=0, level='PRODUCT_NC')

# ref_dict = get_reference(yearly, country)
# # Not necessary, good for testing though
# # ref_tuple = [(k, v) for k, v in ref_dict.iteritems()]

# # Now Generalize to arbitrary product!

# # adiff = np.log(df08 / gr08.sum().reindex(df08.index, level='PRODUCT_NC')).ix[200852] - (
# #         np.log(df07 / gr07.sum().reindex(df07.index, level='PRODUCT_NC')).ix[200752]) - (
# #         Insert Arbitrary reference here)

# # Now diff with the reference
# # Pass .ix[] a list of tuples: get = [(200852, '01', 3), (200852, '01', 5)]

# """
# Let me tell you my strategy.
# We want the values for the ref country.  Start with the dict of pairs and
# filter out only those that are valid (i.e. there exists a reference partner).

# Then filter down the full df to just the partners by passing a list of the
# (year, prodcut, ref_partner) tuples.

# Next drop the year and PARTNER levels with .ix[year] and rest_index & select
# just the Value.  This gives us a # Produ2cts x 1 series of the reference
# values.

# Now broadcast this up with .reindex.  Finally take the difference.
# """

# l1 = gr08.groups.keys()
# l2 = []
# drops08 = []
# for x in l1:
#     try:
#         l2.append((200852, x, ref_dict[x]))
#     except KeyError:
#         drops08.append(x)

# refs = df08.ix[l2]

# l3 = gr07.groups.keys()
# l4 = []
# drops07 = []
# for x in l3:
#     try:
#         l4.append((200752, x, ref_dict[x]))
#     except KeyError:
#         drops07.append(x)


# ydiff = np.log(df08 / gr08.sum().reindex(df08.index, level='PRODUCT_NC')).ix[200852] - (
#         np.log(df07 / gr07.sum().reindex(df07.index, level='PRODUCT_NC')).ix[200752])


# kdiff = np.log(df08.ix[l2].ix[200852].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df08.index, level='PRODUCT_NC').ix[200852] / gr08.sum().reindex(df08.index, level='PRODUCT_NC').ix[200852]) - (
#         np.log(df07.ix[l4].ix[200752].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df07.index, level='PRODUCT_NC').ix[200752] / gr07.sum().reindex(df07.index, level='PRODUCT_NC').ix[200752])
#         )

# # ydiff - kdiff Goes in the table (squared)

# np.log(df08 / gr08.sum().reindex(df08.index, level='PRODUCT_NC')).ix[200852] - (
#         np.log(df07 / gr07.sum().reindex(df07.index, level='PRODUCT_NC')).ix[200752]) - (
#         np.log(df08.ix[l2].ix[200852].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df08.index, level='PRODUCT_NC').ix[200852] / gr08.sum().reindex(df08.index, level='PRODUCT_NC').ix[200852]) - (
#         np.log(df07.ix[l4].ix[200752].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df07.index, level='PRODUCT_NC').ix[200752] / gr07.sum().reindex(df07.index, level='PRODUCT_NC').ix[200752])
#         )
#         )
