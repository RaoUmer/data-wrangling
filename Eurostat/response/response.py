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

    returns: Series. percentage change for each product.
    Example: res = pct_chng('001', [2009, 2])

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

    def op(p, trim=True):
        """ Penultimate to calculating pct_chng. Pass
        period & [period[0] -1, period[1]].  Currently only supports imports.
        """
        gr1 = monthly[months(p[1])[0] + '_' + str(p[0])[-2:]].xs((1, country, 4), level=('FLOW', 'DECLARANT', 'STAT_REGIME'))['VALUE_1000ECU']
        gr2 = monthly[months(p[1])[1] + '_' + str(p[0])[-2:]].xs((1, country, 4), level=('FLOW', 'DECLARANT', 'STAT_REGIME'))['VALUE_1000ECU']
        gr3 = monthly[months(p[1])[2] + '_' + str(p[0])[-2:]].xs((1, country, 4), level=('FLOW', 'DECLARANT', 'STAT_REGIME'))['VALUE_1000ECU']

        p1 = gr1.index.levels[0][0]
        p2 = gr2.index.levels[0][0]
        p3 = gr3.index.levels[0][0]
        if trim:
            idx1 = [x for x in gr1.index.levels[1] if len(x) == 8]
            idx2 = [x for x in gr2.index.levels[1] if len(x) == 8]
            idx3 = [x for x in gr3.index.levels[1] if len(x) == 8]

            gr1 = gr1.ix[p1].ix[idx1]
            gr2 = gr2.ix[p2].ix[idx2]
            gr3 = gr3.ix[p3].ix[idx3]

            def fil(x):
                if x[1] < 1000:
                    return True
                else:
                    return False

            gr1 = gr1[map(fil, gr1.index)]
            gr2 = gr2[map(fil, gr2.index)]
            gr3 = gr3[map(fil, gr3.index)]
        # Put in dict and mean to avoid excess na's.
        d = {
            months(period[1])[0]: gr1.groupby(level=['PRODUCT_NC']).sum(),
            months(period[1])[1]: gr2.groupby(level=['PRODUCT_NC']).sum(),
            months(period[1])[2]: gr3.groupby(level=['PRODUCT_NC']).sum()}

        return pd.DataFrame(d).mean(axis=1)

    df1 = op(period)
    df2 = op([period[0] - 1, period[1]])
    ind = df1[df1 > 0].index.intersection(df2[df2 > 0].index)
    d = {
        period[0]: df1[ind],
        period[0] - 1: df2[ind]}

    df = pd.DataFrame(d)
    return (df[period[0]] - df[period[0] - 1]) / df[period[0] - 1]
