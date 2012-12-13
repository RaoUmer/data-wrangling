import os
import string
from cPickle import load, dump
import datetime as dt

import numpy as np
import pandas as pd

"""
Data are indexed uniquely by (time, geo) pairs.
*Columns are according to NACE rev 2.* No info on seasonal adj.f
Probably want to look at 2007Q2 - 2008Q2 for most everything.

I need to decide if my predictor is percent change in ind_prod or
just the change in ind_prod.  It seems to be indexed at 0 rather
than 100 so does pct_change make sense?  Telling different stories.
"""

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Eurostat/ind_prod_store/')
pr = pd.read_csv('ind_prod_clean.csv', index_col=['time', 'geo'])


pr.index.levels[0] = pd.DatetimeIndex(pr.index.levels[0])
pr = pr.sortlevel()

# Calculate the absolute change in the index by country:

gr = pr.ix['2006-03-01':].groupby(axis=0, level='geo')
res = gr.apply(lambda x: x - x.shift(4))

# Helper to get the largest decline. Not working with groupby though.
res.apply(lambda x: x.index[x.dropna().argmin()])

### Testing
# Just some notes
test = pr.xs('AT', level='geo')[['B', 'C', 'D']]
test.ix['2007-03-01':'2012-09-01'].pct_change(4)

pr2 = pd.read_csv('ind_prod_clean.csv')

for ctry in pr.index.levels[1]:
    plt.figure()
    pr.xs(ctry, level='geo')['C'].plot(label=ctry, legend=True)



# Cleaning NACE_rev2_dic.txt
os.chdir('/Volumes/HDD/Users/tom/DataStorage/Eurostat/correspondences')
f = open('nace_r2_dic.txt', 'r')
l = [x.split('\t') for x in f.readlines()]
f.close()

d = {k: v.rstrip('\r\n') for k, v in l}
out = open('nace_r2_dict.pkl', 'w')
dump(d, out, protocol=2)

with open('/Volumes/HDD/Users/tom/DataStorage/Eurostat/correspondences/nace_r2_dict.pkl', 'r') as f:
    d = load(f)
