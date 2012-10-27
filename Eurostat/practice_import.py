from __future__ import division


import pandas as pd

df = pd.read_csv(
    '/Volumes/HDD/Users/tom/DataStorage/Eurostat/namq_gdp_c/namq_gdp_c_1_Data.csv',
    index_col=[1, 0], parse_dates=True, na_values=':', thousands=',')

"""
This dataFrame will be multi-indexed with quaters on the outer index
and countries on the inner index. The data in this case is exports
non-seasonally-adjusted, percentage of GDP.
"""
df = df.drop(['UNIT', 'INDIC_NA', 'S_ADJ'], axis=1)
df = df.rename(columns={'Value': 'Exports'})

"""
The below is older code, keeping around for examples.

exports_pcgdp_nsa = df[['GEO', 'TIME', 'Value']]


geo = df['GEO'].unique()
for country in geo:
    df[country] = np.zeros(len(df))

x = ['GEO', 'TIME', 'Value']
for i, country in enumerate(df['GEO']):
    df[country][np.floor(i / 32)] = df['Value'][i]

del df['GEO']
del df['Value']
df.index = pd.TimeSeries(df.TIME)
del df['TIME']
df = df.rename(columns={
    'Germany (including  former GDR from 1991)': 'Germany'})

subset = ['Belgium', 'Germany', 'Spain', 'France']
"""
