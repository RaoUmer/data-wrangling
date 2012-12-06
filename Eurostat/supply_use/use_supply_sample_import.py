import pandas as pd

df = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Eurostat/supply_use_tables/naio_cp15_r2.tsv',
        na_values=[':', ' :', ': '], sep=',|s*\t',
        index_col=['unit', 'geo\\time', 't_cols2', 't_rows2'], nrows=4000)
# ,|s* is a regex to find a comma OR arbitrary white space then tab.
# I don't think na_vavlues takes regex's.

"""
Want to reproduce the table:
            Industries
           _______________________________________
 commodity|                  |      | Total
          |                  |      | Commodity
          |                  | Final| Output
          |                  | Uses |
          |                  |      |
          ----------------------------------------
          |    Value Added   | GDP  |
          ----------------------------------------
          | Total Ind Output |      | Total Output

But to deal with years we'll throw it out the outside axis
so a .ix[2008] will give that table.

Really only going to use 2008.  Lot's of nans elsewhere.

Note on indicies: "the first four digits are the classification of the
producing enterprise given by the Statistical Classification of Economic
Activities in the European Community (NACE) and the first six correspond
to the CPA.

"""

df.columns = [(x.strip(' ')) for x in df.columns]
df.index.names = ['unit', 'geo', 'industry', 'input']
df2 = df[2008]

# Gives the table for (unit, country) pairs. Work with this.
df2 = df2.unstack(level='industry')
gr = df2.groupby(axis=0, level='geo')