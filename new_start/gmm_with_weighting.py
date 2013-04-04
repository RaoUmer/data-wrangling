"""
You have a df like:
                          'p', s, c
year, partner, product ||


GMM go!
"""
import numpy as np
import pandas as pd
from scipy import optimize
from scipy import dot


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


def minimization_w(good, W=None, n_min=4):
    """
    Idea is for good to be an item from a groupby.
    Changed small samples to return -5 for status code.
    """
    # print(good.name)
    res = optimize.minimize(sse_w, x0=[2, 2], method='Nelder-Mead',
                            args=good.dropna().values.T)
    if len(good) < n_min:
        res['status'] = -5
    return res

if __name__ == '__main__':
    from cPickle import load
    from datetime import datetime

    base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
    gmm = pd.HDFStore(base + 'gmm_store.h5')
    gmm_results = pd.HDFStore(base + 'gmm_results')
    with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
        country_code = load(declarants)

    declarants = sorted(country_code.keys())
    for ctry in declarants:
        t = datetime.utcnow()
        df = gmm.select('by_ctry_' + ctry)
        gr = df.groupby(level='PRODUCT_NC')
        res = gr.apply(minimization_w)  # takes a while.  Maybe 5 - 10 min?
        res2 = pd.DataFrame([dict(x) for x in res])
        res2.index = res.index
        res2 = res2.drop('message', axis=1)
        thetas = pd.DataFrame([[y[0], y[1]] for y in res2.x.values],
                              index=res2.index, columns=['t1', 't2'])
        res2 = res2.join(thetas)
        res2 = res2.drop('x', axis=1)
        gmm_results.append('params_' + ctry, res2)
        print('Finshed {} at'.format(ctry))
        print(datetime.utcnow() - t)
