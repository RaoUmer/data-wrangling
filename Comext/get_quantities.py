import os
import cPickle

import pandas as pd


# def get_quantities(countries, store=yearly, years=['y2007', 'y2008', 'y2009',
#         'y2010', 'y2011']):
#     """"
#     Counstructs pyTables for the quantities used in the weight_matrix.
#     May be useful: q_gen = it.product([1, 2], sorted(country_code.keys()),
#         sorted(cpa.keys()))
#     Paramaters
#     ----------
#     Returns:
#     --------
#     """

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly')
yearly = pd.HDFStore('yearly.h5')

pickle_file = open('product_dict.pkl', 'rb')
cpa = cPickle.load(pickle_file)
pickle_file.close()

# partners_pickle = open('partners_dict.pkl', 'rb')
# partners = cPickle.load(partners_pickle)
# partners_pickle.close()


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


def lexicographic(df, i, j):
        '''
        Function to apply to 2 columns of a DataFrame.  Returns a series
        that is the lexicographic max (assuming nonzero here).  Call with
        pd.DataFrame(df.apply(lexicographic, axis=1, args=(0, 1)),
        columns=['quantity'])
        '''

        if df[i] != 0:
            return df[i]
        else:
            return df[j]

countries = sorted(country_code.keys())
years = ['y2007', 'y2008', 'y2009', 'y2010', 'y2011']

for country in countries:
    try:
        yearly['quantity' + '_' + country] = pd.DataFrame(
            yearly[years[0] + '_' + country].reset_index(level='PERIOD').apply(
            lexicographic, axis=1, args=(0, 1)), columns=[years[0]])
    except:
        print 'Trouble with %s' % country
    for year in years[1:]:
        try:
            yearly['quantity' + '_' + country] = yearly[
                'quantity' + '_' + country].merge(pd.DataFrame(
                yearly[year + '_' + country].reset_index(level='PERIOD').apply(
                lexicographic, axis=1, args=(0, 1)), columns=[year]),
                how='outer', left_index=True, right_index=True)
        except:
            print 'Trouble with %s, %s in inner loop.' % (country, year)
yearly.close
