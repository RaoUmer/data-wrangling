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


def get_shares(df_col, store=yearly):
    """
    To fill the initialized DataFrame.

    Pass it a DataFrame called via tb['c'+country] =
        tb['c+country'][[s_20YY]].apply(get_shares, axis=1).

    Params
    df_col: an n x 1 DataFrame via [[column]]

    Returns
    -------
    A scaler that will fill the gmm_calc matrix.  Not yet squared though.
    """

    year = 'y' + df_col.index[0][-4:] + '_'
    iyear = int(year[1:5] + '52')
    variety = df_col.name
    refcountry = reference[variety[0]]
    prev = 'y' + str(int(year[1:5]) - 1) + '_'
    iprev = int(prev[1:5] + '52')

    # if product == ref_product:
    #     pass
    # else:
    #     global ref_product
    #     ref_product = product

    print('Working on %r, %r') % (variety[0], variety[1])
    print(datetime.now() - start_time)
    try:
        value_sum = (
            np.log(store[year + country]['VALUE_1000ECU'].ix[1, iyear,
            variety[0]].sum()))

    except:
        print('Couldn\'t calculate sum for %r, %r') % (variety[0], variety[1])

    try:
        prior_sum = (
            np.log(store[prev + country]['VALUE_1000ECU'].ix[1, iprev,
            variety[0]].sum()))

    except:
        print('Couldn\'t calculate prev for %r, %r') % (variety[0], variety[1])

    try:
        return ((np.log(store[year + country]['VALUE_1000ECU'].ix[(1, iyear, variety[0], variety[1])] / value_sum)) - (
                np.log(store[prev + country]['VALUE_1000ECU'].ix[(1, iprev, variety[0], variety[1])] / prior_sum)) - (
                np.log(store[year + country]['VALUE_1000ECU'].ix[(1, iyear, variety[0], refcountry)] / value_sum) - (
                np.log(store[prev + country]['VALUE_1000ECU'].ix[(1, iprev, variety[0], refcountry)] / prior_sum))))
    except:
        print('Failed on the fill of %r, %r') % (variety[0], variety[1])


def get_prices(df_col, store=yearly):
    """
    Use to fill for the gmm_calc DataFrame.

    Pass it a DataFrame called via tb['c'+country] =
        tb['c+country'][[p_20YY]].apply(get_shares, axis=1).

    Parameters
    ----------
    df_col : A DataFrame via [[column]]

    Returns
    -------
    A scaler with the price used in the gmm calculation.  Not yet squared.
    """

    year = 'y' + df_col.index[0][-4:] + '_'
    iyear = int(year[1:5] + '52')
    variety = df_col.name
    refcountry = reference[variety[0]]
    prev = 'y' + str(int(year[1:5]) - 1) + '_'
    iprev = int(prev[1:5] + '52')

    try:
        return ((np.log(store[year + 'price_' + country].ix[1, iyear, variety[0], variety[1]]) -
                np.log(store[prev + 'price_' + country].ix[1, iprev, variety[0], variety[1]])) - (
                np.log(store[year + 'price_' + country].ix[1, iyear, variety[0], refcountry]) -
                np.log(store[prev + 'price_' + country].ix[1, iprev, variety[0], refcountry])))
    except:
        print('Failed on the fill of %r, %r') % (variety[0], variety[1])


