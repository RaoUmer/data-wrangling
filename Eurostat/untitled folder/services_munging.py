import numpy as np
import pandas as pd

"""
Data from: http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-061462_QID_8D6729E_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;CURRENCY,L,Z,0;POST,L,Z,1;FLOW,L,Z,2;PARTNER,L,Z,3;INDICATORS,C,Z,4;&zSelection=DS-061462INDICATORS,OBS_FLAG;DS-061462POST,200;DS-061462FLOW,CREDIT;DS-061462CURRENCY,MIO_EUR;DS-061462PARTNER,ACP;&rankName1=TIME_1_0_0_0&rankName2=PARTNER_1_2_-1_2&rankName3=POST_1_2_-1_2&rankName4=FLOW_1_2_-1_2&rankName5=CURRENCY_1_2_-1_2&rankName6=INDICATORS_1_2_-1_2&rankName7=GEO_1_2_0_1&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23
bulk download version.
"""

df = pd.read_csv('services/bop_services.tsv', sep=',|s*\t',
    na_values=[':', ' :', ': '],
    index_col=['currency', 'post', 'flow', 'partner', 'geo\\time'])

df.columns = [int(x.strip(' ')) for x in df.columns]
df.index.names = ['currency', 'post', 'flow', 'partner', 'geo']
df = df.ix['MIO_EUR']

