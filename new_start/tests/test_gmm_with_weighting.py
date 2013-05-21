from __future__ import division

from ..gmm_with_weighting import (weight_matrix, gen_moms_sse, gen_params,
                                  weight_array, diff_q)
import numpy as np
import pandas as pd


class test_gmm_weighting(object):
    """
    """
    def __init__(self):
        with pd.get_store('/Volumes/HDD/Users/tom/DataStorage/'
                          'Comext/yearly/for_gmm.h5') as f:
            df = f.select('ctry_001')
            df = df.dropna()
            df = df[~(df == np.inf)]
            self.data = df.xs('01', level='good')

    def test_data_loaded(self):
        assert len(self.data) == 594

    def test_weight_array(self, T=3):
        expected = np.array([T * (3/10) ** (-1/2),
                             T * (3/10) ** (-1/2),
                             T * (2/15) ** (-1/2)])
        pass

    def test_diff_q(self):
        var = pd.Series(np.arange(1, 5))
        expected = pd.Series([1.0, 1.0, .5, 1/3.])
        assert (diff_q(var) == expected).all()
