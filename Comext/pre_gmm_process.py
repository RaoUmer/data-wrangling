from __future__ import division

import os
from cPickle import load

import numpy as np
import pandas as pd
from get_reference2 import get_reference

"""
Goal is to get necessary data into a final DataFrame that will
be used for the gmm estimation.  I **think** we'll do one gmm estimation
for each year and then take the average of those.

For each country i, we'll have G goods that it *imported* (each year?).
Each country will have one DataFrame for each good G, with each DataFrame
of dimension c varities (partners) x 3 * y (number of years).

*I'm assuming here that we're only looking at varities we have observations
for every year?*
But why do that?  All we need is 2 years for an estimation, right?  This
will force me to have different indecies though.  Right now I'm just going
to accept NA's in the DataFrame.


  p_gct^2 | s_gct^2 | p_gct * s_gct || p_gct+1^2 | s_gct+1^2 | p_gct+1*s_gct+1

PROD

where each has been differenced with an appropriate country (same accros t,
different (potentially) across g).

The pyTable should ideally look like
|-root
|  |
|  |-Counties (N: 'c001')
|  |  |
|  |  | -Goods (G: '01')
|  |  |
|  |  |
|  |  |

But will probably just be 'cXXX_YYYYYYYY' where XXX is the country code
and YYYYYYYY is the CN8 PRODUCT_NC identifier.

To avoid a massive number of leaves in the table, I'm going to take
a bit of a risk and just to 1 df / country, and not differentiate
by goods.

Implementation
--------------
For each country:
    For each good:
        1. Find reference country
        2. Calculate delta k log shares for every variety.
        3. Calculate delta k log prices for every variety.

TODO:
    Check on "weighting the data".  Does that mean the values in the
    DataFrames I'm counstructing need to be scaled?  Or does this go in
    the actual weighting matrix?

"""

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')
tb = pd.HDFStore('gmm_store.h5')

with open('declarants_no_002_dict.pkl', 'r') as declarants:
    country_code = load(declarants)
declarants.closed

declarants = sorted(country_code.keys())

cols = [
        'p_2008', 's_2008', 'ps_2008',
        'p_2009', 's_2009', 'ps_2009',
        'p_2010', 's_2010', 'ps_2010',
        'p_2011', 's_2011', 'ps_2011']


for country in declarants:
    reference_tuple = get_reference(yearly, country)
    reference = reference_tuple[1]
    tb['c_' + country] = pd.DataFrame(index=reference_tuple[0], columns=cols)


    #     tb['c_' + country] = pd.DataFrame((np.log(yearly['quantity_' + country].xs(
    #         1, level='FLOW')[years[1]]) - np.log(yearly['quantity_' + country].xs(
    #         1, level='FLOW')[years[0]]))-(np.log(yearly['quantity_' + qq        refctry].xs(
    #         1, level='FLOW')[years[1]]) - np.log(yearly['quantity_' + refctry].xs(
    #         1, level='FLOW')[years[0]]) ** 2
    # except:
    #     print('Trouble with %s setup') % country
    #     break
    # for year in years:
    #     try:
    #         yearly['c_' + country] = yearly['c_' + country].merge(pd.DataFrame(
    #             yearly))
