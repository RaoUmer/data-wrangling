import re

import pandas as pd
from matplotlib.pylab import flatten

letter_header = {
        'A': ['01', '02', '03'],
        'B': ['05', '06', '07', '08', '09'],
        'C': ['10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33'],
        'D': ['35'],
        'E': ['36', '37', '38', '39'],
        'F': ['41', '42', '43'],
        'G': ['45', '46', '47'],
        'H': ['49', '50', '51', '52'],
        'I': ['55', '56'],
        'J': ['58', '59', '60', '61', '62', '63'],
        'K': ['64', '65', '66'],
        'L': ['68'],
        'M': ['69', '70', '71', '72', '73', '74', '75'],
        'N': ['77', '78', '79', '80', '81', '82'],
        'O': ['84'],
        'P': ['85'],
        'Q': ['86', '87', '88'],
        'R': ['90', '91', '92', '93'],
        'S': ['94', '95', '96'],
        'T': ['97', '98'],
        'U': ['99']
        }
# for country in c.res1.index.levels[0]:


def use_col_parse(c, country=None):
    l = c.res1.ix[country].index
    l2 = []
    d2 = {}
    for s in l:
        m1 = re.search(r'CPA_\w\d\d\w|CPA_\w*\d|CPA_[B, F, I, T, U]$', s)
        if m1:
            m2 = re.findall(r'[^_]\d\d[A-Z]?|[B, F, I, T, U]', s)
            l2.append(m2)
            try:
                for i, v in enumerate(m2):
                    d2[v] = c.res1.ix[country].ix[s]
            except IndexError:
                pass
    """
    Not too proud of this one.  Some lists in our list l2 are 'ranges'.
    Need to get the endpoints of 'ranges', fill them in, append to l2,
    then flatten,[A-Z]hen exand the leading letter, then go to dict.
    """
    for i in l2:
        if type(i) == list and len(i) > 1:
            x1, x2 = i[0][-2:], i[1][-2:]
            r = range(int(x1) + 1, int(x2))
            l2 = l2 + [i[0][0] + str(x) for x in r]

    full = sorted(flatten(l2))
    diff = list(set(full) - set(d2.keys()))
    for x in diff:
        d2[x] = d2[x[0] + str(int(x[-2:]) - 1)]

    d3 = {}
    for s in d2.keys():
        if len(s) > 1:
            l2 = [re.findall(s[-2:] + r'.\d\d.\d\d', x) for x in c.d_cpa_cn.keys()]
            l3 = filter(lambda x: len(x) > 0, l2)
            for t in flatten(l3):
                d3[t] = d2[s]
        else:
            temp = c.letter_header[s]
            for s2 in temp:
                l2 = [re.findall(s2 + r'.\d\d.\d\d', x) for x in sorted(c.d_cpa_cn.keys())]
                l3 = filter(lambda x: len(x) > 0, l2)
                for t in flatten(l3):
                    d3[t] = d2[s]

    g1 = (x for x in sorted(d3.values()))
    g2 = (c.d_cpa_cn[x] for x in sorted(d3.keys()))
    return pd.DataFrame([x for x in g1],
        columns=[country + '_res1'], index=[y for y in g2])
