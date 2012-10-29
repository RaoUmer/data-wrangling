# more cleaning
import pandas as pd

df2 = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Eurostat/namq_gdp_c 2/namq_gdp_c_1_Data.csv', index_col=[1,0], parse_dates=True, na_values=':', thousands=',')
df2 = df2.rename(columns={'Value': 'g_nsa_m_n'})
df2 = df2.drop(['S_ADJ', 'UNIT', 'INDIC_NA', 'Flag and Footnotes'], axis = 1)

df3 = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Eurostat/namq_gdp_c 2/namq_gdp_c_2_Data.csv', index_col=[1,0], parse_dates=True, na_values=':', thousands=',')
df3 = df3.rename(columns={'Value': 'e_nsa_m_n'})
df3 = df3.drop(['S_ADJ', 'UNIT', 'INDIC_NA', 'Flag and Footnotes'], axis = 1)

df4 = pd.read_csv('/Volumes/HDD/Users/tom/DataStorage/Eurostat/namq_gdp_c 2/namq_gdp_c_3_Data.csv', index_col=[1,0], parse_dates=True, na_values=':', thousands=',')
df4 = df4.rename(columns={'Value': 'im_nsa_m_n'})
df4 = df4.drop(['S_ADJ', 'UNIT', 'INDIC_NA', 'Flag and Footnotes'], axis = 1)

df = pd.merge(df2, df3, on=None, how='outer', left_index=True, right_index=True)
df = pd.merge(df, df4, on=None, how='outer', left_index=True, right_index=True)

nsa_m_n = pd.HDFStore('nsa_m_n.h5')
nsa_m_n['df'] = df

# Reading in
nsa_m_n = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Eurostat/namq_gdp_c 2/nsa_m_n.h5')
df = nsa_m_n['df']
nsa_m_n.close()

# Some Plotting
plt.figure()

fig_1 =  df.unstack('GEO')[('g_nsa_m_n', 'European Union (27 countries)')].plot()
plt.figure()

fig_2 =  df.unstack('GEO')[('im_nsa_m_n', 'European Union (27 countries)')].plot()
plt.figure()

fig_3 =  df.unstack('GEO')[('e_nsa_m_n', 'European Union (27 countries)')].plot()
plt.figure()
fig_4 =  df.unstack('GEO')[('e_nsa_m_n', 'European Union (27 countries)')].pct_change(4).plot()
fig_5 =  df.unstack('GEO')[('g_nsa_m_n', 'European Union (27 countries)')].pct_change(4).plot()
fig_5 =  df.unstack('GEO')[('g_nsa_m_n', 'European Union (27 countries)')].pct_change(4).plot(c='r')
fig_6 =  df.unstack('GEO')[('im_nsa_m_n', 'European Union (27 countries)')].pct_change(4).plot(c='k')
