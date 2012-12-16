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


def cn_nace(x, to='nace'):
    """
    To move from CN to NACE nomenclature via:
    cn12 <-> cn11 <-> PRODCOM <- NACE

    Check length for 2 v 4 v 6 v 8 digits.
    """
    def space(x):
        if len(x) == 8:
            return ' '.join([x[:4], x[4:6], x[6:]])
        else:
            return x
