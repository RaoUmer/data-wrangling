from __future__ import division

import os
import pandas as pd

"""
may want df.ix[(1, year):(2, year)]
"""

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')

country_code = {
            '001': 'France',
            '002': 'Belg.-Luxbg',
            '003': 'Netherlands',
            '004': 'Fr Germany',
            '005': 'Italy',
            '006': 'Utd. Kingdom',
            '007': 'Ireland',
            '008': 'Denmark',
            '009': 'Greece',
            '010': 'Portugal',
            '011': 'Spain',
            '017': 'Belgium',
            '018': 'Luxembourg',
            '030': 'Sweden',
            '032': 'Finland',
            '038': 'Austria',
            '600': 'Cyprus',
            '061': 'Czech Republic',
            '053': 'Estonia',
            '064': 'Hungary',
            '055': 'Lithuania',
            '054': 'Latvia',
            '046': 'Malta',
            '060': 'Poland',
            '091': 'Slovenia',
            '063': 'Slovakia',
            '068': 'Bulgaria',
            '066': 'Romania',
            'EU': 'EU',
}

keys = sorted(country_code.keys())

for leaf in yearly.keys():
    for key in keys:
        try:
            yearly[leaf + key] = yearly[leaf].xs(key, level='DECLARANT')
            print 'done with %s, %s' % (leaf, key)
        except:
            print 'Trouble with %s, %s' % (leaf, key)
    print 'All done with %s' % leaf
