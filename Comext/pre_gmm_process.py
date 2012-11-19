from __future__ import division

import os
from cPickle import load
from datetime import datetime

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

(PROD, Partner)

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
    1. Find reference country for each good
    2. Construct empty DataFrame
    3. Calculate delta k log shares for every variety.
        -Plan is to use df.apply

    3. Calculate delta k log prices for every variety.
    4. Multiply for the delta k cross
    5. Square prices and shares at the end, in place.
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

prices = ['p_2008', 'p_2009', 'p_2010', 'p_2011']
shares = ['s_2008', 's_2009', 's_2010', 's_2011']
cross = ['ps_2008', 'ps_2009', 'ps_2010', 'ps_2011']
cols = shares + prices + cross
start_time = datetime.now()


def get_shares(df_col, country, product, refcountry, year, iyear, prev, iprev, store=yearly):
    """
    To fill the initialized DataFrame.

    Call with:

    s_test.head(5).ix[product].apply(get_shares, axis=1, args=(country, product,
        refcountry, year, iyear, prev, iprev))


    Params
    df_col: Either a row or series from a DataFrame, not sure.
    country : String. From the outer loop
    product : String. From the next loop
    refcountry : Int. From reference dict.
    year : String, pulled from column name.
    iyear : Int. Pulled from column name.
    prev : String. Derived from column name.
    iprev: Int. Derived from column name.


    Returns
    -------
    A scaler that will fill the gmm_calc matrix.  Not yet squared though.

    Example:
    for country in declarants:
        for column in tb[shares]:
            for product in tb[column].index.levels[0]:
                reference_tuple = get_reference(yearly, country)
                reference = reference_tuple[1]
                refcountry = reference[product]
                year = 'y' + column[-4:] + '_'
                iyear = int(year[1:5] + '52')
                prev = 'y' + str(int(year[1:5]) - 1) + '_'
                iprev = int(prev[1:5] + '52')
                try:
                    value_sum = (
                        np.log(yearly[year + country]['VALUE_1000ECU'].ix[1, iyear,
                        product].sum()))
                except:
                    print('Couldn\'t calculate sum for %r') % (
                        product)
                try:
                    prior_sum = (
                        np.log(yearly[prev + country]['VALUE_1000ECU'].ix[1, iprev,
                        product].sum()))
                except:
                    print('Couldn\'t calculate prev for %r') % (product)
                ref_share = (
                    np.log(yearly[year + country]['VALUE_1000ECU'].ix[(1, iyear, product, refcountry)] / value_sum).values - (
                    np.log(yearly[prev + country]['VALUE_1000ECU'].ix[(1, iprev, product, refcountry)] / prior_sum).values))
                tb['c_' + country][column].ix[product] = tb['c_' + country][[column]].ix[
                    product].apply(get_shares, axis=1, args=(country, product,
                    refcountry, year, iyear, prev, iprev))
    """

    partner = df_col.name
    print('Working on %r, %r') % (product, partner)
    print(datetime.now() - start_time)

    try:
        return ((np.log(store[year + country]['VALUE_1000ECU'].ix[(1, iyear, product, partner)] / value_sum).values) - (
                np.log(store[prev + country]['VALUE_1000ECU'].ix[(1, iprev, product, partner)] / prior_sum).values) - (
                ref_share))
    except:
        print('Failed on the fill of %r, %r') % (product, partner)


def get_prices(df_col, country, product, refcountry, year, iyear, prev, iprev,
    store=yearly):
    """
    Use to fill prices for gmm calculation.

    Parameters
    ----------
    df_col : the column/row being applied to
    country : String. From the outer loop
    product : String. From the next loop
    refcountry : Int. From reference dict.
    year : String, pulled from column name.
    iyear : Int. Pulled from column name.
    prev : String. Derived from column name.
    iprev: Int. Derived from column name.

    Example:
    for country in declarants:
        for column in gmm_matrix[prices]:
            for product in p_test.index.levels[0]:
                refcountry = reference[product]
                year = 'y' + column[-4:] + '_'
                iyear = int(year[1:5] + '52')
                prev = 'y' + str(int(year[1:5]) - 1) + '_'
                iprev = int(prev[1:5] + '52')
                ref_price = np.log(yearly[year + 'price_' + country].ix[1, iyear, product, refcountry].values) - (
                            np.log(yearly[prev + 'price_' + country].ix[1, iprev, product, refcountry].values))

                p_test.ix[product].apply(get_prices, axis=1, args=(country, product, refcountry, year, iyear, prev, iprev))
    """

    partner = df_col.name
    print('Working on %r') % partner
    print(datetime.now() - start_time)
    try:
        return (np.log(store[year + 'price_' + country].ix[1, iyear, product, partner].values)[0] -
                np.log(store[prev + 'price_' + country].ix[1, iprev, product, partner].values)[0]) - (
                ref_price)
    except:
        print('Failed on the fill of %r, %r') % (product, partner)


# Test Producdure
# yearly = pd.HDFStore('yearly.h5')
# product = '01'
# country = '001'
# year = 'y2008_'
# iyear = 200852
# prev = 'y2007_'
# iprev = 200752
# variety = ('01', 3)
# reference_tuple = get_reference(yearly, country)
# reference = reference_tuple[1]
# refcountry = reference[variety[0]]
# ref_price = float(np.log(yearly[year + 'price_' + country].ix[1, iyear, product, refcountry].values) - (
#     np.log(yearly[prev + 'price_' + country].ix[1, iprev, product, refcountry].values)))

# # Particular df depends on testing prices vs. shares
# p_test = tb['c_' + country][['p_2008']]
# df1 = yearly[year + 'price_' + country].head(100)
# df2 = yearly[prev + 'price_' + country].head(100)
# p_test.head(5).apply(get_prices, axis=1, args=(country, product, refcountry, year, iyear, prev, iprev))


# s_test = tb['c_' + country][['s_2008']]
# df1 = yearly[year + country].head(100)
# df2 = yearly[prev + country].head(100)
# s_test.head(5).apply(get_shares, axis=1, args=(country, product, refcountry, year, iyear, prev, iprev))