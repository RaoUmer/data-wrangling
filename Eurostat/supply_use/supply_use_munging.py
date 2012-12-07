from __future__ import division

import os
import pandas as pd

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Eurostat/supply_use_tables/')
df = pd.read_csv('naio_cp15_r2.tsv',
        na_values=[':', ' :', ': ', ': c'], sep=',|s*\t',
        index_col=['unit', 'geo\\time', 't_cols2', 't_rows2'])
# ,|s* is a regex to find a comma OR arbitrary white space then tab.
# I don't think na_vavlues takes regex's.
# WARNING: Some provisionals stripped.

df.columns = [int(x.strip(' ')) for x in df.columns]
df.index.names = ['unit', 'geo', 'industry', 'input']
df = df.astype('float')
df.to_csv('clean_naio_cp15_r2.csv')
