import os
import cPickle

import pandas as pd

"""
I've moved the resulting pickles for convinience
TO LOAD:
with open('cn11-prodcom11.pkl', 'r') as f:
    cn11_pd11 = cPickle.load(f)

with open('cn12-cn11.pkl', 'r') as f:
    cn12_cn11 = cPickle.load(f)


Trade data uses CN 2012.

Ind_prod is in NACE rev.

CN has a cors. with PRODCOM 2011.  Prodcom <- CPA <- NACE
Need CN2012->CN2011->PRODCOM2011 <- NACE
"""
os.chdir('ind_prod_store/cn11-cn12/')
xls = pd.ExcelFile('CN 2011 - CN 2012.xls')
df = xls.parse(xls.sheet_names[0], index_col=None, skiprows=4)
df.index = df['CN 2012']
del df['Unnamed: 1'], df['CN 2012']

d = df.to_dict()[df.columns[0]]
os.chdir('ind_prod_store/cn11-cn12/')

out = open('cn12-cn11.pkl', 'w')
cPickle.dump(d, out, 2)
out.close()

################### CN2011 - PRODCOM11
os.chdir('../prodcom11-cn11')
xls = pd.ExcelFile('CN 2011 - PRODCOM 2011.xls')
df = xls.parse(xls.sheet_names[0], index_col='CN2011')
del df['Year']

d = df.to_dict()[df.columns[0]]
out = open('cn11-prodcom11.pkl', 'w')
cPickle.dump(d, out, 2)
out.close()

################################################
# The final dict: Compose cn12 -> cn11 & cn11 -> prodcom11
d = {i: cn11_pd11[cn12_cn11[i]] for i in cn12_cn11}
out = open('CN-PD.pkl', 'w')
cPickle.dump(d, out, 2)
out.close()
