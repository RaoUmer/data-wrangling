import pandas as pd

df = pd.read_csv(
    '/Volumes/HDD/Users/tom/DataStorage/Eurostat/namq_gdp_c/namq_gdp_c_1_Data.csv',
    parse_dates=True, na_values=':', thousands=',')
