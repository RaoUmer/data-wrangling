import cPickle

import pandas as pd


def cn_nace(x, to='nace'):
    """
    To move from CN to NACE nomenclature via:
    cn12 <-> cn11 <-> PRODCOM <- NACE

    Check length for 2 v 4 v 6 v 8 digits.
    """
    def space(x):
        if len(x) == 8:
            return ' '.join([x[:4], x[4:6], x[6:]])
        else:
            return x

######## Testing
import space

monthly = pd.HDFStore('montly.h5')
m = monthly['jan_08'].ix[1].ix['2008-01-01']
f = open('new_cn_to_pd.pkl')
d_cn_pc = cPickle.load(f)
f.close()

hits = []
miss = []
for i in m.index.levels[1]:
    try:
        hits.append(d_cn_pc[space(i)])
    except KeyError:
        miss.append(space(i))
