import string
import cPickle
import itertools as it
from collections import deque

import numpy as np
import pandas as pd


# # Pickling cpa:
# output = open('product_dict.pkl', 'wb')
# cPickle.dump(cpa, output, 2)
# output.close()

# # Pickling partners:
# out = open('partners_dict.pkl', 'wb')
# cPickle.dump(partners, out, 2)
# out.close()

# Read with:
yearly = pd.HDFStore('yearly.h5')

pickle_file = open('product_dict.pkl', 'rb')
cpa = cPickle.load(pickle_file)
pickle_file.close()

partners_pickle = open('partners_dict.pkl', 'rb')
partners = cPickle.load(partners_pickle)
partners_pickle.close()

country_code = {
            '001': 'France',
            '003': 'Netherlands',
            '004': 'Fr Germany',
            '005': 'Italy',
            '006': 'Utd. Kingdom',
            '007': 'Ireland',
            '008': 'Denmark',
            '009': 'Greece',
            '010': 'Portugal',
            '011': 'Spain',
            '017': 'Belgium',
            '018': 'Luxembourg',
            '030': 'Sweden',
            '032': 'Finland',
            '038': 'Austria',
            '600': 'Cyprus',
            '061': 'Czech Republic',
            '053': 'Estonia',
            '064': 'Hungary',
            '055': 'Lithuania',
            '054': 'Latvia',
            '046': 'Malta',
            '060': 'Poland',
            '091': 'Slovenia',
            '063': 'Slovakia',
            '068': 'Bulgaria',
            '066': 'Romania',
            'EU': 'EU',
}


    # leaves = zip(['variety'] * len(country_code), country_code)
    # final = []
    # for elem in leaves:
    #     final.append(string.join(elem, sep='_'))


idx = sorted(cpa.keys())
cols = [
        'product_2007',
        'product_2008',
        'product_2009',
        'product_2010',
        'product_2011',
        ]


def lexicographic(df, i, j):
        '''
        Function to apply to 2 columns of a DataFrame.  Returns a series
        that is the lexicographic max (assuming nonzero here).  Call with
        pd.DataFrame(df.apply(lexicographic, axis=1, args=(0, 1)), columns=['quantity'])
        '''

        if df[i] != 0:
            return df[i]
        else:
            return df[j]

countries = sorted(country_code.keys())


def get_quantities(store, countries, years=['y2007', 'y2008', 'y2009', 'y2010', 'y2011']):
    """"
    Countruts pyTables for the quantities used in the weight_matrix.
    Paramaters
    ----------

    Returns:
    --------
    """
    q_gen = it.product([1, 2], sorted(country_code.keys()), sorted(cpa.keys()))
    for country in countries:
        try:
            yearly['quantity' + '_' + country] = pd.DataFrame(yearly[years[0] + '_' + country].reset_index(level='PERIOD').apply(lexicographic, axis=1, args=(0, 1)), columns=[years[0]])
        except:
            print 'Trouble with %s' % country
        for year in years[1:]:
            try:
                yearly['quantity' + '_' + country] = yearly['quantity' + '_' + country].append(pd.DataFrame(yearly[year + '_' + country].reset_index(level='PERIOD').apply(lexicographic, axis=1, args=(0, 1)), columns=[year]))
            except:
                print 'Trouble with %s, %s in inner loop.' % (country, year)

def weight_matrix(store, countries, years=['y2007', 'y2008', 'y2009', 'y2010', 'y2011']):
    """
    T^(3/2)((1 / q_{gct}) + (1 / q_{gct-1}))^(-1/2)

    Current step is to get quantities for each country, index by (flow, )
    Need to get the index correct.  Want variety_XXX
    to have a (partner, product) multiIndex.

    Having to treat the first year special.

    Check on switching:
    df[(df2['QUANTITY_TON'] == 0) != (df['QUANTITY_TON'] == 0)].head()
    df2[(df2['QUANTITY_TON'] == 0) != (df['QUANTITY_TON'] == 0)].head()

    df.reset_index(level='PERIOD') may be useful.
    """
    



    for year in sorted(yearly.keys()):


    variety_600 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_091 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_010 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_011 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_038 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_018 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_017 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_032 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_055 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_030 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_053 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_061 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_060 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_063 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_064 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_066 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_068 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_003 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_002 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_001 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_007 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_006 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_005 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_004 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_EU = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_046 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_009 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_008 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)
    variety_054 = pd.DataFrame(np.zeros([len(cpa), nyears]), idx, columns=cols)

yearly.close()