def get_prices2(df_col, country, product, refcountry, year, iyear, prev, iprev,
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
        for product in p_test.index.levels[0][:34]:
            refcountry = reference[product]
            year = 'y' + column[-4:] + '_'
            iyear = int(year[1:5] + '52')
            prev = 'y' + str(int(year[1:5]) - 1) + '_'
            iprev = int(prev[1:5] + '52')
            ref_price = np.log(yearly[year + 'price_' + country].ix[1, iyear, product, refcountry].values) - (
                        np.log(yearly[prev + 'price_' + country].ix[1, iprev, product, refcountry].values))

            p_test.apply(get_prices2, axis=1, args=(country, product, refcountry, year, iyear, prev, iprev))
    """

    partner = df_col.name[1]
    print('Working on %r') % partner
    try:
        return (np.log(store[year + 'price_' + country].ix[1, iyear, product, partner].values) -
                np.log(store[prev + 'price_' + country].ix[1, iprev, product, partner].values)) - (
                ref_price)[0][0]
    except:
        print('Oh Noes')

# Will probably need to do tb[thing] = tb[thing].apply
# Use df[[column]] to pass a series to apply apparantly axis=1

for country in declarants:
    reference_tuple = get_reference(yearly, country)
    reference = reference_tuple[1]

    for column in tb['c_' + country][shares]:
        tb['c_' + country][[column]] = tb['c_' + country][[column]].apply(get_shares, axis=1)

    for column in tb['c_' + country][prices]:
        tb['c_' + country][[column]] = tb['c_' + country][[column]].apply(get_prices, axis=1)    


# Test Producdure
yearly = pd.HDFStore('yearly.h5')
country = '001'
year = 'y2008_'
iyear = 200852
prev = 'y2007_'
iprev = 200752
variety = ('01', 3)
reference_tuple = get_reference(yearly, country)
reference = reference_tuple[1]
refcountry = reference[variety[0]]

# Particular df depends on testing prices vs. shares
df = tb['c_' + country][['p_2008']]

"""
I'm currently have some index issues.  All the data we're getting is comming
from the y20xx_country leaves.  Our reference index is coming from the quantity
leaves.  The quantity index **should** be a superset of the shares/pricse index.

This means I should be able to move ahead using the quantity index to
initialize the DataFrameself.

Currently hitting an error on the reference lookup for '01019090'
"""


# Displaced Code Below
"""
# Generates the final DataFrame.  Already ran on accident, but it should work.
 for country in declarants:
     tb['c_' + country] = pd.DataFrame(index=reference_tuple[0], columns=cols)


# get_cross().  Going to pick up by filling the gmm_store with non squared
values first, filling the croses with the product, and then squaring the
prices and shares.

def get_cross(df_col, store=yearly):
    """
    # Use to fill the cross column in the gmm_calc DataFrame.
    # Pass it a DataFrame called via tb['c'+country] =
    #     tb['c+country'][[ps_20YY]].apply(get_cross, axis=1).

    # Parameters
    # ----------
    # df_col : A DataFrame via [[column]]

    # Returns
    # -------
    # A scaler with the share * price used in the gmm calculation.
    """

    year = 'y' + df_col.index[0][-4:] + '_'
    iyear = int(year[1:5] + '52')
    variety = df_col.name
    refcountry = reference[variety[0]]
    prev = 'y' + str(int(year[1:5]) - 1) + '_'
    iprev = int(prev[1:5] + '52')

    try:
        value_sum = (
            np.log(store[year + country]['VALUE_1000ECU'].ix[1, iyear,
            variety[0]].sum()))

    except:
        print('Couldn\'t calculate sum for %r, %r') % (variety[0], variety[1])

    try:
        prior_sum = (
            np.log(store[prev + country]['VALUE_1000ECU'].ix[1, iprev,
            variety[0]].sum()))

    except:
        print('Couldn\'t calculate prev for %r, %r') % (variety[0], variety[1])

    return ((np.log(store[year + country]['VALUE_1000ECU'].ix[(1, iyear, variety[0], variety[1])] / value_sum)) - (
            np.log(store[prev + country]['VALUE_1000ECU'].ix[(1, iprev, variety[0], variety[1])] / prior_sum)) - ((
            np.log(store[year + country]['VALUE_1000ECU'].ix[(1, iyear, variety[0], refcountry)] / value_sum)) - (
            np.log(store[prev + country]['VALUE_1000ECU'].ix[(1, iprev, variety[0], refcountry)] / prior_sum)))) * ((
            np.log(store[year + 'price_' + country].ix[1, iyear, variety[0]]) -
            np.log(store[prev + 'price_' + country].ix[1, iprev, variety[0]])) - (
            np.log(store[year + 'price_' + country].ix[1, iyear, variety[0], refcountry]) -
            np.log(store[prev + 'price_' + country].ix[1, iprev, variety[0], refcountry])))


"""


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
