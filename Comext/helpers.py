from __future__ import division


def unit_price(df, col1='VALUE_1000ECU', col2='QUANTITY_TON',
                                        col3='SUP_QUANTITY'):
    """
    Calculate the unit price estimate for each good.
    Use with df.apply, axis=1.

    Parameters
    ----------
    df: Pandas dataFrame.
    col1: Total Valaue of item.
    col2: First measure of weight.
    col3: Second measure of weight.

    Returns
    -------
    Pandas Series.  Set to unit_price column in df.
    """
    if df[col2] == 0:
        if df[col3] == 0:
            unit_p = 0
            return unit_p
        else:
            unit_p = df[col1] / df[col3]
            return unit_p
    else:
        unit_p = df[col1] / df[col2]
        return unit_p
    return unit_p
