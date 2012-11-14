import os
import cPickle

import pandas as pd
    from weighting_matrix import weight_matrix as wm

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

with open('declarants_no_002_dict.pkl', 'r') as declarants:
    countries = cPickle.load(declarants)
declarants.closed

def error():
    """
    u_gct = [delta^k * ln(p_gct)]**2 - theta_1 * (delta^k * ln(s_gct))**2 -
        theta_2 * (delta^k * ln(p_gct) * delta^k * ln(s_gct))

    Where
        theta_1 = w_g / ((1 + w_g)(sigma_g - 1))
        theta_2 = (1 - w_g(sigma_g - 2)) / ((1 + w_g)(sigma_g -1))
    """


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
    1. Going to have to rework this to return a list of potentials for each good.
    From that list we'll (automatically according to some criteria) choose
    the reference **for that good**.


    2. I want to rework this so there's no need to write anything out to disk.
    I want call it for each gmm estimation (I think).  It will return a tuple with
    the reference country for that product.  Probaly will need to attach some info
    about which country it's for.
    Parameters:
    -----------
    store : HDF5Store
    country : String
    years: list of strings

    Returns:
    --------
    DataFrame (call index on this; for storage reasons)

    Will want to return some kind of (product, reference) pair.
    """

    df = wm(store, country, years[4]).ix[
        wm(store, country, years[3]).ix[
        wm(store, country, years[2]).ix[
        wm(store, country, years[1]).index
        ].dropna().index
        ].dropna().index
        ].dropna()

    ref = df.index.levels[2]

