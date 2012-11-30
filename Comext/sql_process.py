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
df1_i = gmm['s_001'].head(50)
df2_i = gmm['p_001'].head(50)

df1.reset_index(inplace=True)
df2.reset_index(inplace=True)
# call(["sqlite3", "test.db"])
# .quit
con = lite.connect('test.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS df")
    cur.execute("DROP TABLE IF EXISTS df2")

sql.write_frame(df1, name='df1', con=con)
sql.write_frame(df2, name='df2', con=con)

con.commit()
# Columns: (PRODUCT_NC, PARTNER, s_2008, s_2009, s_2010, s_2011)
#          (PRODUCT_NC, PARTNER, p_2008, p_2009, p_2010, p_2011)


################
# Join in sqlite
################

# CURRENTLY STACKING.
"""
'SELECT df1.PRODUCT_NC, df1.PARTNER, df1.s_2008 FROM df1 LEFT OUTER JOIN df2 ON (df1.PRODUCT_NC = df2.PRODUCT_NC AND df1.PARTNER = df2.PARTNER)
UNION
SELECT df2.PRODUCT_NC, df2.PARTNER, df2.p_2008 FROM df2 LEFT OUTER JOIN df1 ON (df1.PRODUCT_NC = df2.PRODUCT_NC AND df1.PARTNER = df2.PARTNER);'
"""

query = '''SELECT df1.PRODUCT_NC, df1.PARTNER, df1.s_2008 FROM df1 LEFT OUTER JOIN df2 ON (df1.PRODUCT_NC = df2.PRODUCT_NC AND df1.PARTNER = df2.PARTNER)
            UNION
            SELECT df2.PRODUCT_NC, df2.PARTNER, df2.p_2008 FROM df2 LEFT OUTER JOIN df1 ON (df1.PRODUCT_NC = df2.PRODUCT_NC AND df1.PARTNER = df2.PARTNER);'''

read_frame(query, con)


"""
SELECT PRODUCT_NC, PARTNER, s_2008, s_2009, s_2010, s_2011, p_2008, p_2009, p_2010, p_2011
FROM df1 JOIN df2
ON (df1.PRODUCT_NC = df2.PRODUCT_NC AND df1.PARTNER = df2.PARTNER);

"""