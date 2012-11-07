import subprocess
import os
from year_month_parse import year_month

import pandas as pd


"""
A one-off script to covert a list of 7z Archives to a single
pandas-PyTables HDFStore.  Could be refactored to take
the directory containing the files to be decompressed,
but I'm not going to worry about that right now.
"""

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/')
files = [
        'nc200801',
        'nc200802',
        'nc200803',
        'nc200804',
        'nc200805',
        'nc200806',
        'nc200807',
        'nc200808',
        'nc200809',
        'nc200810',
        'nc200811',
        'nc200812',
        'nc200901',
        'nc200902',
        'nc200903',
        'nc200904',
        'nc200905',
        'nc200906',
        'nc200907',
        'nc200908',
        'nc200909',
        'nc200910',
        'nc200911',
        'nc200912',
        'nc201001',
        'nc201002',
        'nc201003',
        'nc201004',
        'nc201005',
        'nc201006',
        'nc201007',
        'nc201008',
        'nc201009',
        'nc201010',
        'nc201011',
        'nc201012',
]

z7 = '.7z'
dat = '.dat'

# cmd = ['7z', 'e']
# for f in files:
#     subprocess.call(cmd + [f + z7])

comext = pd.HDFStore('comext.h5')
lookup = {
        'nc200801': 'Jan2008',
        'nc200802': 'Feb2008',
        'nc200803': 'Mar2008',
        'nc200804': 'Apr2008',
        'nc200805': 'May2008',
        'nc200806': 'Jun2008',
        'nc200807': 'Jul2008',
        'nc200808': 'Aug2008',
        'nc200809': 'Sep2008',
        'nc200810': 'Oct2008',
        'nc200811': 'Nov2008',
        'nc200812': 'Dec2008',
        'nc200901': 'Jan2009',
        'nc200902': 'Feb2009',
        'nc200903': 'Mar2009',
        'nc200904': 'Apr2009',
        'nc200905': 'May2009',
        'nc200906': 'Jun2009',
        'nc200907': 'Jul2009',
        'nc200908': 'Aug2009',
        'nc200909': 'Sep2009',
        'nc200910': 'Oct2009',
        'nc200911': 'Nov2009',
        'nc200912': 'Dec2009',
        'nc201001': 'Jan2010',
        'nc201002': 'Feb2010',
        'nc201003': 'Mar2010',
        'nc201004': 'Apr2010',
        'nc201005': 'May2010',
        'nc201006': 'Jun2010',
        'nc201007': 'Jul2010',
        'nc201008': 'Aug2010',
        'nc201009': 'Sep2010',
        'nc201010': 'Oct2010',
        'nc201011': 'Nov2010',
        'nc201012': 'Dec2010',
}


for f in files:
    leaf = lookup[f]
    comext[leaf] = pd.read_csv(f + dat, parse_dates=[5],
        date_parser=year_month)
    print 'Added %s' % leaf
