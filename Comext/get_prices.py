from __future__ import division

import os
from cPickle import load
from datetime import datetime as dt

import numpy as np
import pandas as pd


def unit_price(df, col1='VALUE_1000ECU', col2='QUANTITY_TON',
                                        col3='SUP_QUANTITY'):
    """
    Calculate the unit price estimate for each good.
    Use with df.apply, axis=1.

    Parameters
    ----------
    df: Pandas dataFrame.
    col1: Total Valaue of item.
    col2: First measure of weight.
    col3: Second measure of weight.

    Returns
    -------
    Pandas Series.  Set to unit_price column in df.
    """
    if df[col2] == 0:
        if df[col3] == 0:
            return np.nan
        else:
            return df[col1] / df[col3]
    else:
        return df[col1] / df[col2]


os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

yearly = pd.HDFStore('yearly.h5')
with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)


# for       [FLOW       , PERIOD,      PRODUC_NC, DECLARANT,  PARTNER]
# Types are [numpy.int64, numpy.int64, str,     , str,        numpy.int64]

keys = ['y2007', 'y2008', 'y2009', 'y2010', 'y2011']
start_time = dt.now()
failures = []

for df in keys:
    iyear = int(df.strip('y') + '52')
    for declarant in sorted(declarants):
        try:
            temp_df = yearly[df].xs((1, iyear, declarant), level=(
                'FLOW', 'PERIOD', 'DECLARANT'))
            yearly[df + '_price_' + declarant] = temp_df[temp_df['STAT_REGIME'] == 4].apply(unit_price, axis=1)
            print("Done with %s, %s" % (df, declarant))
            print(dt.now() - start_time)
        except:
            print('Failed on %s, %s' % (df, declarant))
            failures.append((df, declarant))
    print('All done with %s' % df)
    print(dt.now() - start_time)

print 'All Done'
yearly.close()
