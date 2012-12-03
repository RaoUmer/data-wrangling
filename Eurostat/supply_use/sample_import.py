import pandas as pd

df = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Eurostat/supply_use_tables/naio_cp15_r2.tsv',
        na_values=[':', ' :', ': '], sep=',|s*\t',
        index_col=['unit', 't_cols2', 't_rows2', 'geo\\time'], nrows=10)
# ,|s* is a regex to find a comma OR arbitrary white space then tab.
# I don't think na_vavlues takes regex's.
