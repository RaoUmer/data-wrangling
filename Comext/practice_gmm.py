from __future__ import division

import os

import pandas as pd

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
gmm = pd.HDFStore('gmm_store.h5')

df = gmm['f_001'].dropna(how='all')
gr = df.groupby(axis=0, level='PRODUCT_NC')

# df1 is used for gmm
df1 = gr.get_group('01')[['s_2008', 'p_2008', 'c_2008']].dropna()
