import numpy as np


def winsorize(df, cols='all'):
    """Replace > 3sigma obs with 3sigma.  cols is a list of col names.
    """
    wins = pd.DataFrame(df.copy())
    if cols == 'all':
        try:
            columns = df.columns
        except AttributeError:
            columns = [df.name]
    else:
        columns = cols
    for col in columns:
        std_w = wins.std()[col]
        if std_w == 0:
            continue
        cap_level = 3 * np.sign(wins[col]) * std_w
        wins[col][np.abs(wins[col]) > 3 * std_w] = cap_level
    return wins
