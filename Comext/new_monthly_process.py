import os

import pandas as pd
from year_month_parse import year_month

os.chdir('/Volumes/HDD/Users/tom/DataStorage/Comext/')
files = [
        'nc200801',
        'nc200802',
        'nc200803',
        'nc200804',
        'nc200805',
        'nc200806',
        'nc200807',
        'nc200808',
        'nc200809',
        'nc200810',
        'nc200811',
        'nc200812',
        'nc200901',
        'nc200902',
        'nc200903',
        'nc200904',
        'nc200905',
        'nc200906',
        'nc200907',
        'nc200908',
        'nc200909',
        'nc200910',
        'nc200911',
        'nc200912',
        'nc201001',
        'nc201002',
        'nc201003',
        'nc201004',
        'nc201005',
        'nc201006',
        'nc201007',
        'nc201008',
        'nc201009',
        'nc201010',
        'nc201011',
        'nc201012',
]

files = [
        'nc201009',
        'nc201010',
        'nc201011',
        'nc201012',
        ]


monthly = pd.HDFStore('monthly.h5')
lookup = {
        'nc200801': 'jan_08',
        'nc200802': 'feb_08',
        'nc200803': 'mar_08',
        'nc200804': 'apr_08',
        'nc200805': 'may_08',
        'nc200806': 'jun_08',
        'nc200807': 'jul_08',
        'nc200808': 'aug_08',
        'nc200809': 'sep_08',
        'nc200810': 'oct_08',
        'nc200811': 'nov_08',
        'nc200812': 'dec_08',
        'nc200901': 'jan_09',
        'nc200902': 'feb_09',
        'nc200903': 'mar_09',
        'nc200904': 'apr_09',
        'nc200905': 'may_09',
        'nc200906': 'jun_09',
        'nc200907': 'jul_09',
        'nc200908': 'aug_09',
        'nc200909': 'sep_09',
        'nc200910': 'oct_09',
        'nc200911': 'nov_09',
        'nc200912': 'dec_09',
        'nc201001': 'jan_10',
        'nc201002': 'feb_10',
        'nc201003': 'mar_10',
        'nc201004': 'apr_10',
        'nc201005': 'may_10',
        'nc201006': 'jun_10',
        'nc201007': 'jul_10',
        'nc201008': 'aug_10',
        'nc201009': 'sep_10',
        'nc201010': 'oct_10',
        'nc201011': 'nov_10',
        'nc201012': 'dec_10',
}

for f in files:
    leaf = lookup[f]

    monthly[leaf] = pd.read_csv(f + '.dat', parse_dates=[5],
        date_parser=year_month, index_col=['FLOW', 'PERIOD', 'DECLARANT',
        'PRODUCT_NC', 'PARTNER', 'STAT_REGIME'])