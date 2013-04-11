import pandas as pd


def opt_dict_format(results, names):
    """Returns a tuple. For full results use joined.  For just the solution
    use
    """
    joined = results.join(split_arrays(results['x'], names=names))
    return (joined, joined[names])


def split_arrays(column, names):
    """
    Split a Series containing values like [x1, x2] into two columns

    Parameters
    ----------
    column: Series or column from DataFrame
    names: list of column names to use in new DataFrame

    Returns
    -------
    DataFrame whose columns are the split array from column.
    """
    list_ = [[x[0], x[1]] for x in column.values]
    return pd.DataFrame(list_, columns=names, index=column.index)
