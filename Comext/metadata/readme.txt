
Data are avalaible in DATA directory
Metadata are available in TEXT directory

To download a file, just go to the correct directory (folder)
and click on the desired file to save it on your computer.



*** Data avalaible in DATA directory, it's a bunch of files *.zip (files *.dat compress in zip format).

Here is the format of data files : 
declarant country, partner country, product code, flow, statistical procedure, period, 
value in 1000ECU, value in tonnes, value in supplementary unit

Each file corresponds to a period, ex : nc200101.dat --> January 2001


FLOW : =1 for import =2 for export
PRODUCT CODE : CN8 (8 digits) 
         : HS2 (2 digits) 
           ("TOTAL" code is TOTAL TRADE)
PARTNER COUNTRY : 4 digits code.
STATISTICAL PROCEDURE : 1 digit code.
statistical procedure 1 has to be calculated thanks to others
    RS1 = RS4-RS2-RS3-RS5-RS6-RS7-RS9
DECLARANT COUNTRY : 3 digits code (EU is Europe)

Example of a *.dat file :
DECLARANT,PARTNER,PRODUCT_NC,FLOW,STAT_REGIME,PERIOD,VALUE_1000ECU,QUANTITY_TON,SUP_QUANTITY
001,0003,01,1,4,200201,6191.13,1947.9,00
001,0003,01011010,1,4,200201,20.66,2.3,6

To get a NC code of 4 or 6 digits, 8 digits corresponding codes have to be added.
Ex : code 1234 is the sum of all 8 digits codes beginning by 1234
(1234 = sum(1234????))



*** In TEXT directory are following text files : 

- ajustmt.txt   : file of adjusted values intra community.
format: , delimited

REPORTER,PARTNER,FLOW,PERIOD,VALUE
001,0002,1,198801,1251392
001,0002,1,198802,1419867

- exchange.txt  : file of exchange rates
format: , delimited

SOURCE_CURRENCY,TARGET_CURRENCY,PERIOD,RATE
ECU,BEC,198801,43.187600
ECU,BEC,198802,43.196400

 
- status.txt    : file of the dates of update of the data
format : , delimited

DECLARANT,PERIOD,TRADE_TYPE,LAST_UPD_DT
001,200101,E,21.09.2001 *
001,200101,I,10.07.2002  


And for each language are following text files  :

catalog.txt   : catalogue of all Eurostat publications
conf.txt      : explaination of confidentialities
cpa.txt       : CPA codes's label
cpanc.txt     : relationship between CPA and NC8 codes
ctci.txt      : CTCI codes's label
ctci5nc.txt   : relationship between CTCI (5 digits) and NC8 codes
dec.txt       : declarant countries's label
curr.txt      : currencies's label
guide.pdf     : methodological guide in pdf format
infogen.txt   : general informations about data and CD
nc.txt        : NC codes's label
part.txt      : partners countries's label
us.txt        : supplementary units's label
usnc.txt      : relationship between NC8 codes and supplementary units
zonepart.txt  : description of zones

- catalog.txt   : catalogue of all eurostat publications
format : text

- conf.txt  : explaination of confidentialities
format : TAB delimited

DATE_START DATE_END DECLARANT PRODUCT_NC TRADE_TYPE TEXT
1997    1998    001 09011100    1    Intra-EU : No breakdown by countries ; 
1997    2001    001 09011100    1    Extra-EU : No breakdown by countries ; 

- cpa.txt : CPA codes's label
format :  TAB delimited

PRODUCT_CPA DATE_START DATE_END DESCRIPTION
01  1988        PRODUCTS OF AGRICULTURE, HUNTING AND RELATED SERVICES
011 1988        CROPS, PRODUCTS OF MARKET, GARDENING AND HORTICULTURE

- cpanc.txt : relationship between CPA and NC8 codes
format : TAB delimited

0111    10SSS041    1997    
011111  10011010    1988    1992


- ctci.txt : CTCI codes's label
format : TAB delimited

PRODUCT_CTCI DATE_START DATE_END DESCRIPTION
0   1988        FOOD AND LIVE ANIMALS
1   1988        BEVERAGES AND TOBACCO

- ctci5nc.txt : relationship between CTCI (5 digits) and NC8 codes
format : TAB delimited

PRODUCT_CTCI PRODUCT_NC DATE_START DATE_END
00108   01SSS001    1997    
00111   01021000    1988    1992


- dec.txt : declarants countries's label
format : TAB delimited

DECLARANT DATE_START DATE_END DESCRIPTION
001 1976        France
002 1976    1998    Belg.Luxbg.


- curr.txt : currencies's label
format : TAB delimited

CURRENCY DATE_START DATE_END DESCRIPTION
FF  1976        Franc (France)
BEC 1976    1998    Franc (Belgique)


- infogen.txt :  general informations about data and CD
format : text


- nc.txt : NC codes's label
format : TAB delimited

PRODUCT_NC DATE_START DATE_END DESCRIPTION
84472091    1988    1993    WARP KNITTING MACHINES, INCL. RASCHEL TYPE
84472092    1994        WARP KNITTING MACHINES, INCL. RASCHEL TYPE, STITCH-BONDING MACHINES, MOTORIZED

- part.txt : partners countries's label (with zones)
format : TAB delimited

COUNTRY DATE_START DATE_END DESCRIPTION
0001    1997        France
0002    1976    1998    Belg.Luxbg.


- us.txt : supplementary units's label
format : TAB delimited

CODE_US DATE_START DATE_END DESCRIPTION
F   1958        METRES
G   1958    1983    THOUSAND METRES


- usnc.txt : relationship between NC8 codes and supplementary units
format : TAB delimited

PRODUCT_NC CODE_US DATE_START DATE_END
01011010    A   2002    2002
01011090    A   2002    2002


- zonepart.txt : description of zones

ZONE COUNTRY DATE_START DATE_END 
1000    0001    1976    1996
1000    0001    1997    


For other informations, you can reach :
Ms MAQUEDA LAFUENTE Ana
Tel : (352) 4301 34101  Fax : (352) 4301 34119
E-mail : comextsupport@ec.europa.eu
