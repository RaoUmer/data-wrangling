"""
This file does the differencing across periods and with respect to a reference
country.  See Broda and Weinstein (2006).

Note that we're going to lose some goods here.
"""
from __future__ import division, print_function, unicode_literals

import numpy as np
import pandas as pd
#-----------------------------------------------------------------------------


def _checker(x):
    """
    This would return all possible reference countries for a particular good.
    It's unnecessarily slow though since it finds *all* possible references
    and then chooses the first, so I don't think I'll use it.
    """

    if (x > 0).all():
        return 1
    else:
        return np.nan


def find_reference(df):
    """
    Find a single country from which you imported a specific product
    in every year you imported that product.

    Parameters
    ----------
    df: Dataframe.  Called via apply.

    Returns
    -------
    a series with index like: good.
    """
    year_0 = df.irow(0).name[0]
    year_n = df.irow(-1).name[0]
    for ctry in df.index.levels[-1]:
        tmp = df.xs(ctry, level='partner')
        if sum(tmp['price'] > 0) == year_n - year_0 + 1:
            return ctry
            break
        else:
            continue


def year_diff(df):
    """
    Groupby.apply was taking too much memory.  I think this should work.
    """
    temps = []
    for year in df.index.levels[0][1:]:
        temp = df.xs(year) - df.xs(year - 1)
        temp['period'] = year
        temps.append(temp.reset_index().set_index(
            ['period', 'declarant', 'good', 'partner']))
    return pd.concat(temps)


#-----------------------------------------------------------------------------
in_store = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly'
                       '/by_declarant.h5')

out_store = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly'
                        '/for_gmm.h5')
#-----------------------------------------------------------------------------
items = in_store.iteritems()
for tup in items:
    name = tup[0].lstrip('/')
    print('Working on {}'.format(name))
    df = in_store.select(name)[['price', 'share']]
    gr = df.groupby(level='good')

    refs = gr.apply(find_reference)
    #-------------------------------------------------------------------------
    # Dropping goods with a valid reference.
    to_drop = refs[pd.isnull(refs)].index
    refs = refs.dropna()
    df = df.reset_index()
    df = df[-df['good'].isin(to_drop)]
    df = df.set_index(['period', 'declarant', 'good',
                       'partner'])
    #-------------------------------------------------------------------------
    # Difference by time:
    # period 2001 refers to the change from 2000 to 2001.
    tdiffed = year_diff(df)
    print('Finished the year diff for {}'.format(name))
    #-------------------------------------------------------------------------
    # Now difference with the reference country:
    refs2 = pd.DataFrame(refs, columns=['ref'])
    ref_dict = refs.to_dict()

    gr = tdiffed.dropna().groupby(level=('period', 'declarant', 'good'))
    empty_ = pd.DataFrame(np.zeros((len(tdiffed.dropna().index), 2)),
                          columns=['price', 'share'],
                          index=tdiffed.dropna().index)
    for ind, group in gr:
        ctry = ref_dict[ind[-1]]
        values = group.xs((name[-3:], ind[-1], ctry),
                          level=('declarant', 'good', 'partner'))
        values = values.reindex_like(group, method='ffill')
        empty_.ix[values.index] = values

    res = tdiffed - empty_
    try:
        out_store[name] = res
        print('Added {} to the store'.format(name))
    except:
        print('Using csv for {}'.format(name))
        res.to_csv('ctry_{}.csv'.format(name))
