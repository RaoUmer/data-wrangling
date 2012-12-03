import pandas as pd

df = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Eurostat/ind_prod/sts_inpr_q.tsv',
    sep=",|s*\t", na_values=[':', ' :', ': '], index_col=['indic_bt', 'nace_r2', 's_adj', 'geo\\time'])

# Moves the quarters to the index and nace_r2 to the columns.
df2 = df.stack().unstack('nace_r2')
