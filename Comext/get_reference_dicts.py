from __future__ import division

import os
import cPickle
import itertools as it

"""
Script to pickle the reference dicts rather than having
to call them on each iteration.  Some memory issues, peaked
at around 6 GB and swaped out a few GB.
"""

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

gmm_store = pd.HDFStore('gmm_store.h5')
with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = cPickle.load(f)

f.close()
yearly = pd.HDFStore('yearly.h5')


def gr(country, years=['y2007', 'y2008', 'y2009', 'y2010', 'y2011']):

    """
    Finds potential countries to use as k in calculating errors.
    Must provide a positive quantity in every year.

    Read inside out to maintain sanity.  Would be so easy recursively...
        Get index for first year possible (i.e. second year in sample).
        Filter by calling .ix on that index; drop the NaNs.  Take that index.
        ...
        End with index of (product, partner) that works as references.

    Parameters:
    -----------
    yearly : HDF5Store
    country : String
    years: list of strings

    Returns:
    --------
    Or maybe a list of tuples with (good, partner) pairs?
    """

    idx = yearly['quantity_' + country][years[4]].ix[1].ix[
          yearly['quantity_' + country][years[3]].ix[1].ix[
          yearly['quantity_' + country][years[2]].ix[1].ix[
          yearly['quantity_' + country][years[1]].ix[1].ix[
          yearly['quantity_' + country][years[0]].ix[1].dropna().index
          ].dropna().index
          ].dropna().index
          ].dropna().index
          ].dropna().index

    holder = '0'
    references = []
    for tuple in idx:
        if tuple[0] == holder:
            pass
        else:
            references.append(tuple)
            holder = tuple[0]
    return {prod: partner for prod, partner in references}

m = it.imap(gr, sorted(declarants))
iz = it.izip(sorted(declarants), m)
d = {k: v for (k, v) in iz}

out = open('references_dict.pkl', 'w')
cPickle.dump(d, out, 2)
