from __future__ import division

import os
from cPickle import load

import numpy as np
from weighting_matrix import weight_matrix as wm

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

with open('partners_dict.pkl', 'r') as partners_dict_file:
    partners_dict = load(partners_dict_file)
partners_dict_file.closed
partners = sorted(partners_dict.keys())


def flip(x):
    if x == 1:
        return 2
    else:
        return 1


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
    Going to have to rework this to return a list of potentials for each prod.
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

    for product in np.unique(df.index.get_level_values('PRODUCT_NC')):
        print picker(df.xs((1, product), level=('FLOW', 'PRODUCT_NC')).index)
