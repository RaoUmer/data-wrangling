from __future__ import division

import os
from cPickle import load

import pandas as pd

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

with open('declarants_no_002_dict.pkl', 'r') as f:
    countries = load(f)

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/')
monthly = pd.HDFStore('monthly.h5')


def pct_chng(country, period):
    """ Gives the percentage change in each good's flow over.
    Aggregated from monthly over the quarterly.
    Parameters
    ----------
    country : string
    period : [int, int] [year, quarter]
        Everything is THIS year i.e. period[0] relative
        to last year: period[0] - 1. So period >= 2009

    returns: DataFrame. percentage change for each product.
    Notes
    -----
    Use this to generate the response variable for regression.
    Right now it's quite memory intensive (not paging out though)
    and takes ~10 seconds to run.
    """
    def months(q):
        """Quarter number to constituent months.
        """
        try:
            if q == 1:
                return ['jan', 'feb', 'mar']
            if q == 2:
                return ['apr', 'may', 'jun']
            if q == 3:
                return ['jul', 'aug', 'sep']
            if q == 4:
                return ['oct', 'nov', 'dec']
            else:
                raise
        except:
            print('Not a valid quarter. Enter 1, 2, 3, or 4')
            raise

    def op(p):
        """ Penultimate to calculating pct_chng. Pass
        period & [period[0] -1, period[1]].
        """
        gr1 = monthly[months(p[1])[0] + '_' + str(p[0])[-2:]].xs((country, 4), level=('DECLARANT', 'STAT_REGIME'))['VALUE_1000ECU'].groupby(level=['FLOW', 'PRODUCT_NC'])
        gr2 = monthly[months(p[1])[1] + '_' + str(p[0])[-2:]].xs((country, 4), level=('DECLARANT', 'STAT_REGIME'))['VALUE_1000ECU'].groupby(level=['FLOW', 'PRODUCT_NC'])
        gr3 = monthly[months(p[1])[2] + '_' + str(p[0])[-2:]].xs((country, 4), level=('DECLARANT', 'STAT_REGIME'))['VALUE_1000ECU'].groupby(level=['FLOW', 'PRODUCT_NC'])
        # Put in dict and mean to avoid excess na's.
        d = {
            months(period[1])[0]: gr1.sum(),
            months(period[1])[1]: gr2.sum(),
            months(period[1])[2]: gr3.sum()}

        return pd.DataFrame(d).mean(axis=1)

    df1 = op(period)
    df2 = op([period[0] - 1, period[1]])

    d = {
        period[0]     : df1,
        period[0] - 1 : df2}

    df = pd.DataFrame(d)
    return (df[period[0]] - df[period[0] - 1]) / df[period[0] - 1]
