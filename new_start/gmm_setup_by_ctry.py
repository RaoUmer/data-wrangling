"""
Goal is to get index like

                          'p', s, c
year, partner, product ||


This file attempts it from the gmm store but not the f (final) leaves.
Doing it this way to get a sensible index first (every year essentailly)
and then merge across p, s, and c.
"""

import itertools as it

import numpy as np
import pandas as pd


def preprocessing(s):
    """
    Helper function.  Takes a dataframe and drops nans, cleans up col names.

    Import stuff is with the stack.  This is to get a nice index for merge later.
    """
    s[np.isinf(s)] = np.nan
    s = s.dropna()
    letter = s.columns[0][0]
    s.columns = [int(y.split('_')[1][-4:]) for y in s.columns]
    s = s.stack()
    s.name = letter
    s.index.names[-1] = 'year'
    s = s.sortlevel('year')
    s = s.reorder_levels((2, 0, 1))  # (year, product, partner)
    return s


def process_and_merge(s):
    """
    Where the action is at.  Is what assemples stacked Dataframes (series)
    into merged dataframe.
    """
    l = [preprocessing(df) for df in s]
    d = {x.name: x for x in l}
    df = pd.DataFrame(d)
    df.index.names = [x.lower() for x in df.index.names]
    return pd.DataFrame(d)

if __name__ == '__main__':
    from cPickle import load

    gmm = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/gmm_store.h5')
    with open('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/declarants_no_002_dict.pkl',
              'r') as declarants:
        country_code = load(declarants)

    declarants = sorted(country_code.keys())

    for ctry in declarants:
        s = iter([gmm['c_' + ctry], gmm['s_' + ctry], gmm['p_' + ctry]])
        df = process_and_merge(s)
        gmm.append('by_ctry_' + ctry, df)
        print('Added country {}'.format(ctry))
    gmm.close()