# Mapping of 'post' to description.
d = {200: 'Current account, Services',
    201: 'Current account, Services, Branding, Quasi-transit adjustment',
    205: 'Current account, Services, Transportation',
    206: 'Current account, Services, Transportation, Sea transport',
    207: 'Current account, Services, Transportation, Sea transport, Passenger transport on sea',
    208: 'Current account, Services, Transportation, Sea transport, Freight transport on sea',
    209: 'Current account, Services, Transportation, Sea transport, Supporting, auxiliary and other sea transport services',
    210: 'Current account, Services, Transportation, Air transport',
    211: 'Current account, Services, Transportation, Air transport, Passenger transport by air',
    212: 'Current account, Services, Transportation, Air transport, Freight transport by air',
    213: 'Current account, Services, Transportation, Air transport, Supporting, auxiliary and other air transport services',
    214: 'Current account, Services, Transportation, Other transport (other than sea and air)',
    215: 'Current account, Services, Transportation, Other transport (other than sea and air), Passenger on other transport',
    216: 'Current account, Services, Transportation, Other transport (other than sea and air), Freight on other transport',
    217: 'Current account, Services, Transportation, Other transport (other than sea and air), Other of other transport',
    218: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Space transport',
    219: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Rail transport',
    220: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Rail transport, Passenger on rail',
    221: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Rail transport, Freight on rail',
    222: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Rail transport, Supporting, auxiliar...',
    223: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Road transport',
    224: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Road transport, Passenger on road',
    225: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Road transport, Freight on road',
    226: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Road transport, Supporting, auxiliar...',
    227: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Inland waterway transport',
    228: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Inland waterway transport, Passenger...',
    229: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Inland waterway transport, Freight o...',
    230: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Inland waterway transport, Supportin...',
    231: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Pipeline transport',
    232: 'Current account, Services, Transportation, Other transport (other than sea and air) - extended classification, Other supporting and auxiliary trans...',
    236: 'Current account, Services, Travel',
    237: 'Current account, Services, Travel, Business travel',
    238: 'Current account, Services, Travel, Business travel, Expenditure by seasonal and border workers',
    239: 'Current account, Services, Travel, Business travel, Other business travel',
    240: 'Current account, Services, Travel, Personal travel',
    241: 'Current account, Services, Travel, Personal travel, Health-related expenditure',
    242: 'Current account, Services, Travel, Personal travel, Education related expenditure',
    243: 'Current account, Services, Travel, Personal travel, Other personal travel',
    981: 'Current account, Services, Other services',
    245: 'Current account, Services, Other services, Communications services',
    246: 'Current account, Services, Other services, Communications services, Postal and courier services',
    958: 'Current account, Services, Communications services, Postal and courier services, Postal services',
    959: 'Current account, Services, Communications services, Postal and courier services, Courier services',
    247: 'Current account, Services, Other services, Communications services, Telecommunication services',
    249: 'Current account, Services, Other services, Construction services',
    250: 'Current account, Services, Other services, Construction services, Construction abroad',
    251: 'Current account, Services, Other services, Construction services, Construction in the compiling economy',
    253: 'Current account, Services, Other services, Insurance services',
    254: 'Current account, Services, Other services, Insurance services, Life insurance and pension funding',
    255: 'Current account, Services, Other services, Insurance services, Freight insurance',
    256: 'Current account, Services, Other services, Insurance services, Other direct insurance',
    257: 'Current account, Services, Other services, Insurance services, Reinsurance',
    258: 'Current account, Services, Other services, Insurance services, Auxiliary services',
    260: 'Current account, Services, Other services, Financial services',
    262: 'Current account, Services, Other services, Computer and information services',
    263: 'Current account, Services, Other services, Computer and information services, Computer services',
    264: 'Current account, Services, Other services, Computer and information services, Information services',
    889: 'Current account, Services, Other services, Computer and information services, Information services, News agency services',
    890: 'Current account, Services, Other services, Computer and information services, Information services, Other information provision services',
    266: 'Current account, Services, Other services, Royalties and license fees',
    891: 'Current account, Services, Other services, Royalties and license fees, Franchises and similar rights',
    892: 'Current account, Services, Other services, Royalties and license fees, Other royalties and license fees',
    268: 'Current account, Services, Other services, Other business services',
    269: 'Current account, Services, Other services, Other business services, Merchanting and other trade-related services',
    270: 'Current account, Services, Other services, Other business services, Merchanting and other trade-related services, Merchanting',
    271: 'Current account, Services, Other services, Other business services, Merchanting and other trade-related services, Other trade-related services',
    272: 'Current account, Services, Other services, Other business services, Operational leasing services',
    273: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services',
    274: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Legal, accounting,...',
    275: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Legal, accounting,...',
    276: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Legal, accounting,...',
    277: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Legal, accounting,...',
    278: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Advertising, marke...',
    279: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Research and devel...',
    280: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Architectural, eng...',
    281: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Agricultural, mini...',
    282: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Agricultural, mini...',
    283: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Agricultural, mini...',
    284: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Other miscellaneou...',
    285: 'Current account, Services, Other services, Other business services, Miscellaneous business, professional and technical services, Services between a...',
    287: 'Current account, Services, Other services, Personal, cultural and recreational services',
    288: 'Current account, Services, Other services, Personal, cultural and recreational services, Audio-visual and related services',
    289: 'Current account, Services, Other services, Personal, cultural and recreational services, Other personal, cultural and recreational services',
    895: 'Current account, Services, Other services, Personal, cultural and recreational services, Other personal, cultural and recreational services, Educat...',
    896: 'Current account, Services, Personal, cultural and recreational services, Other personal, cultural and recreational services, Health services',
    897: 'Current account, Services, Other services, Personal, cultural and recreational services, Other personal, cultural and recreational services, Other',
    291: 'Current account, Services, Other services, Government services, n.i.e.',
    292: 'Current account, Services, Other services, Government services, n.i.e., Embassies and consulates',
    293: 'Current account, Services, Other services, Government services, n.i.e., Military units and agencies',
    294: 'Current account, Services, Other services, Government services, n.i.e., Other government services',
    982: 'Current account, Services, Services not allocated',
    894: 'Current account, Services, Memorandum items, Audiovisual transactions',
    983: 'Commercial services (services excluding Government services, n.i.e.)'}


def strip_float(x):
    """Use with applymap to convert Maybe annotated floats (strings) to floats.
    """
    if type(x) == float:
        return x
    else:
        try:
            return float(x.split(' ')[0])
        except ValueError:
            return np.nan

df2 = df.stack().unstack('post').applymap(strip_float)
