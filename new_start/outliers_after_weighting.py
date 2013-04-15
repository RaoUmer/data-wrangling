import cPickle
from itertools import izip

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.font_manager
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.covariance import EmpiricalCovariance, MinCovDet, EllipticEnvelope
#-----------------------------------------------------------------------------
base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
    country_code = cPickle.load(declarants)
    declarants = sorted(country_code.keys())

gmm_res = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
                      'gmm_results.h5')
#-----------------------------------------------------------------------------
# Helper functions


def load_pre(ctry, close=True):
    gmm = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
                      'gmm_store.h5')
    df = gmm.select('by_ctry_' + ctry)
    if close:
        gmm.close()
    return df


def load_res(ctry, close=True):
    gmm_res = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
                          'gmm_results.h5')
    df = gmm_res.select('res_' + ctry)
    if close:
        gmm_res.close()
    return df


def grabber(pre=None, res=None, ctry=None):
    """
    Get the dataframe of price and share who ended up giving
    the max and min values for theta1 and theta2.
    """
    if pre is None:
        try:
            pre = load_pre(ctry)
        except NameError:
            raise NameError('You Need to give a country code')
    if res is None:
        res = load_res(ctry)
    maxes = res.idxmax()
    mins = res.idxmin()
    rmax = [pre.xs(maxes[x], level='PRODUCT_NC') for x in maxes.index]
    rmin = [pre.xs(mins[x], level='PRODUCT_NC') for x in mins.index]
    return {'maxes': rmax, 'mins': rmin}


def scatter_(ctry):
    df = load_res(ctry)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(df.t1, df.t2, alpha=.67, marker='.')
    try:
        ax.set_title(country_code[ctry])
    except:
        ax.set_title(ctry)
    return ax


def get_outliers(df=None, ctry=None, s=3, how='any'):
    """
    Find all observations which are at least s (three) sigma for (all)
    or (any) of the features.
    """
    if df is None:
        df = load_res(ctry)
    if how == 'any':
        return df[(np.abs(df) > df.std()).any(1)]
    elif how == 'all':
        return df[(np.abs(df) > df.std()).all(1)]
    else:
        raise TypeError('how must be "any" or "all".')


def get_inliers(df=None, ctry=None, s=3, how='any'):
    """
    Get a subset of df with just inliers.  When how='any', this is the
    complement to get_outliers with how='all', and vice-versa.
    """
    if df is None:
        df = load_res(ctry)
    if how == 'any':
        return df[(np.abs(df) <= df.std()).any(1)]
    elif how == 'all':
        return df[(np.abs(df) <= df.std()).all(1)]
    else:
        raise TypeError('how must be "any" or "all".')


def mahalanobis_plot(ctry=None, df=None):
    if df and ctry is None:
        raise ValueError('Either the country or a dataframe must be supplied')
    elif df is None:
        df = load_res(ctry)
    X = df.values

    robust_cov = MinCovDet().fit(X)

    # compare estimators learnt from the full data set with true parameters
    emp_cov = EmpiricalCovariance().fit(X)

    # Display results
    fig = plt.figure()
    fig.subplots_adjust(hspace=-.1, wspace=.4, top=.95, bottom=.05)

    # Show data set
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.scatter(X[:, 0], X[:, 1])
    ax1.set_title(country_code[ctry])

    # Show contours of the distance functions
    xx, yy = np.meshgrid(np.linspace(ax1.get_xlim()[0], ax1.get_xlim()[1],
                                     100),
                         np.linspace(ax1.get_ylim()[0], ax1.get_ylim()[1],
                                     100))
    zz = np.c_[xx.ravel(), yy.ravel()]

    mahal_emp_cov = emp_cov.mahalanobis(zz)
    mahal_emp_cov = mahal_emp_cov.reshape(xx.shape)
    emp_cov_contour = ax1.contour(xx, yy, np.sqrt(mahal_emp_cov),
                                  cmap=plt.cm.PuBu_r,
                                  linestyles='dashed')

    mahal_robust_cov = robust_cov.mahalanobis(zz)
    mahal_robust_cov = mahal_robust_cov.reshape(xx.shape)
    robust_contour = ax1.contour(xx, yy, np.sqrt(mahal_robust_cov),
                                 cmap=plt.cm.YlOrBr_r, linestyles='dotted')
    ax1.legend([emp_cov_contour.collections[1], robust_contour.collections[1]],
               ['MLE dist', 'robust dist'],
               loc="upper right", borderaxespad=0)
    ax1.grid()
    return (fig, ax1, ctry)


