"""
# TODO: You last run (may) have failed because some of the optimizations
will  return None.  That makes your dataframe of type ```object```,
which cannot be appended.

You have a df like:
                          'p', s, c
year, partner, product ||


GMM go!
"""
from __future__ import division, print_function, unicode_literals

import numpy as np
import pandas as pd
from scipy import optimize
from scipy import dot

import gmail


def sse_w(x, c, p, s, W=None):
    """
    minimize this in the GMM.  Make sure you're
    estimating the params of interst and not theta...

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
    t1, t2 = x
    # t1 = w / ((1 + w) * (sig - 1))
    # t2 = (1 - w * (sig - 2)) / ((1 + w) * (sig - 1))
    u = p ** 2 - t1 * s ** 2 - t2 * c
    return (1 / len(c)) * dot(dot(u, W), u)


def minimization_w(good, x0=[2, 2], W=None, n_min=4, method='Nelder-Mead'):
    """
    Idea is for good to be an item from a groupby.
    Changed small samples to return -5 for status code.
    """
    # print(good.name)
    res = optimize.minimize(sse_w, x0=x0, method=method,
                            args=good.dropna().values.T)
    if len(good) < n_min:
        res['status'] = -5
    return res


def _theta_to_interest(t1, t2):
    """
    GMM estimates theta1 and theta2, we want sigma and omega.
    """
    pass


def gen_moms_sse(theta, subgroup, W=None):
    """
    ### Rethink:
        The mean of the mean error is the same as the mean of the errors.
        i.e. it doesn't matter if I groupby country, find the average error,
        and pass those errors up (one per country) to be averaged VS.
        simply taking the average error upfront. Right?
    FU 1011
    ### Rethink over.
    See notes below.  This one finds the errors for a coutry
    and returns the average.  Generates one moment.
    """
    err = ((subgroup.p ** 2 - theta[0] * subgroup.s ** 2 -
            theta[1] * subgroup.c).values.reshape(1, -1).T)
    if W is None:
        W = np.eye(len(err))
    return dot(dot(err.T, W), err) / len(err)


# def t(x, theta=2):
#     return inner_error(x)


def gen_params(subgroup, x0, method='Nelder-Mead', options={'disp': False}):
    """Currently at year, partner index. subgroup = grp
    """
    try:
        return optimize.minimize(gen_moms_sse, x0=x0, args=[(subgroup)],
                                 method=method, options=options)
    except AttributeError:
        print('Failed On frame {}'.format(subgroup.name))
        return (np.nan, np.nan)


if __name__ == '__main__':
    from cPickle import load
    from datetime import datetime

    base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
    gmm = pd.HDFStore(base + 'gmm_store.h5')
    gmm_results = pd.HDFStore(base + 'gmm_results.h5')
    with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
        country_code = load(declarants)

    declarants = sorted(country_code.keys())
    for ctry in declarants:
        t = datetime.utcnow()
        df = gmm.select('by_ctry_' + ctry)
        by_product_partner = df.dropna().groupby(level=['PRODUCT_NC', 'PARTNER'])
        res = {name: gen_params(group, x0=[2, 1])
               for name, group in by_product_partner}
        res = pd.DataFrame(res).T
        res.reset_index(inplace=True)
        res = res.rename(columns={0: 'theta1', 1: 'theta2', 'index': 'tuples'})
        res.index = pd.MultiIndex.from_tuples(res['tuples'], names=['product', 'partner'])
        res = res.drop('tuples', axis=1)
        try:
            res = res.astype('float')
            gmm_results.append('res_' + ctry, res)
        except TypeError:
            res.to_csv('/Volumes/HDD/Users/tom/DataStorage/Comext/'
                       'yearly/ctry_{}.csv'.format(ctry))

        m = 'Finshed country {0} in {1}'.format(ctry, datetime.utcnow() - t)
        try:
            gmail.mail('thomas-augspurger@uiowa.edu', 'Test', m)
        except:
            pass
