import cPickle
import itertools as it

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


levels = select_level_index(2, ctry='001')
for country in declarants:
    df = load_res(ctry=country)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cycle = it.cycle(plt.rcParams['axes.color_cycle'])
    top = most_pre(ctry=country)
    for level in top.index.intersection(levels):
        x = select_range(level, df=df)
        scatter_(df=x, ax=ax, color=cycle.next(), label=level)
