from __future__ import division

import pandas as pd


def naio_munge(file, ind=False):
    """Cleans some problems from naio use-supply/IO tables.
    Drops some provisoinal warnings.

    df = pd.read_csv('clean_naio_cp16_r2.csv', index_col=[0, 1, 2, 3])
    Used on
             naio_munge('naio_cp15_r2.tsv')
    In [55]: naio_munge('naio_cp16_r2.tsv')

    In [56]: naio_munge('naio_cp17_r2.tsv')

    In [57]: naio_munge('naio_cp17i_r2.tsv', ind=True)


    """
    df = df = pd.read_csv(file,
        na_values=[':', ' :', ': ', ': c'], sep=',|s*\t',
        index_col=['unit', 'geo\\time', 't_cols2', 't_rows2'])
    df.columns = [int(x.strip(' ')) for x in df.columns]
    df.index.names = ['unit', 'geo', 'input', 'industry']
    if ind:
        df.index.names = ['unit', 'geo', 'cols', 'rows']

    df = df[2008]
    try:
        df = df.astype('float')
    except ValueError:
        print 'Failed to convert to float'

    df.to_csv('clean_' + file[:-3] + 'csv', header=True)
