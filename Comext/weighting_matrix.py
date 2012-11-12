import pandas as pd


def weight_matrix(store, country, year,
    years=['y2007', 'y2008', 'y2009', 'y2010', 'y2011'], t=5):
    """
    To adjust for heteroskedasticity in the GMM estimation of
    the elasticity of substitution.

    Formula: T^(3/2)((1 / q_{gct}) + (1 / q_{gct-1}))^(-1/2)
        where:
        T : number of years involved in estimate (5 for now)
        q_{gct} : quantity of variety gc at t.

    Parameters:
    -----------
    store: pyTables object
    country: A string from the declarants dict.
    year: A string e.g. 'y2007' from years.

    Returns:
    --------
    An g*k (number of nonzero varieties).

    TODO:

    - May need to drop the solo varieties (only one year).


    df.count(axis=1)  # Gives the T for each variety.
    sum(df1.count(axis=1) == 1)  # Count of solos
    df1[df1.count(axis=1) == 1]  # DataFrame of the solos


    Check on switching:
    df[(df2['QUANTITY_TON'] == 0) != (df['QUANTITY_TON'] == 0)].head()
    df2[(df2['QUANTITY_TON'] == 0) != (df['QUANTITY_TON'] == 0)].head()

    Helpers:
    """
    # years = ['y2007', 'y2008', 'y2009', 'y2010', 'y2011']  # TEMPORARY
    print 'Starting country %s, year %s now.' % (country, year)
    y0 = years[years.index(year) - 1]
    t = len(years)

    return pd.DataFrame(t ** (3 / 2) * ((1 / store['quantity_' + country][year]) + (
        1 / store['quantity_' + country][y0])) ** (-1 / 2), columns=['weight']).dropna()
