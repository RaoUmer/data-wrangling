"""
A collection of helpers to calculate and write out summary statistics
for the data files.

We'll mainly deal with the files

    filtered_for_gmm.h5               (Before)
    filtered_gmm_results_weighted.h5  (After)

or

    for_gmm.h5               (Before)
    gmm_results_weighted.h5  (After)

depending on if I figure out the weighitng stuff.
Care will need to be taken to get the counts adjusted for NaNs correctly.
"""

import cPickle

import pandas as pd

#-----------------------------------------------------------------------------
base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'

with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
    country_code = cPickle.load(declarants)

pre_gmm = pd.HDFStore(base + 'filtered_for_gmm.h5')  # '/ctry_001'

declarants = sorted(country_code.keys())


def get_number_of_goods(df):
    return df['price'].groupby(level='period').count().plot()


def get_partner_counts(df):
    """ Returns a Series of counts"""
    return df['price'].groupby(level=('period', 'partner')).count()


def get_top_partner_shares(df, yearly=True):
    """ Shares of imports by value. May want to use
    an earlier dataframe. Trouble with infs right now.
    """
    if yearly:
        gr = df.groupby(level=('period', 'partner'))
    else:
        gr = df.groupby(level='partner')
        # return
