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
from parse_optimize_results import opt_dict_format
#-----------------------------------------------------------------------------


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

    ### Rethink over.
    See notes below.  This one finds the errors for a coutry
    and returns the average.  Generates one moment.
    """
    c, p, s = subgroup
    p = p ** 2
    s = s ** 2
    err = p - theta[0] * s - theta[1] * c  # .reshape(1, -1).T)
    if W is None:
        W = np.eye(len(err))
    return dot(dot(err.T, W), err) / len(err)


def gen_params(subgroup, x0, method='Nelder-Mead', options={'disp': False}):
    """Currently at year, partner index. subgroup = grp
    """
    try:
        return optimize.minimize(gen_moms_sse, x0=x0, args=[(subgroup.values.T)],
                                 method=method, options=options)
    except AttributeError:
        print('Failed On frame {}'.format(subgroup.name))
        return (np.nan, np.nan)
#-----------------------------------------------------------------------------

if __name__ == '__main__':
    from cPickle import load
    from datetime import datetime

    base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
    gmm = pd.HDFStore(base + 'gmm_store.h5')
    gmm_results = pd.HDFStore(base + 'gmm_results.h5')
    with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
        country_code = load(declarants)
    declarants = sorted(country_code.keys())

#-----------------------------------------------------------------------------
# Main loop.  Optimize to get params for each good, for each declarant.
    for ctry in declarants:
        print('Working on {}'.format(ctry))
        t = datetime.utcnow()
        try:
            df = gmm.select('by_ctry_' + ctry)
            by_product = df.dropna().groupby(level='PRODUCT_NC')
        except KeyError, AssertionError:
            with open('gmm_logging.txt', 'a') as f:
                f.write('Failed to open or group ctry: {}'.format(ctry))
            continue

        # GMM Estimation.
        res = {name: gen_params(group, x0=[2, 1])
               for name, group in by_product}

        # Formatting and IO.
        res = pd.DataFrame(res).T
        for_csv, for_hd5 = opt_dict_format(res, names=['t1', 't2'])
        try:
            gmm_results.append('res_' + ctry, for_hd5)
        except TypeError:
            for_csv.to_csv('/Volumes/HDD/Users/tom/DataStorage/Comext/'
                           'yearly/ctry_{}.csv'.format(ctry))

        m = 'Finshed country {0} in {1}'.format(ctry, datetime.utcnow() - t)
        try:
            gmail.mail('thomas-augspurger@uiowa.edu', 'Test', m)
        except:
            pass
