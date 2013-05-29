import ipdb
import cPickle
import itertools as it

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.covariance import EmpiricalCovariance, MinCovDet
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# Helper functions


class Results(object):
    """
    Collect some helpful functions for analyzing the results.
    """
    def __init__(self, ctry, weighted=True, close=True):
        self.country = ctry
        self.df = self.load_res(self.country)
        self.pre = None
        self.inliers = None
        self.outliers = None
        country_code = {'001': 'France',
                        '003': 'Netherlands',
                        '004': 'Fr Germany',
                        '005': 'Italy',
                        '006': 'Utd. Kingdom',
                        '007': 'Ireland',
                        '008': 'Denmark',
                        '009': 'Greece',
                        '010': 'Portugal',
                        '011': 'Spain',
                        '017': 'Belgium',
                        '018': 'Luxembourg',
                        '030': 'Sweden',
                        '032': 'Finland',
                        '038': 'Austria',
                        '046': 'Malta',
                        '053': 'Estonia',
                        '054': 'Latvia',
                        '055': 'Lithuania',
                        '060': 'Poland',
                        '061': 'Czech Republic',
                        '063': 'Slovakia',
                        '064': 'Hungary',
                        '066': 'Romania',
                        '068': 'Bulgaria',
                        '091': 'Slovenia',
                        '600': 'Cyprus',
                        'EU': 'EU'}
        self.name = country_code[self.country]

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Results_' + self.name

    def load_pre(self, close=True):
        """
        Get a dataframe with the trade data.
        """
        if self.pre is not None:
            return self.pre
        else:
            ctry = self.country
            base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
            gmm = pd.HDFStore(base + 'filtered_for_gmm.h5')
            df = gmm.select('ctry_' + ctry)
            if close:
                gmm.close()
            self.pre = df
            return df

    def load_res(self, ctry, weighted=True, close=True):
        """
        Get a dataframe with the estimated parameters for that country.
        """
        base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
        if weighted:
            gmm_res = pd.HDFStore(base + 'filtered_gmm_res/'
                                  'filtered_gmm_results_weighted.h5')
        else:
            gmm_res = pd.HDFStore(base + 'gmm_results.h5')
        df = gmm_res.select('transformed_' + ctry)
        if close:
            gmm_res.close()
        return df

    def get_extremes(self):
        """
        Get the dataframe of price and share who ended up giving
        the max and min values for theta1 and theta2.
        """
        df = self.df
        pre = self.load_pre()
        maxes = df.idxmax()
        mins = df.idxmin()
        rmax = [pre.xs(maxes[x], level='good') for x in maxes.index]
        rmin = [pre.xs(mins[x], level='good') for x in mins.index]
        return {'maxes': rmax, 'mins': rmin}

    def scatter_(self, df=None, inliers=False, ax=None, **kwargs):
        """
        Plot a scatter of the two parameters.  Give either a country code
        or a dataframe of estimated parameters.  If inliers, the dataframe
        will filter out the outliers.
        """
        ctry = self.country
        if inliers:
            df = self.get_inliers()
        else:
            df = self.df
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        ax.scatter(df.t1, df.t2, alpha=.67, marker='.', **kwargs)
        try:
            ax.set_title(self.name)
        except:
            ax.set_title(ctry)
        self.axes_scatter = ax
        return ax

    def get_outliers(self, s=3, how='any'):
        """
        Find all observations which are at least s (three) sigma for (all)
        or (any) of the features.
        """
        if self.outliers is not None:
            return self.outliers
        else:
            df = self.df
            if how == 'any':
                outliers = df[(np.abs(df) > df.std()).any(1)]
            elif how == 'all':
                outliers = df[(np.abs(df) > df.std()).all(1)]
            else:
                raise TypeError('how must be "any" or "all".')
            self.outliers = outliers
            return outliers

    def get_inliers(self, s=3, weighted=True, how='all'):
        """
        Get a subset of df with just inliers.  When how='any', this is the
        complement to get_outliers with how='all', and vice-versa.
        """
        if self.inliers is not None:
            return self.inliers
        else:
            df = self.df
            if how == 'any':
                inliers = df[(np.abs(df) <= df.mean() + s * df.std()).any(1)]
            elif how == 'all':
                inliers = df[(np.abs(df) <= df.mean() + s * df.std()).all(1)]
            else:
                raise TypeError('how must be "any" or "all".')
            self.inliers = inliers
            return inliers

    def mahalanobis_plot(self, inliers=False):
        """
        See http://scikit-learn.org/0.13/modules/outlier_detection.html#\
            fitting-an-elliptic-envelop

        for details.
        """
        if inliers:
            df = self.get_inliers()
        else:
            df = self.df
        X = df.values
        robust_cov = MinCovDet().fit(X)
        #---------------------------------------------------------------------------
        # compare estimators learnt from the full data set with true parameters
        emp_cov = EmpiricalCovariance().fit(X)
        #---------------------------------------------------------------------------
        # Display results
        fig = plt.figure()
        fig.subplots_adjust(hspace=-.1, wspace=.4, top=.95, bottom=.05)
        #---------------------------------------------------------------------------
        # Show data set
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.scatter(X[:, 0], X[:, 1], alpha=.5, color='k', marker='.')
        ax1.set_title(self.name)
        #---------------------------------------------------------------------------
        # Show contours of the distance functions
        xx, yy = np.meshgrid(np.linspace(ax1.get_xlim()[0], ax1.get_xlim()[1],
                                         100),
                             np.linspace(ax1.get_ylim()[0], ax1.get_ylim()[1],
                                         100))
        zz = np.c_[xx.ravel(), yy.ravel()]
        #---------------------------------------------------------------------------
        mahal_emp_cov = emp_cov.mahalanobis(zz)
        mahal_emp_cov = mahal_emp_cov.reshape(xx.shape)
        emp_cov_contour = ax1.contour(xx, yy, np.sqrt(mahal_emp_cov),
                                      cmap=plt.cm.PuBu_r,
                                      linestyles='dashed')
        #---------------------------------------------------------------------------
        mahal_robust_cov = robust_cov.mahalanobis(zz)
        mahal_robust_cov = mahal_robust_cov.reshape(xx.shape)
        robust_contour = ax1.contour(xx, yy, np.sqrt(mahal_robust_cov),
                                     cmap=plt.cm.YlOrBr_r, linestyles='dotted')
        ax1.legend([emp_cov_contour.collections[1], robust_contour.collections[1]],
                   ['MLE dist', 'robust dist'],
                   loc="upper right", borderaxespad=0)
        ax1.grid()
        return (fig, ax1, ctry)

    def hist_(self, ncuts=1000, inliers=False):
        """
        Histogram for a country.  This one is plots t1 and t2 side by side.
        """
        if inliers:
            df = get_inliers()
        else:
            df = self.df
        cuts = np.linspace(min(df.min()), max(df.max()), ncuts)
        cutted = [pd.cut(df.t1, bins=cuts), pd.cut(df.t2, bins=cuts)]
        cutted = [sorted(x) for x in cutted]
        s1, s2 = [pd.DataFrame(pd.value_counts(x, sort=False)) for x in cutted]
        s1.columns = ['t1']
        s2.columns = ['t2']
        joined = s1.join(s2, how='outer', sort=False).fillna(0)
        ax = joined.plot(kind='bar')
        ticks = ax.get_xticks()
        labels = ax.get_xticklabels()
        ticks = ticks[::10]  # Every other.
        labels = labels[::6]
        return ax

    def hist_2(self, ncuts=1000, thin=4, inliers=False):
        """
        Histogram for a country.  This one is plots t1 and t2 on separate subplots.
        """
        if inliers:
            df = get_inliers()
        else:
            df = self.df
        cuts = [np.linspace(df.min()[x], df.max()[x], ncuts) for x in ['t1', 't2']]
        cutted = [pd.cut(df.t1, bins=cuts[0]), pd.cut(df.t2, bins=cuts[1])]
        # cutted = [sorted(x) for x in cutted]
        s1, s2 = [pd.DataFrame(pd.value_counts(x, sort=False)) for x in cutted]
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        ax1 = s1.plot(kind='bar', ax=ax1, rot='45')
        ax2 = s2.plot(kind='bar', ax=ax2, rot='45')
        #-------------------------------------------------------------------------
        ticks = [ax1.get_xticks(), ax2.get_xticks()]
        ticks = [x[::thin] for x in ticks]  # Every other.
        #-------------------------------------------------------------------------
        ax1.set_xticks(ticks[0])
        ax2.set_xticks(ticks[1])
        return (ax1, ax2)

    @staticmethod
    def get_mid(ind):
        ind = ind.strip('(]').split(', ')
        return np.mean([float(x) for x in ind])

    @staticmethod
    def density_(df, n=100):
        x = pd.cut(df.t1, n)
        y = pd.cut(df.t2, n)
        x_counts = pd.value_counts(x)
        y_counts = pd.value_counts(y)
        x_mid = map(get_mid, x_counts.index)
        y_mid = map(get_mid, y_counts.index)
        lower = min(min(x_mid), min(y_mid))
        upper = max(max(x_mid), max(y_mid))
        arr = np.linspace(lower, upper, 100)
        grid = np.meshgrid(arr, arr)
        x_counts.index = x_mid
        y_counts.index = y_mid
        x_counts = x_counts.sort_index()
        y_counts = y_counts.sort_index()

    def select_level(self, level, inliers=False):
        """
        Use this function to get all goods at a particilar level, e.g. 2, 8.

        level: int
        """
        if inliers:
            df = self.get_inliers()
        else:
            df = self.df
        return df.ix[df.index.map(lambda x: len(x) == level)]

    def select_level_index(self, level, inliers=False):
        if inliers:
            df = self.get_inliers()
        else:
            df = self.df
        return np.unique(df.index.map(lambda x: x[:level]))

    def select_range(self, level, inliers=False):
        """
        Grab out a specific level at any level of aggregation.
        e.g. '02' for all items in that section.
        parameters
        -level: Str.

        returns
        -DataFrame. Subset of the original.
        """
        if inliers:
            df = self.get_inliers()
        else:
            df = self.df
        return df.ix[df.index.map(lambda x: x.startswith(level))]

    def most_pre(self, n=10):
        df = self.load_pre().reset_index()
        df['group'] = df.good.str.slice(stop=2)
        cts = df.groupby(['group']).count()['price'].copy()
        cts.sort()
        return cts[-10:]

    def color_scatter(self, n_levels=2, n_cats=10, inliers=False):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cycle = it.cycle(plt.rcParams['axes.color_cycle'])
        top = self.most_pre(n=n_cats)
        ipdb.set_trace()
        for level in top.index.intersection(self.select_level_index(
                                            n_levels, inliers=inliers)):
            x = self.select_range(level)
            ax = self.scatter_(df=x, ax=ax, inliers=inliers, label=level,
                               color=cycle.next())
        return ax

    def get_summary(self, inliers=False):
        if inliers:
            df = self.get_inliers()
        else:
            df = self.df
        return df.describe()

    def groupby_level(self, n=2, inliers=False):
        """
        Group your data (possibly adjusted for inliners) by a specific
        level of aggregation, e.g. 2.

        Retuerns a groupby object.
        """
        levels = self.select_level_index(n, inliers=inliers)
        levels = pd.DataFrame(levels, index=levels)
        if inliers:
            df = self.get_inliers()
        else:
            df = self.df
        levels = levels.reindex_axis(self.df.index, method='ffill')
        return df.groupby(levels[0])

    def truncated_hist(self, ax=None, tol=0.9975, bins=100, cols=None, **kwargs):
        """
        Data are skewed (left?) massively.
        
        BUG: Passing a list of cols makes pandas take over the axes handling.
        """
        if cols is None:
            cols = 't1'
        df = self.df[cols]
        df = df[df < df.quantile(tol)]
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        ax = df.hist(bins=bins, ax=ax)
        ax.set_title(self.name)
        return ax


class GroupPlot(object):
    def __init__(self, n_subplots=28):
        self.n_subplots = n_subplots
        base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
        with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
            self.country_code = cPickle.load(declarants)
            self.declarants = sorted(self.country_code.keys())
        self.results_store = {ctry: Results(ctry) for ctry in self.declarants}

    def make_plot(self, func, inliers=False, **kwargs):
        fig = plt.figure(figsize=(16, 9))
        grid = gridspec.GridSpec(4, self.n_subplots / 4)
        grid.update(hspace=0.5, wspace=0.7)
        for i, ctry in enumerate(self.results_store):
            res = self.results_store[ctry]
            row = int(np.floor(i / 7))
            ax = plt.subplot(grid[row, i - 7 * row])
            ax = getattr(res, func)(ax=ax, inliers=inliers, **kwargs)
            # ax = res.scatter_(ax=ax, inliers=inliers)
            ax.set_title(res.name, size=8)
            ax.grid(False)
            for i, tic in enumerate(
                    it.chain(ax.get_yticklabels(), ax.get_xticklabels())):
                tic.set_size(8)
                if i % 2 == 0:
                    tic.set_alpha(0)
            # ipdb.set_trace()
            print('added {}'.format(ctry))
        return fig, grid
