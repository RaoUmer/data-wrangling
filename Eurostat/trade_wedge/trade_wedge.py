import numpy as np
import pandas as pd

df = pd.read_csv('trade_wedge_clean.csv', index_col=['TIME', 'GEO'], parse_dates=[0])

e = [1.5, 6]


def trade_wedge(q1, q2, e=e[0]):
    """
    All in log changes.
    hat{y^f} = e * (hat{P} - hat{p^f}) + hat{(C + I)}

    hat: (log) change
    y^f : (real) demand for imports
    e : elasticity of substitution
    P : GDP deflator (not log?)
    p^f : import price deflator (not log?)
    C + I : Domestic final demand (real consumption + real investment)

    Suggested values for e = {1.5, 6}
    """

    imp_delta = np.log(df['imports_c'].ix[q2]) - np.log(df['imports_c'].ix[q1])

    gdp_def_delta = np.log((df['gdp_n'].ix[q2] / df['gdp_c'].ix[q2]) * 100) - np.log((
        df['gdp_n'].ix[q1] / df['gdp_c'].ix[q1]) * 100)

    imp_def_delta = np.log((df['imports_n'].ix[q2] / df['imports_c'].ix[q2]) * 100) - np.log((
        df['imports_n'].ix[q1] / df['imports_c'].ix[q1]) * 100)

    demand_delta = np.log(df['demand_c'].ix[q2]) - np.log(df['demand_c'].ix[q1])

    wedge = imp_delta - e * (gdp_def_delta - imp_def_delta) + demand_delta

    wedge = wedge.rename({'Euro area (17 countries)': 'EU17',
                'European Union (27 countries)': 'EU27',
                'Former Yugoslav Republic of Macedonia, the': 'Macedonia',
                'Germany (including  former GDR from 1991)': 'Germany'
                })
    return wedge

wedges = trade_wedge('2008-06-01', '2009-06-01')
wedges.order(ascending=False).plot(kind='barh')
