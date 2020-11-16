# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 10:47:56 2020

@author: wantysal
"""
import numpy as np

def a0_definition(bark_axis):
    """ Zwicker's a0 coefficients representing the transmission between
    free field and the peripheral hearing system.
    
    The coefficients meaning is described in detail in E. Zwicker, H. Fastl:
    Psychoacoustics. Springer, Berlin, Heidelberg, 1990.
    The coefficients are interpolated from the values given in figure 8.18.
    
    Parameter
    ---------
    bark_axis : numpy.array
                frequencies where to calculate a0 in bark
    
    Output
    ------
    A0 : numpy.array
          coeffcient values along the given bark_axis
    
    """
   
    xp = [0,          8.589759,   9.202893,  9.879537, 10.3658,   10.894279, 
          11.486193, 11.972306,  12.479491, 13.092401, 13.578366, 13.93761, 
          14.317924, 14.740527,  15.163206, 15.54352,  15.945054, 16.410246,
          16.875364, 17.34078,   17.95451,  18.568613, 19.564072, 19.9665,  
          20.559309, 21.215328,  21.744701, 22.274446, 22.76235,  22.996138,
          23.208857, 23.4008,    23.571081, 23.720438, 24]

    
    yp = [0,         0,          -0.00542723,-0.023471035, -0.19643776, 
         -0.53053,  -0.86631376, -1.3592759, -2.0127997,   -2.669143, 
         -3.4821007,-3.9716797,  -4.6218204, -5.2730885,   -5.7643595,  
         -6.4144998,-6.9052067,  -6.9176116, -7.0900145,   -6.6224265, 
         -5.5187945,-3.6151738,  -0.12172516, 1.307541,     2.89173,    
         3.9942343,  5.5801153,   7.965985,  11.312968,    13.86673,  
         16.581053, 20.095928,   22.491383,  25.367395,    30]
    
    A0 = np.interp(bark_axis,xp,yp)
    
    # plot
    
    # plt.figure(figsize=(12,4))
    # plt.plot(bark_axis,A0,color='blue')
    # plt.xlabel('Frequency')
    # plt.ylabel('a0 coefficient')
    # plt.title('Zwicker coefficient representing the transmission between free field and hearing system')
    # plt.xticks([0,4,8,12,16,20,24])
    
    
    return A0