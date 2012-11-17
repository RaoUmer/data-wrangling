

def get_reference(store, country, n=500,
        years=['y2007', 'y2008', 'y2009', 'y2010', 'y2011']):
    """
    Finds potential countries to use as k in calculating errors.
    Must provide a positive quantity in every year. (Exports & Imports?)

    Read inside out to maintain sanity.  Would be so easy recursively...
        Get index for first year possible (i.e. second year in sample).
        Filter by calling .ix on that index; drop the NaNs.  Take that index.
        ...
        End with index of (flow, product, partner) that works as references.

    TODO:
    Going to have to rework this to return a list of potentials for each prod.
    From that list we'll (automatically according to some criteria) choose
    the reference **for that product**.  That criteria MUST include preference
    for other countries in the dataset.  If not, no way to calculate moment.

    Parameters:
    -----------
    store : HDF5Store
    country : String
    years: list of strings

    Returns:
    --------
    DataFrame (call index on this; for storage reasons).
    Or maybe a list of tuples with (good, partner) pairs?

    I need a (product, reference) tuple
    """

    idx =store['quantity_' + country].head(n)[years[4]].ix[1].ix[
        store['quantity_' + country].head(n)[years[3]].ix[1].ix[
        store['quantity_' + country].head(n)[years[2]].ix[1].ix[
        store['quantity_' + country].head(n)[years[1]].ix[1].ix[
        store['quantity_' + country].head(n)[years[0]].ix[1].dropna().index
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


    # for product in np.unique(df.index.get_level_values('PRODUCT_NC')):
    #     print picker(df.xs((1, product), level=('FLOW', 'PRODUCT_NC')).index)
