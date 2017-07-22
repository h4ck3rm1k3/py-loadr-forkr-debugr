from __future__ import print_function
#from six import print_ as print
__global_test_data__=None
 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import pprint


def test_series():
    m = sys.modules[__name__]
    print ("in series test")
    print ("glob", m.__dict__['__global_test_data__'])
    print ("Global", __global_test_data__)
#    pprint.pprint( m._xdata_ )

 #   s = pd.Series([1,3,5,np.nan,6,8])
