from __future__ import division

import os
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
            unit_p = 0
            return unit_p
        else:
            unit_p = df[col1] / df[col3]
            return unit_p
    else:
        unit_p = df[col1] / df[col2]
        return unit_p
    return unit_p


os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

yearly = pd.HDFStore('yearly.h5')

# for       [FLOW       , PERIOD,      PRODUC_NC, DECLARANT,  PARTNER]
# Types are [numpy.int64, numpy.int64, str,     , str,        numpy.int64]


keys = ['y2007', 'y2008', 'y2009', 'y2010', 'y2011']


for df in keys:
        yearly[df + '_price'] = yearly[df].apply(unit_price, axis=1)
        print "Done with %s" % df

print 'All Done'
yearly.close()
