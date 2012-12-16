from __future__ import division

import sys
import datetime as dt

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

sys.path.append('/Users/tom/TradeData/data-wrangling/correspondences')
sys.path.append('/Users/tom/TradeData/data-wrangling/Eurostat/response')
from response import pct_chng
from durables_classification import get_dummy


monthly = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/monthly.h5')
yearly = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/yearly.h5')
# Most drops in 2008Q2, next most in 2008Q3

m_dict = {
        1: ['jan', 1],
        2: ['feb', 1],
        3: ['mar', 1],
        4: ['apr', 2],
        5: ['may', 2],
        6: ['jun', 2],
        7: ['jul', 2],
        8: ['aug', 2],
        9: ['sep', 2],
        10: ['oct', 4],
        11: ['nov', 4],
        12: ['dec', 4]
        }


def just_8(df):
    """Filters out the aggregates, leaving only 8 digit indicies.
    Expects df to have index level 1 of products.
    """
    if df.index.levels[0].name != 'PRODUCT_NC':
        raise NameError
    return df.index.levels[0][[len(x) == 8 for x in df.dropna().index.levels[0]]]


def grand_reg(country, date):
    """
    Parameters
    ----------
        -Country: Should be string (e.g. '001')
        -date: list of ints [year, month]: e.g. ['2009', 9]
    """
    pass


class grandRegression(object):
        """docstring for grad_reg"""
        def __init__(self, country, date):
            """Date should be [int, int], [year, month].
            """
            super(grandRegression, self).__init__()
            self.country = country
            self.month = m_dict[date[1]][0]  # str
            self.q = m_dict[date[1]][1]
            self.year = date[0]
            self.yearly = 'y' + str(self.year) + '_' + self.country
            self.isodt = dt.datetime.isoformat(dt.datetime(
                self.year, date[1], 1))[:10]

            #Data IO
            self.df = monthly[self.month + '_' + str(self.year)[2:]].xs((
                1, self.isodt, self.country, 4), level=('FLOW', 'PERIOD',
                'DECLARANT', 'STAT_REGIME'))
            self.sf = yearly[self.yearly][yearly[self.yearly][
            'STAT_REGIME'] == 4].xs((1, 200952), level=("FLOW", 'PERIOD'))
            self.y = pct_chng(self.country, [self.year, self.q]).dropna().ix[1]

            # Indicies
            self.idx8 = just_8(self.df)

            # Size of each product relative to ALL imports.
            self.df_red = pd.DataFrame(self.df.ix[self.idx8].groupby(axis=0,
                level='PRODUCT_NC')['VALUE_1000ECU'].sum() / (self.df.ix[
                self.idx8].groupby(axis=0, level='PRODUCT_NC')[
                'VALUE_1000ECU'].sum().sum()), columns=['size'])

            get_dummy(self.df_red)
            self.df_red = sm.add_constant(self.df_red, prepend=True)

            self.idx = self.y.index.intersection(self.df_red.dropna().index)
            self.endog = self.y[self.idx]
            self.endog.name = 'pct_change'
            self.exog = self.df_red.ix[self.idx]

        def estimate(self):
            """Get fitted regression result.  No controls for now.
            """
            model = sm.OLS(self.endog, self.exog)
            return model.fit()

        def filter(self):
            """Attempt to "deal with" (ignore) outliers.
            """
            f_idx = self.exog['size'][self.exog['size'] < self.exog[
                'size'].quantile(.9997)].index

            f_idx = f_idx.intersection(self.endog[
                self.endog < self.endog.quantile(.995)].index)
            self.f_exog = self.exog.ix[f_idx]
            self.f_endog = self.endog[f_idx]
            self.f_res = sm.OLS(self.f_endog, self.f_exog).fit()

if __name__ == '__main__':
    pass

# Testing
"""
df = monthly['sep_09'].xs((1, '2009-09-01'), level=('FLOW', 'PERIOD'))
sf = yearly['y2009_001']
sf = sf[sf['STAT_REGIME'] == 4].xs((1, 200952), level=("FLOW", 'PERIOD'))
gr = sf.groupby(axis=0, level='PRODUCT_NC')

y = pct_chng('001', [2009, 3]).dropna().ix[1]

test = df.xs(('001', 4), level=("DECLARANT", 'STAT_REGIME'))
res = pd.DataFrame(
    test.groupby(axis=0, level='PRODUCT_NC')['VALUE_1000ECU'].sum())

idx8 = res.index[[len(x) == 8 for x in res.index]]  # Need to avoid partners.
gr2 = test.ix[idx8].groupby(axis=0, level='PRODUCT_NC')
sc = pd.DataFrame(
    gr2['VALUE_1000ECU'].sum()[idx8] / gr2['VALUE_1000ECU'].sum()[idx8].sum())
sc.columns = ['size']
get_dummy(sc)

idx = y.dropna().index.intersection(idx8)
idx4 = idx3.intersection(exog.dropna().index)

endog = y[idx]
exog = sm.add_constant(sc.ix[idx], prepend=True)

model = sm.OLS(y[idx4], exog[['const', 'durable', 'size']].ix[idx4])
results = model.fit()
print results.summary()

### Some plotting ###
y2 = endog[endog < .5]
x2 = exog[exog['size'] < .015]
idx3 = y2.index.intersection(x2.index)
plt.scatter(exog['size'].ix[idx3], endog[idx3])
plt.figure()
plt.subplot(111)
plt.scatter(exog['size'].ix[idx3], endog[idx3])
"""