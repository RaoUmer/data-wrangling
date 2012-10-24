from bs4 import BeautifulSoup

# def comtrade_parse(url):
#     '''
#     
#     '''

def get_names(tag):
    """
    Use to extract the column names from a element.Tag;
    
    Parameters
    ----------
    
    * tag : an element.Tag (e.g. from BeautifulSoup)
    
    Returns
    -------
    
    * names : a list containing the columns to be used for a DataFrame.
    """
    
    names = []
    for i in range(len(tag.findChildren())):
        return names.append(tag.findChildren()[i].name)
    
