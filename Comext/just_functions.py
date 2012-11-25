import pandas as pd


def get_shares(country, year, square=2, name='s_', store=yearly):
    """
    Use to fill in the table for gmm calculation.

    Parameters
    ----------
    country : string.  Probably from an outer loop.
    year : int.
    square : whether to square the result or not. Defaults to true (i.e. 2).
    name : string. For the returned column name.
    store : HDFStore.
    Returns
    -------
    A dataframe w/ col name name_YYYY
    """

    year1 = 'y' + str(year) + '_'
    year0 = 'y' + str(year - 1) + '_'
    iyear1 = int(str(year) + '52')
    iyear0 = int(str(year - 1) + '52')

    df1 = yearly[year1 + country]['VALUE_1000ECU'].ix[1]
    df0 = yearly[year0 + country]['VALUE_1000ECU'].ix[1]

    gr1 = df1.groupby(axis=0, level='PRODUCT_NC')
    gr0 = df0.groupby(axis=0, level='PRODUCT_NC')

    l1 = []
    drop1 = []
    for product in gr1.groups.keys():
        try:
            l1.append((iyear1, product, ref_dict[product]))
        except KeyError:
            drop1.append(product)

    l0 = []
    drop0 = []
    for product in gr0.groups.keys():
        try:
            l0.append((iyear0, product, ref_dict[product]))
        except KeyError:
            drop0.append(product)

    # Check if return is actually what you want to do.
    return pd.DataFrame(
        np.log(df1 / gr1.sum().reindex(df1.index, level='PRODUCT_NC')).ix[iyear1] - (
        np.log(df0 / gr0.sum().reindex(df0.index, level='PRODUCT_NC')).ix[iyear0]) - (
        np.log(df1.ix[l1].ix[iyear1].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df1.index, level='PRODUCT_NC').ix[iyear1] / gr1.sum().reindex(df1.index, level='PRODUCT_NC').ix[iyear1]) - (
        np.log(df0.ix[l0].ix[iyear0].reset_index(level='PARTNER')['VALUE_1000ECU'].reindex(df0.index, level='PRODUCT_NC').ix[iyear0] / gr0.sum().reindex(df0.index, level='PRODUCT_NC').ix[iyear0])
        )
        ), columns=[name + str(year)]
        ) ** square
