import datetime as dt


def year_month(x):
    ym = (int(str(x)[:4]), int(str(x)[-2:]))
    return dt.datetime(ym[0], ym[1], 1)


def year_quarter(x):
    year, quarter = (int(x[:4]), int(x[-1]) * 3)
    return dt.datetime(year, quarter, 1)


def quarter_datetime(x):
    """convert '2012Q3' -> good format
    """
    q_to_m = {'1': 3,
            '2': 6,
            '3': 9,
            '4': 12}
    l = x.split('Q')
    return dt.datetime(int(l[0]), q_to_m[l[1]], 1)


if __name__ == '__main__':
    pass
