import datetime as dt


def year_month(x):
    ym = (int(str(x)[:4]), int(str(x)[-2:]))
    return dt.datetime(ym[0], ym[1], 1)


def year(x):
    y = int(str(x)[:4])
    return dt.datetime(y, 01, 1)
