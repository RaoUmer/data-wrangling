from __future__ import division


def unit_price(df, col1='VALUE_1000ECU', col2='QUANTITY_TON',
                                        col3='SUP_QUANTITY'):
    """
    Calculate the unit price estimate for each good.
    Use with df.apply, axis=1.

    Parameters
    ----------
    df: Pandas dataFrame.
    col1: Total Valaue of item.
    col2: First measure of weight.
    col3: Second measure of weight.

    Returns
    -------
    Pandas Series.  Set to unit_price column in df.
    """
    if df[col2] == 0:
        if df[col3] == 0:
            unit_p = 0
            return unit_p
        else:
            unit_p = df[col1] / df[col3]
            return unit_p
    else:
        unit_p = df[col1] / df[col2]
        return unit_p
    return unit_p

"""
Pickling dicts:
import cPickle

Pickling cpa:
output = open('product_dict.pkl', 'wb')
cPickle.dump(cpa, output, 2)
output.close()

# Pickling partners:
out = open('partners_dict.pkl', 'wb')
cPickle.dump(partners, out, 2)
out.close()

# Pickling country codes:
out = open('declarants_no_002_dict.pkl', 'wb')
cPickle.dump(country_code, out, 2)
out.close()
---------------------------------------------------

Getting dicts:
import cPickle

with open('product_dict.pkl', 'rb') as pickle_file:
    cpa = load(pickle_file)
pickle_file.closed

with open('partners_dict.pkl', 'rb') as partners_pickle:
    partners = load(partners_pickle)
partners_pickle.closed

with open('declarants_no_002_dict.pkl', 'r') as declarants:
    declarants = cPickle.load(declarants)
declarants.closed
---------------------------------------------------



"""