"""
We have the results from GMM.  Now we want to transform
those parameter estimates into values for sigma and rho,
the import demand and export supply elasticities.
"""
import numpy as np
import pandas as pd


def _theta_to_interest(estimated_params):
    """
    GMM estimates theta1 and theta2, we want sigma and omega.

    See Broda and Weinstein's working paper for this derivation.
    Call like c1.apply(_theta_to_interest, axis=1, broadcast=True)
    """
    t1, t2 = estimated_params
    if t1 > 0 and t2 > 0:
        rho = .5 + (.25 - (1 / (4 + t2 / t1))) ** .5
        sigma = 1 + (1 / t2) * (2 * rho - 1) / (1 - rho)
    elif t1 > 0 and t2 < 0:
        rho = .5 - (.25 - (1 / (4 + t2 / t1))) ** .5
        sigma = 1 + (1 / t2) * (2 * rho - 1) / (1 - rho)
    elif t1 < 0:
        rho = np.nan
        sigma = np.nan
    return (sigma, rho)

if __name__ == '__main__':
    from cPickle import load
    from datetime import datetime

    base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
    gmm_results = [pd.HDFStore(base + 'gmm_results_weighted.h5'),
                   pd.HDFStore(base + 'gmm_results.h5')]

    with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
        country_code = load(declarants)
        declarants = sorted(country_code.keys())
#-----------------------------------------------------------------------------
# Main loop.
    for j, store in enumerate(gmm_results):
        for i, ctry in enumerate(declarants):
            try:
                df = store.select('res_' + ctry)
            except KeyError:
                continue
            trans = df.apply(_theta_to_interest, axis=1, broadcast=True)
            store.append('transformed_' + ctry, trans)
            print('Added {}'.format(ctry))
