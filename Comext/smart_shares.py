import os

import numpy as np
import pandas as pd
from get_reference2 import get_reference

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')

# Globals

# This must surely be country depenant?
with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)
f.closed

country = '001'

ref_tuple = get_reference(yearly, country)
ref_dict = ref_tuple

for country in declarants:




def get_shares(country, year, store=yearly):
    """

    Parameters
    ----------
    year : int
    """

    year1 = 'y' + str(year) + '_'
    year0 = 'y' + str(year - 1) + '_'
    iyear1 = int(str(year) + '52')
    iyear0 = int(str(year - 1)+ '52')

    df1 = yearly[year1]['VALUE_1000ECU'].ix[1]
    df0 = yearly[year0]['VALUE_1000ECU'].ix[1]
    
    gr1 = df1.groupby(axis=0, level='PRODUCT_NC')
    gr0 = df0.groupby(axis=0, level='PRODUCT_NC')


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
