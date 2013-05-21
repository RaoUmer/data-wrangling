"""
You have a df like:
                          'p', s, c
year, partner, product ||


GMM go!
"""
from __future__ import division, print_function, unicode_literals

import pdb

import numpy as np
import pandas as pd
from scipy import optimize
from scipy import dot

# import gmail
# from outliers_after_weighting import pre
from parse_optimize_results import opt_dict_format
#-----------------------------------------------------------------------------
# Functions for the GMM.


def _theta_to_interest(t1, t2):
    """
    GMM estimates theta1 and theta2, we want sigma and omega.
    """
    pass


def gen_moms_sse(theta, subgroup, bias_term, W=None):
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
    if W is None:
        # Naiive case.  Doesn't weight, doesn't add that term on p. 583.
        err = p - theta[0] * s - theta[1] * c
        W = np.eye(len(err))
    else:
        err = p - theta[0] * s - theta[1] * c - bias_term
    return dot(dot(err.T, W), err) / len(err)


def gen_params(subgroup, x0, name, method='Nelder-Mead', W=None, country=None,
               options={'disp': False}):
    """Currently at year, partner index. subgroup = grp
    Higher level function called by user to estimate parameters via GMM.
    Pass off to scipy.optimizize.

    Parameters
    ----------
    subgroup: A DataFrame from a groupby(level='good')
    x0: list. Initial guess at parameters for that good.
    name: str. The good that subgroup is associated with.
    method: str.  Optimization routine to use. See scipy.optimize.minimize.
    W: Bool: Whether to solve for the weighting matrix. Default No.
    country: Necessary if W is True.  Used to lookup data for weighitng matrix.
    options: Display options to pass to minimize.

    Returns
    -------
    Bubbles up results from minimize, except fills in nans where appropriate.
    """
    subgroup.name = name  # Side-effectual.
    if W:
        # pdb.set_trace()
        # Calculate the Weighting Matrix.  Uses quantity data.
        # pdb.set_trace()
        with pd.get_store(base + 'by_declarant.h5') as q_store:
            weight_data = q_store.select('ctry_' + country,
                                         pd.Term('good == {}'.format(subgroup.name)))
        # Get like indexed and then remove non-intersection
        # weight_data.index = weight_data.index.droplevel('good')  # TODO: Check this
        weight_data = weight_data.ix[subgroup.index]
        diffed = weight_data.quantity.groupby(level='partner').apply(diff_q)
        bias_term = diffed.mean()  # Need to multiply by estimate of var(ln(error))
        W = weight_matrix(subgroup, diffed, weight_data)
    else:
        bias_term = 0
    try:
        return optimize.minimize(gen_moms_sse, x0=x0,
                                 args=[(subgroup.values.T), bias_term, W],
                                 method=method, options=options)
    except AttributeError:
        print('Failed On frame {}'.format(subgroup.name))
        return (np.nan, np.nan)


def diff_q(x):
    """
    Find 1/q_gct + 1/g_gct-1
    """
    return ((1 / x) + (1 / x.shift())).fillna(method='bfill')


def fit_one(pre=None, ctry=None):
    """
    Similar to gen_params (earlier anyway).  Fits for a single country.
    """
    if pre is None:
        pre = load_pre(ctry)
    by_product = pre.dropna().groupby(level='PRODUCT_NC')
    res = {name: gen_params(group, x0=[2, 1]) for name, group in by_product}
    res = pd.DataFrame(res).T
    for_csv, for_hd5 = opt_dict_format(res, names=['t1', 't2'])
    return (for_csv, for_hd5)


def weight_matrix(group, diffed, weight_data):
    """
    Used to generate optimal value to be passed into the optimization.
    See Broda and Weinstein 2006 p. 584.

    ROBUSTNESS CHECK: Introduce some nans which I fill with the mean.
    ROBUSTNESS CHECK:  We diff with the prior period here.  B&W say nothing
    about what they do with the initial period.  I just fill in from the
    second period.
    """
    t0 = group.irow(0).name[0]
    tn = group.irow(-1).name[0]
    T = tn - t0 + 1
    res = T**(3/2) * diffed ** -(1/2)
    res[pd.isnull(res)] = res.mean()
    return np.outer(res, res)
#-----------------------------------------------------------------------------

if __name__ == '__main__':
    from cPickle import load
    from datetime import datetime

    base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
    gmm = pd.HDFStore(base + 'filtered_for_gmm.h5')
    gmm_results = pd.HDFStore(base + 'filtered_gmm_results_weighted.h5')
    with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
        country_code = load(declarants)
    declarants = sorted(country_code.keys())
#-----------------------------------------------------------------------------
# Main loop.  Optimize to get params for each good, for each declarant.
    for i, ctry in enumerate(declarants):
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
        #---------------------------------------------------------------------
        # GMM Estimation.
        # Without Weighting
        # res = {name: gen_params(group, [2, 1], name, country=ctry, W=None)
        #        for name, group in by_product}
        #---------------------------------------------------------------------
        # With Weighting
        res = {name: gen_params(
            group, [2, 1], name, country=ctry, W=True, options={'disp': False})
            for name, group in by_product}
        print('Finshed estimation for {}'.format(ctry))
        #---------------------------------------------------------------------
        # Formatting and IO.
        res = pd.DataFrame(res).T
        for_csv, for_hd5 = opt_dict_format(res, names=['t1', 't2'])
        try:
            gmm_results.append('res_' + ctry, for_hd5)
        except:
            with open(base + 'failed_h5.txt', 'a') as f:
                f.write("Missed on {}".format(ctry))
            res.to_csv('/Volumes/HDD/Users/tom/DataStorage/Comext/'
                       'yearly/new_ctry_{}_weighted.csv'.format(ctry))
        # try:
        #     for_csv.to_csv('/Volumes/HDD/Users/tom/DataStorage/Comext/'
        #                    'yearly/new_ctry_{}_weighted.csv'.format(ctry))
        # except:
        #     with open(base + 'failed_csv.txt', 'a') as f:
        #         f.write("Missed on {}".format(ctry))

        m = 'Finshed country {0} in {1}'.format(ctry, datetime.utcnow() - t)
        print(m)
        i += 1
        print('About {} done'.format(i / len(declarants)))
