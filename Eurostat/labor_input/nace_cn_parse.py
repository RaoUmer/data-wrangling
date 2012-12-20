import cPickle

import numpy as np
import re
import pandas as pd

def nace_cn(idx):
    """Turns nace industries into CN industries.
    example: ret = nace_cn(ind)
    df.ix[[x for x in ret]]
    """
    l2 = []
    p1 = re.compile(r'[B, C, D, E]\d\d')
    for i in idx:
        m = re.search(p1, i)
        if m:
            l2.append(m.group())

    letter_header = {
            'A': ['01', '02', '03'],
            'B': ['05', '06', '07', '08', '09'],
            'C': ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                '30', '31', '32', '33'],
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

    return sorted(np.unique(l2))

with open('/Users/tom/Tradedata/data-wrangling/correspondences/cpa-cn/cpa-cn_dict.pkl', 'r') as f:
    d_cpa_cn = cPickle.load(f)


def get_val(df, ctry):
    """Filling values
    """

    d = df.xs(ctry, level='geo').to_dict()['labor']
    ret = {}
    for prod in d.keys():
        l2 = filter(None, [re.findall(prod[-2:] + r'.\d\d.\d\d', x)
            for x in sorted(d_cpa_cn.keys())])
        for t in l2:
            ret[t[0]] = d[prod]

    g1 = (x for x in sorted(ret.values()))
    g2 = (d_cpa_cn[x] for x in sorted(ret.keys()))
    return pd.DataFrame([x for x in g1],
        columns=[ctry + '_labor'], index=[y for y in g2])
