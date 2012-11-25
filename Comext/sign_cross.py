import os
from cPickle import load
from datetime import datetime
import numpy as np
import pandas as pd
from get_reference2 import get_reference


"""
Idea is to use the existing tables in gmm_store, and the
numpy.sign() function to get the signs correct.
"""

yearly = pd.HDFStore('yearly.h5')
gmm_store = pd.HDFStore('gmm_store.h5')

with open('declarants_no_002_dict.pkl', 'r') as f:
    declarants = load(f)
f.closed
declarants.pop('EU')  # Error w/ shares on EU.

years = [2007, 2008, 2009, 2010, 2011]

