from __future__ import division

import pandas as pd
from time_parsers import year_quarter

"""
For the trade wedge

Using 2008Q1 - most recent (2012Q3ish) for nominal GDP and
chained to 2005 dollars.

GDP
    Chained: "Millions of euro, chain-linked volumes, reference year 2005 (at 2005 exchange rates)"
    http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055780_QID_32EF0224_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;S_ADJ,L,Z,0;UNIT,L,Z,1;INDIC_NA,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-055780S_ADJ,NSA;DS-055780INDIC_NA,B1GM;DS-055780INDICATORS,OBS_FLAG;DS-055780UNIT,MIO_EUR_CLV2005;&rankName1=TIME_1_0_0_0&rankName2=INDIC-NA_1_2_-1_2&rankName3=S-ADJ_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=UNIT_1_2_-1_2&rankName6=GEO_1_2_0_1&pprRK=FIRST&pprSO=PROTOCOL&ppcRK=FIRST&ppcSO=ASC&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23
    
    Nominal: "GEO","TIME","S_ADJ","UNIT","INDIC_NA","Value","Flag and Footnotes"
    http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055786_QID_-7BCFD5FF_UID_-3F171EB0&layout=GEO,L,X,0;TIME,C,Y,0;S_ADJ,L,Z,0;UNIT,L,Z,1;INDIC_NA,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-055786INDICATORS,OBS_FLAG;DS-055786S_ADJ,NSA;DS-055786UNIT,MIO_EUR;DS-055786INDIC_NA,B1GM;&rankName1=INDIC-NA_1_2_-1_2&rankName2=S-ADJ_1_2_-1_2&rankName3=INDICATORS_1_2_-1_2&rankName4=UNIT_1_2_-1_2&rankName5=GEO_1_2_0_0&rankName6=TIME_1_0_0_1&sortR=ASC_-1_FIRST&pprRK=FIRST&pprSO=ASC&ppcRK=FIRST&ppcSO=PROTOCOL&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23

Imports
    Chained: TIME   GEO S_ADJ   UNIT    INDIC_NA    Value   Flag and Footnotes
    http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055780_QID_-565264BB_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;S_ADJ,L,Z,0;UNIT,L,Z,1;INDIC_NA,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-055780S_ADJ,NSA;DS-055780INDIC_NA,P7;DS-055780INDICATORS,OBS_FLAG;DS-055780UNIT,MIO_EUR_CLV2005;&rankName1=TIME_1_0_0_0&rankName2=INDIC-NA_1_2_-1_2&rankName3=S-ADJ_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=UNIT_1_2_-1_2&rankName6=GEO_1_2_0_1&pprRK=FIRST&pprSO=PROTOCOL&ppcRK=FIRST&ppcSO=ASC&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23

    Nominal GEO S_ADJ   UNIT    INDIC_NA    Value   Flag and Footnotes
    http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055786_QID_-6663BBED_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;S_ADJ,L,Z,0;UNIT,L,Z,1;INDIC_NA,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-055786INDICATORS,OBS_FLAG;DS-055786S_ADJ,NSA;DS-055786UNIT,MIO_EUR;DS-055786INDIC_NA,P7;&rankName1=TIME_1_0_0_0&rankName2=INDIC-NA_1_2_-1_2&rankName3=S-ADJ_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=UNIT_1_2_-1_2&rankName6=GEO_1_2_0_1&pprRK=FIRST&pprSO=PROTOCOL&ppcRK=FIRST&ppcSO=ASC&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23

Demand
    Chained: TIME    GEO S_ADJ   UNIT    INDIC_NA    Value   Flag and Footnotes
    http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055780_QID_-2F18ADE0_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;S_ADJ,L,Z,0;UNIT,L,Z,1;INDIC_NA,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-055780S_ADJ,NSA;DS-055780INDIC_NA,P3_P5;DS-055780INDICATORS,OBS_FLAG;DS-055780UNIT,MIO_EUR_CLV2005;&rankName1=TIME_1_0_0_0&rankName2=INDIC-NA_1_2_-1_2&rankName3=S-ADJ_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=UNIT_1_2_-1_2&rankName6=GEO_1_2_0_1&pprRK=FIRST&pprSO=PROTOCOL&ppcRK=FIRST&ppcSO=ASC&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23

    Nominal: TIME   GEO S_ADJ   UNIT    INDIC_NA    Value   Flag and Footnotes
    http://appsso.eurostat.ec.europa.eu/nui/show.do?query=BOOKMARK_DS-055786_QID_-7AEE9C80_UID_-3F171EB0&layout=TIME,C,X,0;GEO,L,Y,0;S_ADJ,L,Z,0;UNIT,L,Z,1;INDIC_NA,L,Z,2;INDICATORS,C,Z,3;&zSelection=DS-055786INDICATORS,OBS_FLAG;DS-055786S_ADJ,NSA;DS-055786UNIT,MIO_EUR;DS-055786INDIC_NA,P3_P5;&rankName1=TIME_1_0_0_0&rankName2=INDIC-NA_1_2_-1_2&rankName3=S-ADJ_1_2_-1_2&rankName4=INDICATORS_1_2_-1_2&rankName5=UNIT_1_2_-1_2&rankName6=GEO_1_2_0_1&pprRK=FIRST&pprSO=PROTOCOL&ppcRK=FIRST&ppcSO=ASC&sortC=ASC_-1_FIRST&rStp=&cStp=&rDCh=&cDCh=&rDM=true&cDM=true&footnes=false&empty=false&wai=false&time_mode=NONE&lang=EN&cfo=%23%23%23%2C%23%23%23.%23%23%23

"""

