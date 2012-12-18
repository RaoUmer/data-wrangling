from __future__ import division

from cPickle import load

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# USE Table
"""
*Classification Notes*:
    -Should be by NACE Rev. 2.

"""


class use(object):
    """docstring for use"""
    def __init__(self):
        super(use, self).__init__()
        with open('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/'\
            'docs/clean_use_row_labels.pkl', 'r') as f:
            self.d_row = load(f)

        with open('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/'\
            'docs/clean_use_col_labels.pkl', 'r') as f:
            self.d_col = load(f)

        with open('/Users/tom/TradeData/data-wrangling/correspondences/cpa-cn/'\
            'cpa-cn_dict.pkl', 'r') as f:
            self.d_cpa_cn = load(f)

        self.remove = {
            'P3': 'Final consumption expenditure',
            'P3_S13': 'Final consumption expenditure by government',
            'P3_S14': 'Final consumption expenditure by households',
            'P3_S15': 'Final consumption expenditure by non-profit '\
                'organisations serving households (NPISH)',
            'P5': 'Gross capital formation',
            'P51': 'Gross fixed capital formation',
            'P52': 'Changes in inventories',
            'P52_P53': 'Changes in inventories and valuables',
            'P53': 'Changes in valuables',
            'P6': 'Exports',
            'P6_S21': 'Exports intra EU fob',
            'P6_S2111': 'Exports of goods and services EMU members (fob)',
            'P6_S2112': 'Exports of goods and services to EMU non-members (fob)',
            'P6_S22': 'Exports extra EU fob',
            'TFINU': "Final use at purchasers'prices",
            'TOTAL': 'Total',
            'TU': "Total use at purchasers' prices"
            }

        df = pd.read_csv('/Users/tom/TradeData/data-wrangling/Eurostat/'\
            'supply_use/tables/clean_naio_cp16_r2.csv',
            index_col=['unit', 'geo', 'cols', 'rows'])
        df = df.ix['MIO_NAC']
        self.df = df['2008'].unstack(level='cols')

        # Control measure 1: Average value of Downstream use.
        self.res1 = self.df[self.df.columns - self.df[
            self.remove.keys()].columns].mean(axis=1)

        # Control measure 2: Count value of Downstream use.
        def mycount(x):
            return np.count_nonzero(x.dropna())

        self.res2 = self.df[self.df.columns - self.df[
            self.remove.keys()].columns].T.apply(mycount)

        self.thin = [
            'A01',
            'A02',
            'A03',
            'B',
            'C10-C12',
            'C13-C15',
            'C16',
            'C17',
            'C18',
            'C19',
            'C20',
            'C21',
            'C22',
            'C23',
            'C24',
            'C25',
            'C26',
            'C27',
            'C28',
            'C29',
            'C30',
            'C31_C32',
            'C33',
            'D35',
            'E36',
            'E37-E39',
            'F',
            'G45',
            'G46',
            'G47',
            'H49',
            'H50',
            'H51',
            'H52',
            'H53',
            'I',
            'J58',
            'J59_J60',
            'J61',
            'J62_J63',
            'K64',
            'K65',
            'K66',
            'L68A',
            'L68B',
            'M69_M70',
            'M71',
            'M72',
            'M73',
            'M74_M75',
            'N77',
            'N78',
            'N79',
            'N80-N82',
            'O84',
            'P3_S13',
            'P3_S14',
            'P3_S15',
            'P51',
            'P52',
            'P53',
            'P6_S2111',
            'P6_S2112',
            'P6_S22',
            'P85',
            'Q86',
            'Q87_Q88',
            'R90-R92',
            'R93',
            'S94',
            'S95',
            'S96',
            'T',
            'U']

    def heatmap(self, a=4, cmap=plt.cm.gray_r, ctry='all'):
        """Returns a plot showing the intensity of a good's use in
        the other axis' industries.

        Parameters:
        df: dataframe (see notes below)
        a: Thinning paramets.  Plots a label for every ath item.
        cmap: colormap

        Call like:
        for country in df.index.levels[0]:
        try:
            heatmap(np.log(df.ix[country]))
        except:
            pass
        """
        import sys
        sys.path.append('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/')
        from heatmap import hm

        if ctry == 'all':
            for country in self.df.index.levels[0]:
                try:
                    hm(np.log(self.df.ix[country][self.thin]))
                except:
                    print 'No plot for %s' % country
        else:
            if type(ctry) == str:
                try:
                    hm(np.log(self.df.ix[ctry]))
                except:
                    assert 'error'
            elif type(ctry) == list:
                for i, country in enumerate(ctry):
                    try:
                        hm(np.log(self.df.ix[country][self.thin]))
                    except:
                        print('No plot for %s') % country
            else:
                print("Check your country type.  Should be str or list.")







