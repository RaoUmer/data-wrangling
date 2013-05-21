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
from scipy import dot

gmm = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/gmm_store.h5')
df = gmm.select('by_ctry_001')

# Practice

g = df.xs('01', level='PRODUCT_NC')  # Check len(g)


def sse(x, c, p, s):
    """
    Just a plain SSE.  No weighting matrix.
    """
    sig, w = x
    t1 = w / ((1 + w) * (sig - 1))
    t2 = (1 - w * (sig - 2)) / ((1 + w) * (sig - 1))
    u = p ** 2 - t1 * s ** 2 - t2 * c
    return sum(u ** 2)


def sse_w(x, c, p, s, W=None):
    """
    minimize this in the GMM.

    Parameters

    * x: array of parameters to be argmined.
    * c: the cross part from estimation equation.
    * p: the price part from estimation equation.
    * s: the share part from estimation equation.
    * W: weighting matrix.  Default None -> I.

    Returns

    The sum of square errors, possibly weighted by W.
    """
    if W is None:
        W = np.eye(len(c))
    sig, w = x
    t1 = w / ((1 + w) * (sig - 1))
    t2 = (1 - w * (sig - 2)) / ((1 + w) * (sig - 1))
    u = p ** 2 - t1 * s ** 2 - t2 * c
    return dot(dot(u, W), u)


def sse2(x, c, p, s):
    """
    This version estimates theta_1 and theta_2.
    Solve for rho and sigma later.

        BE CAREFUL HERE:
        Frentra's rho (p) != B&W's omega (w)
        p = w * (sig - 1) / (1 + sig * w)

    """
    t1, t2 = x
    u = p ** 2 - t1 * s ** 2 - t2 * c
    return sum(u ** 2)


def minimization(good):
    """
    Idea is for good to be an item from a groupby.

    Need to think about how to go from series of optimize dicts
    to a dataframe.  Either in here or afterwards.
    """
    print(good.name)
    return optimize.minimize(sse, x0=[2, 2], method='Nelder-Mead', args=good.dropna().values.T)


def minimization_w(good):
    """
    Idea is for good to be an item from a groupby.

    Need to think about how to go from series of optimize dicts
    to a dataframe.  Either in here or afterwards.
    """
    print(good.name)
    return optimize.minimize(sse, x0=[2, 2], method='Nelder-Mead', args=good.dropna().values.T)


def minimization2(good):
    """
    This one calls sse2 which solves for theta_1 and theta_2.
    Idea is for good to be an item from a groupby.

    Need to think about how to go from series of optimize dicts
    to a dataframe.  Either in here or afterwards.
    """
    print(good.name)
    return optimize.minimize(sse2, x0=[2, 2], method='Nelder-Mead', args=good.dropna().values.T)


def of_interest(thetas):
    t1, t2 = thetas
    p = .5 + np.sign(t2) * (.25 - (1 / (4 + t2 ** 2 / t1))) ** 0.5
    sig = 1 + ((2 * p - 1) / (1 - p)) / t2
    w = p / (sig * (1 - p) - 1)
    return (p, sig, w)

if __name__ == '__main__':
    from cPickle import load
    base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
    gmm = pd.HDFStore(base + 'gmm_store.h5')
    with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
        country_code = load(declarants)

    declarants = sorted(country_code.keys())
    for ctry in declarants:
        df = gmm.select('by_ctry_001')
        gr = df.groupby(level='PRODUCT_NC')
        res = gr.apply(minimization)  # takes a while.  Maybe 5 - 10 min?
        res2 = pd.DataFrame([dict(x) for x in res])
        res2.index = res.index


## Optimizing
sub = df[:10000]
gr = sub.groupby(level='PRODUCT_NC')
