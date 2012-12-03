from __future__ import division

import os

import pandas as pd

# May want to get df1 below and write those as an HDF5 store,
# so 1 for each (country, product) tuple.
os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
gmm = pd.HDFStore('gmm_store.h5')

df = gmm['f_001'].dropna(how='all')
gr = df.groupby(axis=0, level='PRODUCT_NC')

# df1 is used for gmm
df1 = gr.get_group('01')[['s_2008', 'p_2008', 'c_2008']].dropna()
