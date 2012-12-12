import pandas as pd

xls = pd.ExcelFile('CN 2011 - PRODCOM 2011.xls')
df = xls.parse(xls.sheet_names[0], index_col=None, header=None, skiprows=4)

df.columns = ['year', 'pd', 'cn', 'comment']

t = df['cn']
len(t.unique)  # = 9292
sum(pd.notnull(t))  # = 9291 ummm, is this a zero index thing?
