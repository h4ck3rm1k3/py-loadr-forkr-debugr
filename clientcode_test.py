# 
import pandas as pd

import numpy as np

import matplotlib.pyplot as plt
import sys
import pprint

global_data = None

def test_series():
    m = sys.modules[__name__]
    print "in series test"
    print "glob", m.__dict__['global_data']
    print "Global", global_data
#    pprint.pprint( m._xdata_ )

    s = pd.Series([1,3,5,np.nan,6,8])
