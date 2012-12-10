from __future__ import division

import numpy as np
import matplotlib.pyplot as plt


def heatmap(df, a=4, cmap=plt.cm.gray_r):
    """Returns a plot showing the intensity of a good's use in
    the other axis' industries.

    Parameters:
    df: dataframe (see notes below)
    a: Thinning paramets.  Plots a label for every ath item.
    cmap: colormap

    Call like:
    for country in df.index.levels[0]:
    try:
        heatmap(np.log(df.ix[country]))
    except:
        pass
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    axim = ax.imshow(df.values, cmap=cmap, interpolation='nearest')
    ax.set_xlabel(df.columns.name)
    ax.set_xticks(a * np.arange(len(df.columns) / a))
    ax.set_xticklabels(list(df.columns))
    ax.set_ylabel(df.index.name)
    ax.set_yticks(a * np.arange(len(df.index) / a))
    ax.set_yticklabels(list(df.index))
    plt.colorbar(axim)

