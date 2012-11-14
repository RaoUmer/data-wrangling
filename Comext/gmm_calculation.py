from __future__ import division

import os
from cPickle import load

import numpy as np
import pandas as pd
from weighting_matrix import weight_matrix as wm


os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

with open('years_dict.pkl', 'r') as years_dict_file:
    years_dict = load(years_dict_file)
years_dict_file.closed
years = sorted(years_dict.keys())


def flip(x):
    if x == 1:
        return 2
    else:
        return 1


def error(w, s, store, country, product, partner, year, reference, flow):
    """
    u_gct = [delta^k * ln(p_gct)]**2 - theta_1 * (delta^k * ln(s_gct))**2 -
        theta_2 * (delta^k * ln(p_gct) * delta^k * ln(s_gct))

    Where
        theta_1 = w_g / ((1 + w_g)(sigma_g - 1))
        theta_2 = (1 - w_g(sigma_g - 2)) / ((1 + w_g)(sigma_g -1))

    Parameters:
    -----------
    s : the elasticity of substitution for that variety
    w : omega, inverse supply elasticity


    # TODO:
    # Build in some error control for if no ref in EuroArea.  May want
    # to avoid the EU group btw.
    ------------------------
    I still don't know. Just build it flexible. Feenstra 1994 says
    'eliminate the random terms [...]by subtracting the same equation
    for source k' p. 163.
    """

    y0 = years[years.index(year) - 1]

    share = np.log(store[year + '_' + country]['VALUE_1000ECU'].xs((flow, product, partner),
        level=('FLOW', 'PRODUCT_NC', 'PARTNER')) / (
        store[year + '_' + country]['VALUE_1000ECU'].xs((flow, product),
        level=('FLOW', 'PRODUCT_NC'))['VALUE_1000ECU'].sum())) - (
        np.log(store[y0 + '_' + country])['VALUE_1000ECU'].xs((flow, product, partner),
        level=('FLOW', 'PRODUCT_NC', 'PARTNER')) / (
        store[y0 + '_' + country]['VALUE_1000ECU'].xs((flow, product),
        level=('FLOW', 'PRODUCT_NC'))['VALUE_1000ECU'].sum()))

    # This needs to be looked at more closely.  What is going on with the reference?
    # Are we differencing on its exports?  For that variety or that good?

    ref_share = (
        np.log(store[year + '_' + country]['VALUE_1000ECU'].xs((flip(flow), product, partner),
        level=('FLOW', 'PRODUCT_NC', 'PARTNER')) / (
        store[year + '_' + country]['VALUE_1000ECU'].xs((flip(flow), product),
        level=('FLOW', 'PRODUCT_NC'))['VALUE_1000ECU'].sum())) - (
        np.log(store[y0 + '_' + country])['VALUE_1000ECU'].xs((flip(flow), product, partner),
        level=('FLOW', 'PRODUCT_NC', 'PARTNER')) / (
        store[y0 + '_' + country]['VALUE_1000ECU'].xs((flip(flow), product),
        level=('FLOW', 'PRODUCT_NC'))['VALUE_1000ECU'].sum()))
        )

    price = np.log(store[year + '_price_' + country].xs((flow, product, partner),
        level=('FLOW', 'PRODUCT_NC', 'PARTNER'))) - np.log(
        store[y0 + '_price_' + country].xs((flow, product, partner),
        level=('FLOW', 'PRODUCT_NC', 'PARTNER')))

    # This needs to be looked at more closely.  What is going on with the reference?
    # Are we differencing on its exports?  For that variety or that good?
    # Very unsure here.  Don't give it any status quo bias.

    ref_price = np.log(store[year + '_price_' + reference]).xs(
        (flow, product, partner), level=('FLOW', 'PRODUCT_NC', 'PARTNER')) - (
        np.log(store[y0 + '_price_' + reference]).xs((flow, product, partner),
        level=('FLOW', 'PRODUCT_NC', 'PARTNER')))

    theta_1 = w / ((1 + w) * (s - 1))
    theta_2 = (1 - w * (s - 2)) / ((1 + w) * (s - 1))

    u = ((price - ref_price) ** 2 - theta_1 * (share - ref_share) ** 2 +
            theta_2 * ((price - ref_price) * (share - ref_share)))

    # Now (I think) the goal is to use GMM to estimate theta_i to
    # minimize the weighted SSR w/ moments E(u_i,t,(c?)) = 0.








    # Finally, solve for:

    rho_hat = .5 + (.25 - (1 / (4 + (theta_2 ** 2 / theta_1 ** 2)))) ** (1 / 2)
    sigma_hat = 1 + ((2 * rho_hat) / (1 - rho_hat)) * (1 / theta_2)


    # prices = (np.log(store[year + '_' + 'price' + '_' + country].xs(
    #     (years_dict[year], product), level=('PERIOD', 'PRODUCT_NC'))) -
    #     np.log(store[year + '_' + 'price' + '_' + reference].xs(
    #     (years_dict[year], product), level=('PERIOD', 'PRODUCT_NC')))) ** 2

    # # ((price * quantity) of variety) / (total exp on that product.)
    # shares = (np.log(store[year + '_price' + country].xs((product, partner),
    #     level=('PRODUCT_NC', 'PARTNER'))) * (
    # store['quantity_' + country].xs((product, partner))))

    # ASSUME A REFERENCE COUNTRY


def picker(list):
    done = False
    while done == False:
        for int in list:
            if int in partners:
                return partners[int]
                done = True
            else:
                pass
    else:
        print 'No Matches!'


def get_reference(store, country,
        years=['y2007', 'y2008', 'y2009', 'y2010', 'y2011']):
    """
    Finds potential countries to use as k in calculating errors.
    Must provide a positive quantity in every year. (Exports & Imports?)

    Read inside out to maintain sanity.  Would be so easy recursively...
        Get index wm for first year possible (i.e. second year in sample).
        Filter by calling .ix on that index; drop the NaNs.  Take that index.
        ...
        End with index of (flow, product, partner) that works as references.

    TODO:
    Going to have to rework this to return a list of potentials for each product.
    From that list we'll (automatically according to some criteria) choose
    the reference **for that product**.  That criteria MUST include preference
    for other countries in the dataset.  If not, no way to calculate moment.

    Parameters:
    -----------
    store : HDF5Store
    country : String
    years: list of strings

    Returns:
    --------
    DataFrame (call index on this; for storage reasons)
    """

    df = wm(store, country, years[4]).ix[
        wm(store, country, years[3]).ix[
        wm(store, country, years[2]).ix[
        wm(store, country, years[1]).index
        ].dropna().index
        ].dropna().index
        ].dropna()

    for prod in np.unique(df.index.get_level_values('PRODUCT_NC')):
        print picker(df.xs((1, prod), level=('FLOW', 'PRODUCT_NC')).index)
            
