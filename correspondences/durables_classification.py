import re
import cPickle

import numpy as np
import pandas as pd
from nace_parse import nace_pc, cn_nace


with open('nace_groups_dict.pkl', 'r') as f:
    d_groups = cPickle.load(f)

with open('new_pc_cn_dict.pkl', 'r') as f:
    d_pc_cn = cPickle.load(f)

with open('cn11-prodcom11.pkl', 'r') as f:
    d_cn_pc = cPickle.load(f)

durables = list(set(d_groups['durable'].keys()).union(
    d_groups['capital_goods'].keys()))

m = [t.replace('.', '')[1:] for t in durables]
d_m = {x: 1 for x in m}


def space(x):
    """Takes CN index and inserts spaces after 4th and 6th digit to fit
    into the cn_pc dict keys.  Doesn't handle higher levels yet.
    """
    if len(x) == 8:
        return ' '.join([x[:4], x[4:6], x[6:]])
    else:
        return x


def f(x):
    """ f :: CN (string) -> {0, 1} (int)
    """
    try:
        pc = d_cn_pc[space(x.name[0])]
        if type(pc) is float:  # Pick up weird nan's from dict.
            return np.nan
        else:
            try:
                return d_m[pc[:3]]
            except KeyError:
                try:
                    return d_m[pc[:2]]
                except KeyError:
                    return 0
    except KeyError, e:
        return np.nan


## Testing
monthly = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/monthly.h5')
df = monthly['sep_10'].xs((1, '2010-09-01', '001', 4),
    level=('FLOW', 'PERIOD', 'DECLARANT', 'STAT_REGIME'))

res = df.apply(f, axis=1)

idx = df.index.levels[0]

d = {}
miss = []
for x in idx:
    try:
        if type(d_cn_pc[space(x)]) == float:
            print('Cannot upcast %s.' % x)
            continue
        d[x] = d_cn_pc[space(x)]
    except KeyError, e:
        miss.append(x)
