import pandas as pd


def opt_dict_format(results, names, alt_columns=None):
    """Returns a tuple. For full results use joined.  For just the solution
    use
    """
    if alt_columns is None:
        alt_columns = ['success']
    joined = results.join(split_arrays(results['x'], names=names))
    return (joined, joined[names + alt_columns].convert_objects(convert_numeric=True))


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


def add_in_success(store):
    """
    This cleans up my ignorance from earlier.  I should not have included
    the failed optimiziations in the for_hdf5 store.
    """
    countries = {x.split('_')[1] for x in store.keys()}
    base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/gmm_res/ctry_'
    for country in countries:
        df = pd.read_csv(base + country + '.csv',
                         index_col=0)[['success', 't1', 't2']]
        store.remove('res_' + country)
        store.append('res_' + country, df)
