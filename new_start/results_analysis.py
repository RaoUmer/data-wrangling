import cPickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Results import Results
# -----------------------------------------------------------------------------
# The fun
base = '/Volumes/HDD/Users/tom/DataStorage/Comext/yearly/'
with open(base + 'declarants_no_002_dict.pkl', 'r') as declarants:
    country_code = cPickle.load(declarants)
    declarants = sorted(country_code.keys())

countries = [Results(ctry) for ctry in declarants]
scatters = iter(ctry.scatter_() for ctry in countries)
scatters_adj = iter(ctry.scatter_(inliers=True) for ctry in countries)
mle = iter(ctry.mahalanobis_plot(ctry) for ctry in countries)
mle_adj = iter(ctry.mahalanobis_plot(inliers=True) for ctry in countries)
hists = iter(ctry.hist_() for ctry in countries)
hists2 = iter(ctry.hist_2() for ctry in countries)

# zipped = it.izip(mle_adj, declarants)
# for x, ctry in zipped:
#     plt.savefig('/Users/tom/Desktop/outliers/outlier{}.png'.format(ctry),
#                 dpi=400, format='png')

# #-----------------------------------------------------------------------------
# # Finding the outliers:

# lens = {}
# for country in declarants:
#     df = get_outliers(ctry=country)
#     lens[country] = len(df)
#     gmm_res.append('round_1_{}'.format(country), df)

#-----------------------------------------------------------------------------
# Color by level


colors = iter(ctry.color_scatter() for ctry in countries)
colors_adj = iter(ctry.color_scatter(inliers=True) for ctry in countries)
counts2 = (ctry.groupby_level().count() for ctry in countries)
means2 = (ctry.groupby_level().mean() for ctry in countries)
trunc_hists = iter(ctry.truncated_hist() for ctry in countries)

xs = []
for country in declarants:
    stats_ = Results(country).get_summary()['t1']
    stats_.name = country_code[country]
    xs.append(stats_)

sums = np.round(pd.concat(xs, axis=1), 2)
slices = [slice(*x) for x in [(0, 7), (7, 14), (14, 21), (21, 28)]]
for i, slice_ in enumerate(slices):
    with open('./writeup/summary_stats_{}.txt'.format(i), 'w') as f:
        (sums[sums.columns[slice_]]).to_latex(buf=f)
# or better
with open('./writeup/summary_stats.txt', 'w') as f:
    sums.T.to_latex(buf=f)

# as inliers
xs = []
for country in declarants:
    stats_ = Results(country).get_summary(inliers=True)['t1']
    stats_.name = country_code[country]
    xs.append(stats_)

sums = np.round(pd.concat(xs, axis=1), 2)
with open('./writeup/summary_stats_inliers.txt', 'w') as f:
    sums.T.to_latex(buf=f)

# Scatter Plots
cls = GroupPlot()
fig, grid = cls.make_plot('scatter_')
plt.savefig('./writeup/resources/scatter.png', dpi=400)

fig, grid = cls.make_plot('scatter_', inliers=True)
plt.savefig('./writeup/resources/inliers_scatter.png', dpi=400)

fig, grid = cls.make_plot('truncated_hist', inliers=True, tol=.95)
plt.savefig('./writeup/resources/histograms.png', dpi=400)
#-----------------------------------------------------------------------------
# Aggregate at two level and take the mean
xs = []
for ctry in countries:
    df = ctry.select_level(2)['t1']
    df.name = ctry.name
    xs.append(df)

means = np.round(pd.concat(xs, axis=1), 2).mean()

diff = sums.ix['mean'] - means
both = pd.DataFrame({'2-Digit-mean': means, 'Difference': diff})
with open('./writeup/level_two_means.txt', 'w') as f:
    both.to_latex(buf=f)
