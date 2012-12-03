import os
from cPickle import load
from datetime import datetime as dt

import pandas as pd

"""
Will take as given
    -monthly HDFstore indexed as ['FLOW', 'PERIOD', 'DECLARANT',
        'PRODUCT_NC', 'PARTNER', 'STAT_REGIME']

Will return a series with percentage changes in the value of
    exports or imports indexed as
    [country, flow?, date, product]
"""
start_time = dt.now()

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')
size_control = pd.HDFStore('size_control.h5')
with open('declarants_no_002_dict.pkl', 'r') as f:
    countries = load(f)

years = ['2007', '2008', '2009', '2010', '2011']
for country in countries:
    for year in years:
        if year == '2007':
            print('starting %s') % year
            df = yearly['y' + year + '_' + country]
            df = df[df['STAT_REGIME'] == 4]

            gr = df.groupby(axis=0, level='PRODUCT_NC')
            ret = pd.DataFrame(gr['VALUE_1000ECU'].sum() / (
                gr['VALUE_1000ECU'].sum().tail(1).values))
            print('done with %s') % year
        else:
            print('starting %s') % year
            df = yearly['y' + year + '_' + country]
            df = df[df['STAT_REGIME'] == 4]

            gr = df.groupby(axis=0, level='PRODUCT_NC')

            if type(ret) == pd.core.series.Series:
                ret = pd.DataFrame(ret)

            ret = ret.join(gr['VALUE_1000ECU'].sum() / (
                gr['VALUE_1000ECU'].sum().tail(1).values), how='outer', rsuffix=year)
            print('done with %s') % year
        size_control['c' + country] = ret.mean(axis=1)
    print('done with %s in') % country
    print(dt.now() - start_time)

# ret should .sum() to about 3 since each item is counted 3x: 1 dig; 2 dig; tot


################################
## Testing
################################
# Not straight application since I use TOTAL above (last rows)
# df = yearly['y2011_001'].head(500)
# df = df[df['STAT_REGIME'] == 4]

# gr = df.groupby(axis=0, level='PRODUCT_NC')
# ret = gr['VALUE_1000ECU'].sum() / gr['VALUE_1000ECU'].sum().sum()

# df2 = yearly['y2010_001']
# df2 = df2[df2['STAT_REGIME'] == 4]

# gr2 = df2.groupby(axis=0, level='PRODUCT_NC')
# ret2 = gr2['VALUE_1000ECU'].sum() / gr2['VALUE_1000ECU'].sum().tail(1).values
