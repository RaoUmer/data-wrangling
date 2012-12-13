import re
import os

import cPickle

with open('nace_list.pkl') as f:
    l = cPickle.load(f)

"""
Plan is to check for ending in alpha-numeric, go from there.
"""

for i in l:
    match = re.search('\d', i)
    if match:
        print i[1:]
