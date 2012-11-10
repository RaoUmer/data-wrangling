import os
import pandas as pd

""""
Stuff here for working the 7z files to dats.

Assume done
"""
os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')

files = [
        'nc200752',
        'nc200852',
        'nc200952',
        'nc201052',
        'nc201152',
]

z7 = '.7z'
dat = '.dat'

yearly = pd.HDFStore('yearly.h5')
lookup = {
        'nc200752': 'y2007',
        'nc200852': 'y2008',
        'nc200952': 'y2009',
        'nc201052': 'y2010',
        'nc201152': 'y2011',
}

'''
Index will be FLOW, PERIOD, PRODUCT_NC, DECLARANT, PARTNER.
              3,    5,      2,          0,         1.
'''
# Not Working with the parser/multiIndex.
# def year(x):
#     y = int(str(x)[:4])
#     return dt.datetime(y, 01, 1)


for f in files:
    leaf = lookup[f]
    yearly[leaf] = pd.read_csv(f + dat,
        index_col=['FLOW', 'PERIOD', 'PRODUCT_NC', 'DECLARANT', 'PARTNER'])
    print 'Added %s' % leaf
