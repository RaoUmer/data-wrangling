"""
This is step one of the process.
Taking download from eurostat's Comext bulk download and going to an
HDF5 store, split by declarant.

Via:
http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/
    BulkDownloadListing?sort=1&dir=comext%2F2012S2%2Fdata

I used yealy data from 2000 - 2011.  If additional years are required,
add them under the files.
"""
import subprocess
import os

import pandas as pd
#-----------------------------------------------------------------------------
# Globals and setup.
files = ['nc200052.7z',
         'nc200152.7z',
         'nc200252.7z',
         'nc200352.7z',
         'nc200452.7z',
         'nc200552.7z',
         'nc200652.7z',
         'nc200752.7z',
         'nc200852.7z',
         'nc200952.7z',
         'nc201052.7z',
         'nc201152.7z']

base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
by_declarant_store = pd.HDFStore(base + 'by_declarant.h5')
#-----------------------------------------------------------------------------
# Helper functions


def columnizer(x):
    """
    Renames columns to be more pythonic.
    """
    if x == 'PRODUCT_NC' or x == 'PRODUCT':
        return 'good'  # product clashes with DataFrame method.
    else:
        return x.split('_')[0].lower()


def logger(df, outfile):
    with open(outfile, 'a') as f:
        f.write('\n')
        f.write(str(df.PERIOD[0])[:-2] + '_' + str(len(df)))
#-----------------------------------------------------------------------------
if __name__ == '__main__':

    for file in files:
        try:
            os.chdir(base)
            subprocess.call(["7z", "e", base + file])
            df = pd.read_csv(base + file[:-2] + 'dat')
            logger(df, base + 'year_logging.txt')
            df.columns = map(columnizer, df.columns)
            df['good'] = df['good'].apply(lambda x: str(x))
            df = df.set_index(['period', 'flow', 'stat', 'declarant', 'good',
                               'partner'])
            gr = df.groupby(level='declarant')
            for declarant, frame in gr:
                by_declarant_store.append('ctry_' + declarant, frame)
                print('added country {} for year{}'.format(declarant, file[2:7]))
            subprocess.call(["rm", "-f", file[:-2] + 'dat'])
        except:
            with open('failures.txt', 'a') as f:
                f.write('failed on {}'.format(file))
