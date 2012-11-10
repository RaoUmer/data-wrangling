from __future__ import division

import os
import pandas as pd
from helpers import unit_price

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
if os.getcwd() != '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly':
    print 'You\'re in the wrong directory'

yearly = pd.HDFStore('yearly.h5')

files = [
        'nc200752',
        'nc200852',
        'nc200952',
        'nc201052',
        'nc201152',
]

lookup = {
        'nc200752': 'y2007',
        'nc200852': 'y2008',
        'nc200952': 'y2009',
        'nc201052': 'y2010',
        'nc201152': 'y2011',
}

# for       [FLOW       , PERIOD,      PRODUC_NC, DECLARANT,  PARTNER]
# Types are [numpy.int64, numpy.int64, str,     , str,        numpy.int64]

for df in yearly.keys():
        yearly[df + '_price'] = yearly[df].apply(unit_price, axis=1)
        print "Done with %s" % df

print 'All Done'
yearly.close()
