import cPickle

import pandas as pd

df = pd.read_csv('CPA 2008 - CN 2012_18-12-2012_18-16-46.csv',
    skiprows=1, index_col='"Source"')
df.index = [x.strip('"') for x in df.index]
d = df.to_dict()['Target']

out = open('cpa-cn_dict.pkl', 'w')
cPickle.dump(d, out, protocol=2)
out.close()


def use_col_parse(l):
    """Use to make column names in use table ammenable to dict lookup.
    """
    ret = p[]
    for s in l:  # heh snl
        m = re.search(r'\d+', s)
        if m:
            ret.append(m.group())
        else:


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

l = c.res1.ix['AT'].index
l2 = []
for s in l:
    m1 = re.search(r'CPA_\w*\d', s)
    if m1:
        m2 = re.findall(r'[^_]\d\d', s)
        l2.append(m2)

"""
Not too proud of this one.  Some lists in our list l2 are 'ranges'.
Need to get the endpoints of 'ranges', fill them in, append to l2,
then flatten, then exand the leading letter, then go to dict.
"""
for l in l2:
    if len(l) > 1:
        x1, x2 = l[0][-2:], l[1][-2:]
        r = range(int(x1) + 1, int(x2))
        l2 = l2 + [l[0][0] + str(x) for x in r]

full = sorted(flatten(l2))