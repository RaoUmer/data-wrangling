import string

import numpy as np
import pandas as pd
from nace_cn_parse import nace_cn

df = pd.read_csv('sts_inlb_a.tsv',
    sep=",|s*\t", na_values=[':', ' :', ': '],
    index_col=['indic_bt', 'nace_r2', 's_adj', r'geo\time'])

df.columns = [string.lstrip(x.rstrip()) for x in df.columns]
df2 = df[[str(x) for x in (range(2000, 2007))]].xs(('HOWK', 'GROSS'), level=(
    'indic_bt', 's_adj'))


def strip_float(x):
    """Use with applymap to convert Maybe annotated floats (strings) to floats.
    Warning: Strips some provisionals warnings.  See origninal for details.
    """
    if type(x) == float:
        return x
    else:
        try:
            return float(x.split(' ')[0])
        except ValueError:
            return np.nan

df2 = df2.applymap(strip_float)
df2.index.names = ['nace', 'geo']
ret = nace_cn(df2.index.levels[0])

df2.ix[[x for x in ret]].mean(axis=1).dropna().to_csv(
    'labor_input_00to06_clean.csv', header=True)
