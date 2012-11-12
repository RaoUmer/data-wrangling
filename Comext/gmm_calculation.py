import pandas as pd
from weighting_matrix import weight_matrix as wm


def error():
    """
    u_gct = [delta^k * ln(p_gct)]**2 - theta_1 * (delta^k * ln(s_gct))**2 -
        theta_2 * (delta^k * ln(p_gct) * delta^k * ln(s_gct))

    Where
        theta_1 = w_g / ((1 + w_g)(sigma_g - 1))
        theta_2 = (1 - w_g(sigma_g - 2)) / ((1 + w_g)(sigma_g -1))
    """


def get_reference(store, country,
        years=['y2007', 'y2008', 'y2009', 'y2010', 'y2011']):
    """
    Finds potential countries to use as k in calculating errors.
    Must provide a positive quantity in every year. (Exports & Imports?)

    Read inside out to maintain sanity.  Would be so easy recursivly...
        Get index wm for first year possible (i.e. second year in sample).
        Filter by calling .ix on that index; drop the NaNs.  Take that index.
        ...
        End with index of (flow, good, partner) that works as references.

    Parameters:
    -----------
    store : HDF5Store
    country : String
    years: list of strings

    Returns:
    --------
    MultiIndex
    """

    return wm(store, country, years[4]).ix[
        wm(store, country, years[3]).ix[
        wm(store, country, years[2]).ix[
        wm(store, country, years[1]).index
        ].dropna().index
        ].dropna().index
        ].dropna().index



    # df[df.count(axis=1) == 5] gives the index
    # df.ix[df[df.count(axis=1) == 5]] gives values.
    store['quantity_' + country]