import os

import numpy as np
import pandas as pd
from get_reference2 import get_reference

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')

# Globals
# Probably will become for country in []
country = '001'

ref_tuple = get_reference(yearly, country)
ref_dict = ref_tuple[1]

# For now we'll focus on with year.  May need it later.


##############################################################################
# Testing

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')
country = '001'
df07 = yearly['y2007_001'].head(500)['VALUE_1000ECU'].ix[1]
df08 = yearly['y2008_001'].head(500)['VALUE_1000ECU'].ix[1]

gr07 = df07.groupby(axis=0, level='PRODUCT_NC')
gr08 = df08.groupby(axis=0, level='PRODUCT_NC')

# Without Year
# df = yearly['y2007_001'].head(500)['VALUE_1000ECU'].ix[1, 200752]
# grouped = df.groupby(axis=0, level='PRODUCT_NC')

ref_dict = get_reference(yearly, country)
ref_tuple = [(k, v) for k, v in ref_dict.iteritems()]

# Get shares
# df07.ix[200752, '01'] / gr07.sum().ix['01']
# df08.ix[200752, '01'] / gr08.sum().ix['01']

# The diff.  Currently specific to a product
# Note can't use .ix[:] for year since then the subtraction treat them
# as different indices.

ref_country = ref_dict['01']

year_diff = np.log(df08.ix[200852, '01'] / gr08.sum().ix['01']) - (
            np.log(df07.ix[200752, '01'] / gr07.sum().ix['01'])) - (
            np.log(df08.ix[200852, '01', 3] / gr08.sum().ix['01']) - (
            np.log(df07.ix[200752, '01', 3] / gr07.sum().ix['01'])))

# Now Generalize to arbitrary product!

adiff = np.log(df08 / gr08.sum().reindex(df08.index, level='PRODUCT_NC')).ix[200852] - (
        np.log(df07 / gr07.sum().reindex(df07.index, level='PRODUCT_NC')).ix[200752]) - (
    )

# Now diff with the reference
# Pass .ix[] a list of tuples: get = [(200852, '01', 3), (200852, '01', 5)]

"""
Let me tell you my strategy.
We want the values for the ref country.  Start with the dict of pairs and
filter out only those that are valid (i.e. there exists a reference partner).

Then filter down the full df to just the partners by passing a list of the
(year, prodcut, ref_partner) tuples.

Next drop the year and PARTNER levels with .ix[year] and rest_index & select
just the Value.  This gives us a # Products x 1 series of the reference
values.

Now broadcast this up with .reindex.

"""

l1 = gr08.groups.keys()
l2 = []
drops08 = []
for x in l1:
    try:
        l2.append((200852, x, ref_dict[x]))
    except KeyError:
        drops08.append(x)

refs = df08.ix[l2]

l3 = gr07.groups.keys()
l4 = []
drops07 = []
for x in l3:
    try:
        l4.append((200752, x, ref_dict[x]))
    except KeyError:
        drops07.append(x)


ref_d = np.log(df08.ix[l2].ix[200852].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df08.index, level='PRODUCT_NC').ix[200852] / gr08.sum().reindex(df08.index, level='PRODUCT_NC').ix[200852]) - (
        np.log(df07.ix[l4].ix[200752].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df07.index, level='PRODUCT_NC').ix[200752] / gr07.sum().reindex(df07.index, level='PRODUCT_NC').ix[200752])
        )


# def diff(df1, gr1, df2, gr2):
#     np.log(df1.ix[])
