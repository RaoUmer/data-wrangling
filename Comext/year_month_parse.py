import datetime as dt


def year_month(x):
    ym = (int(str(x)[:4]), int(str(x)[-2:]))
    return dt.datetime(ym[0], ym[1], 1)