#######################################################
# with open('clean_use_row_labels.pkl', 'r') as f:
#     d_row = load(f)

# with open('clean_use_col_labels.pkl', 'r') as f:
#     d_col = load(f)


# remove = {
#         'P3': 'Final consumption expenditure',
#         'P3_S13': 'Final consumption expenditure by government',
#         'P3_S14': 'Final consumption expenditure by households',
#         'P3_S15': 'Final consumption expenditure by non-profit '\
#             'organisations serving households (NPISH)',
#         'P5': 'Gross capital formation',
#         'P51': 'Gross fixed capital formation',
#         'P52': 'Changes in inventories',
#         'P52_P53': 'Changes in inventories and valuables',
#         'P53': 'Changes in valuables',
#         'P6': 'Exports',
#         'P6_S21': 'Exports intra EU fob',
#         'P6_S2111': 'Exports of goods and services EMU members (fob)',
#         'P6_S2112': 'Exports of goods and services to EMU non-members (fob)',
#         'P6_S22': 'Exports extra EU fob',
#         'TFINU': "Final use at purchasers'prices",
#         'TOTAL': 'Total',
#         'TU': "Total use at purchasers' prices"
# }

# os.chdir('/Users/tom/TradeData/data-wrangling/Eurostat/supply_use/tables')

# df = pd.read_csv('clean_naio_cp16_r2.csv',
#         index_col=['unit', 'geo', 'cols', 'rows'])

# df = df.ix['MIO_NAC']

# # Index is (Country, input), columns are industries.
# df = df['2008'].unstack(level='cols')

# # Control measure 1: Average value of Downstream use.
# res1 = df[df.columns - df[remove.keys()].columns].mean(axis=1)

# # Control measure 2: Count value of Downstream use.


# def mycount(x):
#     return np.count_nonzero(x.dropna())

# res2 = df[df.columns - df[remove.keys()].columns].T.apply(mycount)


# ################### Example #####################
# # ## Groupby mechanics:


# # df2 = df[['A01', 'A02', 'R93', 'S94', 'I']]
# # gr2 = df2.groupby(axis=0, level='geo', group_keys=False)
# # test = df2.ix['AT']

# # # measure 2:
# # trans = test.T.dropna(how='all')  # Only summing over columns seems to work.
# # trans.apply(mycount)


# # ## Label Check:  Shows that I should switch my col labels from original (done).
# # hit = []
# # miss = []
# # fails = []

# # for k in df.columns:
# #     try:
# #         hit.append(d_row[k])
# #     except KeyError:
# #         try:
# #             miss.append(d_col[k])  # Should get most/all
# #         except KeyError:
# #             fails.append(k)

# # hit2 = []
# # miss2 = []
# # fails2 = []

# # for k in df.ix['AT'].index:
# #     try:
# #         hit2.append(d_row[k])  # Should get most/all
# #     except KeyError:
# #         try:
# #             miss2.append(d_col[k])
# #         except KeyError:
# #             fails2.append(k)
