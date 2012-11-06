import datetime as dt


def year_month(x):
    ym = (int(str(x)[:4]), int(str(x)[-2:]))
    return dt.datetime(ym[0], ym[1], 1)


def year_quarter(x):
    year, quarter = (int(x[:4]), int(x[-1]) * 3)
    return dt.datetime(year, quarter, 1)
