import pandas as pd

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