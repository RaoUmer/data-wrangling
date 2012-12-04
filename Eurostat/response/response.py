import os
from cPickle import load

import pandas as pd

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

with open('declarants_no_002_dict.pkl', 'r') as f:
    countries = load(f)

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/')
monthly = pd.HDFStore('monthly.h5')


def pct_chng(country, period):
    """ Gives the percentage change in each good's flow.
    country : string
    quarter : [int, int] [year, quarter]

    returns: DataFrame. percentage change for each product.
    """
    def months(q):
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

        d = {
            months(period[1])[0]: gr1.sum(),
            months(period[1])[1]: gr2.sum(),
            months(period[1])[2]: gr3.sum()}

        return pd.DataFrame(d).mean(axis=1)

    df1 = op(period)
    df2 = op([period[0] - 1, period[1]])

    d = {
        period[0]    : df1,
        period[0] -1 : df2}

    df = pd.DataFrame(d)
    return d.mean(axis=1)

