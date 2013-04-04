"""

You have a df like:
                          'p', s, c
year, partner, product ||


GMM go!
"""
from functools import partial

import numpy as np
import pandas as pd
from scipy import optimize

gmm = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/gmm_store.h5')
df = gmm.select('by_ctry_001')

# Practice

g = df.xs('01', level='PRODUCT_NC')  # Check len(g)


def sse(x, df=g.dropna()):
    """
    TODO: CYTHONIZE!
    May need to do for good in df.index.levels[x]:
        sse_ = partial(sse, df=df.xs(x, level=whatever))

    Even better: def a func and groupby country and apply!
    """
    s, w = x
    t1 = w / ((1 + w) * (s - 1))
    t2 = (1 - w * (s - 2)) / ((1 + w) * (s - 1))
    u = df.p ** 2 - t1 * df.s ** 2 - t2 * df.c
    return (u ** 2).sum()  # replace with dot prod and weighting matrix.


def minimization(good):
    """
    Idea is for good to be an item from a groupby.

    Need to think about how to go from series of optimize dicts
    to a dataframe.  Either in here or afterwards.
    """
    fn = partial(sse, df=good)
    print(good.name)
    return optimize.minimize(fn, x0=[2, 2], method='Nelder-Mead')

if __name__ == '__main__':
    from cPickle import load

    gmm = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/gmm_store.h5')
    with open('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/declarants_no_002_dict.pkl',
              'r') as declarants:
        country_code = load(declarants)

    declarants = sorted(country_code.keys())
    for ctry in declarants:
        df = gmm.select('by_ctry_001')
        gr = df.groupby(level='PRODUCT_NC')
        res = gr.apply(minimization)  # takes a while.  Maybe 5 - 10 min?
        res2 = pd.DataFrame([x.values() for x in res], columns=res[0].keys(), index=res.index)

## Optimizing
sub = df[:10000]
gr = sub.groupby(level='PRODUCT_NC')
