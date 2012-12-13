import os

import cPickle
import pandas as pd

"""
Load with:
os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/correspondences/excel_correspondences')
with open('new_cn12_to_pc11', 'r') as f:
    d_cn_pc = cPickle.load(f)

"""
os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/correspondences/excel_correspondences')

xls = pd.ExcelFile('CN 2011 - PRODCOM 2011.xls')
df = xls.parse(xls.sheet_names[0], index_col=None, header=None, skiprows=4)

df.columns = ['year', 'pd', 'cn', 'comment']

t = df['cn']
len(t.unique())  # = 9292 Counts one np.nan.
sum(pd.notnull(t))  # = 9291

# So CN2011 is my unique key here.
df['cn'].dropna()
df2 = df.reindex(df['cn'].dropna().index)
df2 = df2.set_index('cn')

d = df2['cn'].to_dict()
out = open('new_cn_to_pd.pkl', 'w')
cPickle.dump(d, out, protocol=2)
out.close()

#################################

xls = pd.ExcelFile('CN 2012 - CN 2011.xls')
df = xls.parse(xls.sheet_names[0], index_col=None, skiprows=4, na_values='-')

df.columns = ['cn12', 'q', 'cn11']

t = df['cn12']
len(t.unique())  # = 1049 Counts one np.nan.
sum(pd.notnull(t))  # = 1443

"""
So no unique key here.  Some of the sections are being partially transfered,
curried if you will.  Plan is to take those nonuniques are limit to first?
I don't have anything to average at this point.
Ahh I love pandas.  Does that by default (should probably have a warning
though.
"""

df2 = df.set_index('cn12')

d = df2['cn11'].to_dict()
out = open('new_cn12_to_cn11.pkl', 'w')
cPickle.dump(d, out, protocol=2)
out.close()

##################################
# The final dict: cn12 -> cn11 -> prodcom11

f1 = open('nace_intermediate_dict.pkl', 'r')
f2 = open('new_cn_to_pd.pkl', 'r')
cc = cPickle.load(f1)
cp = cPickle.load(f2)
d = {i:cp[cc[s]] for i in cc}

out = open('new_cn12_to_pc11', 'w')
cPickle.dump(d, out, protocol=2)
