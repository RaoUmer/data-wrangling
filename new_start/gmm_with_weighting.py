"""
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

# import gmail
# from outliers_after_weighting import pre
from parse_optimize_results import opt_dict_format
#-----------------------------------------------------------------------------


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
    # p = p ** 2
    # s = s ** 2
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


def fit_one(pre=None, ctry=None):
    if pre is None:
        pre = load_pre(ctry)
    by_product = pre.dropna().groupby(level='PRODUCT_NC')
    res = {name: gen_params(group, x0=[2, 1]) for name, group in by_product}
    res = pd.DataFrame(res).T
    for_csv, for_hd5 = opt_dict_format(res, names=['t1', 't2'])
    return (for_csv, for_hd5)


#-----------------------------------------------------------------------------

if __name__ == '__main__':
    from cPickle import load
    from datetime import datetime

    base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
    gmm = pd.HDFStore(base + 'for_gmm.h5')
    gmm_results = pd.HDFStore(base + 'gmm_results.h5')
    with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
        country_code = load(declarants)
    declarants = sorted(country_code.keys())
    i = 0
#-----------------------------------------------------------------------------
# Main loop.  Optimize to get params for each good, for each declarant.
    for ctry in declarants:
        print('Working on {}'.format(ctry))
        t = datetime.utcnow()
        try:
            df = gmm.select('ctry_' + ctry)
            df = df.dropna()
            df = df[~(df == np.inf)]
            by_product = df.groupby(level='good')
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
        except:
            with open(base + 'failed_h5.txt', 'a') as f:
                f.write("Missed on {}".format(ctry))
        try:
            for_csv.to_csv('/Volumes/HDD/Users/tom/DataStorage/Comext/'
                           'yearly/new_ctry_{}.csv'.format(ctry))
        except:
            with open(base + 'failed_csv.txt', 'a') as f:
                f.write("Missed on {}".format(ctry))

        m = 'Finshed country {0} in {1}'.format(ctry, datetime.utcnow() - t)
        print(m)
        i += 1
        print('About {} done'.format(i / len(declarants)))
        # try:
        #     gmail.mail('thomas-augspurger@uiowa.edu', 'Test', m)
        # except:
        #     pass
