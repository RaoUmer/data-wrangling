import re


def nace_pc(l):
    """Take a list of nace industry names and get the pc code.
    """
    l2 = []
    for x in l:
        m = re.search('\d', x)
        if m and len(x) == 5:
            l2.append(x[1:])
    return l2
