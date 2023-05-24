from numpy import argmax, flip, argsort, delete, int32, asarray, triu, tril, apply_along_axis, tile, where, nan, isnan, maximum, array
import matplotlib.pyplot as plt

def find_right_limit(a, maxima):
    
    idx = asarray(a>0).nonzero()[0]
    if len(idx) == 0:
        return 255
    else:
        return maxima[idx[0]]

def find_left_limit(a, maxima):

    idx = asarray(a>0).nonzero()[0]
    if len(idx) == 0:
        return 0
    else:
        return maxima[idx[-1]]
    
def find_left_valley(limits, Phi_E):
    return limits[1] - 1 - argmax(flip(Phi_E[limits[1]]-Phi_E[limits[0]:limits[1]]))

def find_right_valley(limits, Phi_E):
    return limits[0] + argmax(Phi_E[limits[0]]-Phi_E[limits[0]:limits[1]])


def _comp_prominence(Phi_E, maxima):
    """ 
    Function to compute the prominence value of the peak at index maxima[peak_nb] in the averaged spectrum Phi_E
    """
    if len(maxima) == 0:
        raise ValueError("ERROR: no maxima detected, impossible to compute the prominence.")
    
    else :
        T_right = triu(tile(Phi_E[maxima], (len(maxima),1))-Phi_E[maxima,None])
        right_limit = array(apply_along_axis(find_right_limit, axis=1, arr=where((T_right>0), T_right, 0), maxima=maxima), dtype=object)

        T_left = tril(tile(Phi_E[maxima], (len(maxima),1))-Phi_E[maxima,None])
        left_limit = array(apply_along_axis(find_left_limit, axis=1, arr=where((T_left>0), T_left, 0), maxima=maxima), dtype=object)

        # plt.figure()
        # plt.plot(Phi_E)
        # plt.plot(maxima, Phi_E[maxima], 'o')
        # plt.plot([left_limit, right_limit], [Phi_E[left_limit],Phi_E[right_limit]], 's')
        # plt.show() 


        # the limits of the interval are the closest neighbour peaks that are higher to the peak studied or the signal's
        peak_levels = Phi_E[maxima]

        # Left side   
        left_valley_idx = apply_along_axis(find_left_valley, axis=1, arr=[i for i in zip(left_limit, maxima)],Phi_E=Phi_E)
        left_valley =  peak_levels - Phi_E[left_valley_idx]

        # Right side
        right_valley_idx = apply_along_axis(find_left_valley, axis=1, arr=[i for i in zip(maxima, right_limit)], Phi_E=Phi_E)
        right_valley = peak_levels - Phi_E[right_valley_idx]

        prominence = maximum(left_valley, right_valley)


    return prominence

if __name__ == "__main__":

    import numpy as np

    a = np.array([5,1,3,0,2,6,4])
    aa = np.array([[5,1,3,0,2,6,4], [5,1,3,0,2,6,4],[5,1,3,0,2,6,4],[5,1,3,0,2,6,4],[5,1,3,0,2,6,4],[5,1,3,0,2,6,4],[5,1,3,0,2,6,4]])


    



