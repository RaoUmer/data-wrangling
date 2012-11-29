from __future__ import division

import os
import sys
import sqlite3 as lite
from subprocess import call

import pandas as pd
from pandas.io import sql as sql

"""
Takes as give an HDFStore with two leaves for each country:
one for shares, one for prices.  Moves these to a sqlite table
and joins them.
"""

##### Testing #####
os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
gmm = pd.HDFStore('gmm_store.h5')
df = gmm['s_001'].head(500)
df2 = gmm['s_001'].head(500)

df.reset_index(inplace=True)
df2.reset_index(inplace=True)
call(["sqlite3", "test.db"])
# .quit
con = lite.connect('test.db')

with con:
    cur = con.cursor()

sql.write_frame(df, name='df', con=con)
sql.write_frame(df2, name='df2', con=con)

# Columns: (PRODUCT_NC, PARTNER, s_2008, s_2009, s_2010, s_2011)



################
# Join in sqlite
################

SELECT * from df as S JOIN 