def hist_(df=None, ctry=None, ncuts=1000):
    if df is None:
        df = load_res(ctry)
    cuts = np.linspace(min(df.min()), max(df.max()), ncuts)
    cutted = [pd.cut(df.t1, bins=cuts), pd.cut(df.t2, bins=cuts)]
    cutted = [sorted(x) for x in cutted]
    s1, s2 = [pd.DataFrame(pd.value_counts(x, sort=False)) for x in cutted]
    s1.columns = ['t1']
    s2.columns = ['t2']
    joined = s1.join(s2, how='outer', sort=False)
    ax = joined.plot(kind='bar')
    ticks = ax.get_xticks()
    labels = ax.get_xticklabels()
    ticks = ticks[::2]  # Every other.
    labels = labels[::6]
    return ax


def hist_2(df=None, ctry=None, ncuts=1000, thin=4):
    if df is None:
        df = load_res(ctry)
    cuts = [np.linspace(df.min()[x], df.max()[x], ncuts) for x in ['t1', 't2']]
    cutted = [pd.cut(df.t1, bins=cuts[0]), pd.cut(df.t2, bins=cuts[1])]
    # cutted = [sorted(x) for x in cutted]
    s1, s2 = [pd.DataFrame(pd.value_counts(x, sort=False)) for x in cutted]
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1 = s1.plot(kind='bar', ax=ax1, rot='45')
    ax2 = s2.plot(kind='bar', ax=ax2, rot='45')

    ticks = [ax1.get_xticks(), ax2.get_xticks()]
    ticks = [x[::thin] for x in ticks]  # Every other.

    ax1.set_xticks(ticks[0])
    ax2.set_xticks(ticks[1])
    return (ax1, ax2)
    

#-----------------------------------------------------------------------------
# The fun
scatters = iter(scatter_(ctry) for ctry in declarants)
mahalas = iter(mahalanobis_plot(ctry) for ctry in declarants)
hists = iter(hist_(ctry=country) for country in declarants)
hists2 = iter(hist_2(ctry=country) for country in declarants)
outliers = iter(get_outliers(ctry=country) for country in declarants)
inliers = iter(get_inliers(ctry=country) for country in declarants)

zipped = izip(g2, declarants)
for x, ctry in zipped:
    plt.savefig('/Users/tom/Desktop/outliers/outlier{}.png'.format(ctry),
                dpi=400, format='png')

for ctry in declarants:
    res = gmm_res.select('res_' + ctry)
    res = res.drop(get_outliers(res).index)
    mahalanobis_plot(ctry, df=res)
#-----------------------------------------------------------------------------
# Assert: NotImplemented!
# res1 = gmm_res.select('res_001')
# X = res1.values


# outliers_fraction = 0.005
# n_samples = len(X)


# # define two outlier detection tools to be compared
# classifiers = {
#     "One-Class SVM": svm.OneClassSVM(nu=0.95 * outliers_fraction + 0.05,
#                                      kernel="rbf", gamma=0.1),
#     "robust covariance estimator": EllipticEnvelope(contamination=.1)}

# # Compare given classifiers under given settings
# xl, yl = res1.min().values
# xh, yh = res1.max().values
# xx, yy = np.meshgrid(np.linspace(xl, xh, 1000),
#                      np.linspace(yl, yh, 1000))
# n_inliers = int((1. - outliers_fraction) * n_samples)
# n_outliers = int(outliers_fraction * n_samples)
# # ground_truth = np.ones(n_samples, dtype=int)
# # ground_truth[-n_outliers:] = 0

# # Fit the problem with varying cluster separation

# # Fit the model with the One-Class SVM
# fig = plt.figure(figsize=(10, 5))
# for i, (clf_name, clf) in enumerate(classifiers.iteritems()):
#     # fit the data and tag outliers
#     clf.fit(X)
#     y_pred = clf.decision_function(X).ravel()
#     threshold = stats.scoreatpercentile(y_pred,
#                                         100 * outliers_fraction)
#     y_pred = y_pred > threshold
#     # n_errors = (y_pred != ground_truth).sum()
#     # plot the levels lines and the points
#     Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#     ax = fig.add_subplot(1, 2, i + 1)
#     ax.set_title("Outlier detection")
#     ax.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7),
#                 cmap=pl.cm.Blues_r)
#     a = ax.contour(xx, yy, Z, levels=[threshold],
#                    linewidths=2, colors='red')
#     ax.contourf(xx, yy, Z, levels=[threshold, Z.max()],
#                 colors='orange')
#     b = ax.scatter(X[:, 0], X[:, 1], c='black', alpha=.75)
#     ax.axis('tight')
#     # ax.legend(
#     #     ['learned decision function', 'true inliers', 'true outliers'],
#     #     prop=matplotlib.font_manager.FontProperties(size=11))

