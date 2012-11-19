

def get_reference(store, country,
        years=['y2007', 'y2008', 'y2009', 'y2010', 'y2011']):

    """
    Finds potential countries to use as k in calculating errors.
    Must provide a positive quantity in every year.

    Read inside out to maintain sanity.  Would be so easy recursively...
        Get index for first year possible (i.e. second year in sample).
        Filter by calling .ix on that index; drop the NaNs.  Take that index.
        ...
        End with index of (product, partner) that works as references.

    Parameters:
    -----------
    store : HDF5Store
    country : String
    years: list of strings

    Returns:
    --------
    Or maybe a list of tuples with (good, partner) pairs?
    """

    idx = store['quantity_' + country][years[4]].ix[1].ix[
          store['quantity_' + country][years[3]].ix[1].ix[
          store['quantity_' + country][years[2]].ix[1].ix[
          store['quantity_' + country][years[1]].ix[1].ix[
          store['quantity_' + country][years[0]].ix[1].dropna().index
          ].dropna().index
          ].dropna().index
          ].dropna().index
          ].dropna().index

    holder = '0'
    references = []
    for tuple in idx:
        if tuple[0] == holder:
            pass
        else:
            references.append(tuple)
            holder = tuple[0]
    return (store['quantity_' + country].xs(1, level='FLOW').index,
      {prod: partner for prod, partner in references})

    # for product in np.unique(df.index.get_level_values('PRODUCT_NC')):
    #     print picker(df.xs((1, product), level=('FLOW', 'PRODUCT_NC')).index)
