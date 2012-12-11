import os
import datetime as dt

import numpy as np
import pandas as pd

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Eurostat/ind_prod_store/')
prod = pd.read_csv('ind_prod_clean.csv', index_col=['time', 'geo'])

prod.index.levels[0] = pd.DatetimeIndex(prod.index.levels[0])

"""
Just some notes
test = prod.xs('AT', level='geo')[['B', 'C', 'D']]
test.ix['2007-03-01':'2012-09-01'].pct_change(4)
"""
