import cPickle

import pandas as pd

gmm_store = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
                        'yearly.h5')

with open('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
          'declarants_no_002_dict.pkl', 'r') as declarants:
    country_code = cPickle.load(declarants)
declarants = sorted(country_code.keys())
years = [2007, 2008, 2009, 2010, 2011]
ctry = '001'
df = gmm_store['y' + year + '_' + ctry]
df = df.reset_index()
df = df.rename(columns={'FLOW': 'flow',
                        'PERIOD': 'period',
                        'PRODUCT_NC': 'product',
                        'PARTNER': 'partner',
                        'STAT_REGIME': 'stat',
                        'VALUE_1000ECU': 'value',
                        'QUANTITY_TON': 'quantity',
                        'SUP_QUANTITY': 'sup_quantity'})
df['period'] = df.period.apply(lambda x: int(str(x)[:4]))
df = df.set_index(['flow', 'period', 'product', 'partner', 'stat'])
