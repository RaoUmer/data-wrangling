import pandas as pd
from bs4 import BeautifulSoup
import urllib2

def get_names(tag, names):
    """
    Use to extract the column names from a element.Tag;
    
    Parameters
    ----------
    
    * tag : an element.Tag (e.g. from BeautifulSoup)
    * names : a list (probably empty; I was having trouble when names
    was not a param, I think since it was declared locally and thus not
    returned in the last line.  Maybe...
    
    Returns
    -------
    
    * dictionary : a dict containing the columns to be used for a DataFrame
    and initialized empty lists.
    """
    
    for i in range(len(tag.findChildren())):
        names.append(tag.findChildren()[i].name)
    
    values = [list([]) for _ in range(len(names))]
    dictionary = dict(zip(names, values))
    return dictionary

def to_frame(soup, dictionary):
    """
    Use to convert an xml file (in soup form) to a pandas dataFrame.
    
    Parameters
    ----------
    * soup : A BeautifulSoup object, parsed as xml, either from web or local.
    * dictionary : A dict with index from columns and empty lists to be filled.
    
    Returns
    -------
    * Dataframe object with dict index -> column names. No unique index in df.
    """
    
    tags = soup.findAll('r')
    for key in dictionary.keys():
        for tag in tags:
            dictionary[key].append(tag.find(key).string)

    df = pd.DataFrame(dictionary)
    return df

def to_unicode(df, encoding):
    """
    Use to change encoding on dataFrame elements.

    Parameters
    ----------
    * df : a pandas dataFrame
    * encoding : A string. e.g. 'utf-8'
    Returns
    -------
    * df' : a pandas dataFrame encoded as type encoding.

    Need the try/except for the None types.
    """

    for column in df.columns:
        for row in range(len(df)):
            try:
                df[column][row] = df[column][row].encode(encoding)
            except:
                pass



def comtrade_import(params):
    """
    Interface to Comtrade.

    Parameters
    ----------

    * px - Commodity Classifications - HS, H0-H3, ST, S1-S4, BE
    * r - Reporting Countries - UN Comtrade Country Codes or Country Groups
    * y - Years - 4 digits year
    * cc - Commodity Codes - Commodity Codes, with wild cards or Commodity Groups
    * p - Partner Countries - UN Comtrade Country Codes or Country Groups
    * rg - Trade Flow - Number 1 to 4
    * so - Sort Order - See Below
    * tv1 - Comparison Sign - See Below
    * tv2 - Comparison Value - See Below
    * qt - Aggregation Value - y or n
    * lowT - Start Date / Time - Date format YYYY-MM-DD
    * HighT - End Date / Time - Date format YYYY-MM-DD
    * comp - Data Compression - True or False
    * isOri - Data - true or False
    * max - Max returned records - Number
    * app - Application Identifier - Any text (optional)
    * count  To count no of records - True or False
    * async - Asynchronous Web Call - True or False
    * coded - Authorization Code - Use for off-site web services acces.
    
    Returns
    -------

    * Pandas dataFrame
    * optionally as a csv?

    Based off: http://unstats.un.org/unsd/tradekb/Knowledgebase/Access-Points-and-Parameters-for-Web-Services
    Sorting:
    so= pre-defined sort order ; possible values
        "1" Year;Flow;Rep;Comm;Ptnr;
        "2" Year;Rep;Flow;Comm;Ptnr;
        "3" Flow;Year;Rep;Comm;Ptnr;
        "4" Flow;Rep;Year;Comm;Ptnr;
        "5" Rep ;Year;Flow;Comm;Ptnr;
        "6" Rep ;Flow;Year;Comm;Ptnr;
        "7" Comm;Year;Flow;Rep ;Ptnr;
        "8" Comm;Year;Rep ;Flow;Ptnr;
        "9" Comm;Flow;Year;Rep ;Ptnr;
        "10" Comm;Flow;Rep ;Year;Ptnr
        "11" Comm;Rep ;Year;Flow;Ptnr;
        "12" Comm;Rep ;Flow;Year;Ptnr;
        "13" Year;Flow;Rep;Comm;TradeVal;
        "14" Year;Rep;Flow;Comm;TradeVal;
        "15" Flow;Year;Rep;Comm;TradeVal;
        "16" Flow;Rep;Year;Comm;TradeVal;
        "17" Rep ;Year;Flow;Comm;TradeVal;
        "18" Rep ;Flow;Year;Comm;TradeVal;
        "19" Comm;Year;Flow;Rep ;TradeVal;
        "20" Comm;Year;Rep ;Flow;TradeVal;
        "21" Comm;Flow;Year;Rep ;TradeVal;
        "22" Comm;Flow;Rep ;Year;TradeVal
        "23" Comm;Rep ;Year;Flow;TradeVal;
        "24" Comm;Rep ;Flow;Year;TradeVal;
        "1001" TradeVal;
        "9999" --None--

        For an example, so=13 will order the result by year, flow, reporter, commodity and value

        Filter Trade value, use tv1 and tv2
        tv1=comparison sign:
        0"Greater Than Equal
        1"Greater Than
        2"Less Than Equal
        3"Less Than
        tv2= comparison value in US$

        For an example, tv1=0&tv2=1000000000 will filter the result for trade value >= 1 billion US$

        Aggregation option
        qt=n or qt=y. If qt set to n, the system will keep the quantity differences during the on-fly commodity aggregation.

    """

    soup = BeautifulSoup(urllib2.urlopen(params), 'lxml')
    tag = soup.r
    names = []
    dictionary = get_names(tag, names)
    df = to_frame(soup, dictionary)
    return df


