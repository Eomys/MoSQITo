# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 17:32:06 2020

@author: wantysal
"""

import numpy as np
    
def LTQ(bark_axis):
    """Calculate the level threshold in quiet over frequency axis in Hz
    
    Linear interpolation from the data given in E. Zwicker, H. Fastl:
    Psychoacoustics. Springer, Berlin, Heidelberg, 1990.
    SPL is given for a free-field condition relative to 2 × 10−5 Pa
    """
    
    # Make list of minimum excitation (Hearing Treshold)
    
    HTres_x = np.array(
        [ 0.00,  0.01,  0.17,  0.80,  1.00,  1.50,  2.00,  3.30,  4.00,  5.00,
          6.00,  8.00, 10.00, 12.00, 13.30, 15.00, 16.00, 17.00, 18.00, 19.00,
          20.00, 21.00, 22.00, 23.00, 24.00, 24.50, 25.00 ]
        )
        
    HTres_y = np.array(
        [130.00, 70.00, 60.00, 30.00, 25.00, 20.00,  15.00, 10.00,  8.10, 6.30,
            5.00,  3.50,  2.50,  1.70,  0.00, -2.50,  -4.00, -3.70, -1.50, 1.40,
            3.80,  5.00,  7.50, 15.00, 48.00, 60.00, 130.00 ]
        )
    
    # HTres_x = np.array([2.00e-02, 3.08064020e-02, 8.00e-01, 1.00e+00, 1.50e+00,
    #                     2.00e+00, 3.30e+00, 4.00e+00, 5.00e+00, 6.00e+00, 8.00e+00,
    #                     1.00e+01, 1.20e+01, 1.33e+01, 1.50e+01, 1.60e+01, 1.70e+01,
    #                     1.80e+01, 1.90e+01, 2.00e+01, 2.10e+01, 2.20e+01, 2.30e+01,
    #                     2.40e+01, 2.45e+01, 2.50e+01])
    
    # HTres_y = np.array([70. ,  60.30403 ,  30. ,  25. ,  20. ,  15. ,  10. ,   8.1,
    #                       6.3,   5. ,   3.5,   2.5,   1.7,   0. ,  -2.5,  -4. ,  -3.7,
    #                     -1.5,   1.4,   3.8,   5. ,   7.5,  15. ,  48. ,  60. , 130. ])
       
       
    MinExcdB = np.interp(bark_axis,HTres_x,HTres_y)
        
    return MinExcdB 