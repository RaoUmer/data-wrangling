import os
from cPickle import load

import numpy as np
import pandas as pd
from weighting_matrix import weight_matrix as wm


with open('years_dict.pkl', 'r') as years_dict:
    years_dict = load(years_dict)
years_dict.closed

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')


def error(store, country, good, partner, year, reference):
    """
    u_gct = [delta^k * ln(p_gct)]**2 - theta_1 * (delta^k * ln(s_gct))**2 -
        theta_2 * (delta^k * ln(p_gct) * delta^k * ln(s_gct))

    Where
        theta_1 = w_g / ((1 + w_g)(sigma_g - 1))
        theta_2 = (1 - w_g(sigma_g - 2)) / ((1 + w_g)(sigma_g -1))

    To get shares: Something like

    over total: df.xs(good, level='PRODUCT_NC')['VALUE_1000ECU'].sum()


    """

    prices = (np.log(store[year + '_' + 'price' + '_' + country].xs(
        (years_dict[year], good), level=('PERIOD', 'PRODUCT_NC'))) -
        np.log(store[year + '_' + 'price' + '_' + reference].xs(
        (years_dict[year], good), level=('PERIOD', 'PRODUCT_NC')))) ** 2

    shares = (np.log(store[]))

    # ASSUME A REFERENCE COUNTRY


def get_reference(store, country,
        years=['y2007', 'y2008', 'y2009', 'y2010', 'y2011']):
    """
    Finds potential countries to use as k in calculating errors.
    Must provide a positive quantity in every year. (Exports & Imports?)

    Read inside out to maintain sanity.  Would be so easy recursivly...
        Get index wm for first year possible (i.e. second year in sample).
        Filter by calling .ix on that index; drop the NaNs.  Take that index.
        ...
        End with index of (flow, good, partner) that works as references.

    TODO:
    Going to have to rework this to return a list of potentials for each good.
    From that list we'll (automatically according to some criteria) choose
    the reference **for that good**.  That critera MUST include preference
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

    return wm(store, country, years[4]).ix[
        wm(store, country, years[3]).ix[
        wm(store, country, years[2]).ix[
        wm(store, country, years[1]).index
        ].dropna().index
        ].dropna().index
        ].dropna()