gdp_c = pd.read_csv('chained_gdp.csv', index_col=[1, 0],
    parse_dates=[1], date_parser=year_quarter, thousands=',', na_values=':').drop(
    ['UNIT', 'INDIC_NA', 'S_ADJ'], axis=1)
gdp_c = gdp_c.unstack().stack(1)

gdp_n = pd.read_csv('nominal_gdp.csv', index_col=[1, 0],
    parse_dates=[1], date_parser=year_quarter, thousands=',', na_values=':').drop(
    ['UNIT', 'INDIC_NA', 'S_ADJ'], axis=1)
gdp_n = gdp_n.unstack().stack(1)

imports_c = pd.read_csv('chained_imports.csv', index_col=[0, 1],
    parse_dates=[0], date_parser=year_quarter, thousands=',', na_values=':').drop(
    ['UNIT', 'INDIC_NA', 'S_ADJ'], axis=1)
imports_c = imports_c.unstack().stack(1)

imports_n = pd.read_csv('nominal_imports.csv', index_col=[0, 1],
    parse_dates=[0], date_parser=year_quarter, thousands=',', na_values=':').drop(
    ['UNIT', 'INDIC_NA', 'S_ADJ'], axis=1)
imports_n = imports_n.unstack().stack(1)

demand_c = pd.read_csv('chained_demand.csv', index_col=[0, 1],
    parse_dates=[0], date_parser=year_quarter, thousands=',', na_values=':').drop(
    ['UNIT', 'INDIC_NA', 'S_ADJ'], axis=1)
demand_c = demand_c.unstack().stack(1)

demand_n = pd.read_csv('nominal_demand.csv', index_col=[0, 1],
    parse_dates=[0], date_parser=year_quarter, thousands=',', na_values=':').drop(
    ['UNIT', 'INDIC_NA', 'S_ADJ'], axis=1)
demand_n = demand_n.unstack().stack(1)

frames = [gdp_c, gdp_n, imports_c, imports_n, demand_c, demand_n]

e1 = 1.5
e2 = 6

# gdp_c.xs('Austria', level=1)['Value'].plot()