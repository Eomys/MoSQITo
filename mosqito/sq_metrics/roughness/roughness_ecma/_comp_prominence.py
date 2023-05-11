from numpy import argmax, flip, argsort, delete, int32

def _comp_prominence(Phi_E, maxima, peak_nb):
    """ 
    Function to compute the prominence value of the peak at index maxima[peak_nb] in the averaged spectrum Phi_E
    """

    if len(maxima) == 0:
        raise ValueError("ERROR: no maxima detected, impossible to compute the prominence.")


    if len(maxima) == 1:
        # since there is only one peak, the limits of the interval where to search for the maximum valley are the signal's ones
        # left side
        left_limit = 0 
        left_valley_idx = maxima[0] - argmax(flip(Phi_E[maxima[0]]-Phi_E[left_limit:maxima[0]]))
        left_valley =  Phi_E[maxima[0]] - Phi_E[left_valley_idx]
        # right side
        right_limit = 255 # sb
        right_valley_idx = argmax(Phi_E[maxima[0]]-Phi_E[maxima[0]:right_limit])
        right_valley = Phi_E[maxima[0]] - Phi_E[right_valley_idx]

        if left_valley > right_valley:
            prominence = [left_valley]
        else:
            prominence = [right_valley]

    elif len(maxima) > 1:
        # the limits of the interval are the closest neighbour peaks that are higher to the peak studied or the signal's
        peak_level = Phi_E[maxima[peak_nb]]
        # Left side
        crossing = False
        offset = 1    
        while crossing == False: 
            if (peak_nb == 0) or ((peak_nb-offset) < 0): # first peak or no more peak at the left
                crossing = True # left limit of the signal
                left_limit = 0
            elif Phi_E[maxima[peak_nb-offset]] > peak_level:
                crossing = True
                left_limit = maxima[peak_nb-offset]
            else:
                offset += 1     
        left_valley_idx = maxima[peak_nb] - 1 - argmax(flip(Phi_E[maxima[peak_nb]]-Phi_E[left_limit:maxima[peak_nb]]))
        left_valley =  peak_level - Phi_E[left_valley_idx]

        # Right side
        crossing = False
        offset = 1
        while crossing == False:
            if (peak_nb == len(maxima)) or ((peak_nb+offset)>=len(maxima)): # last peak or no more peak at the right
                crossing = True # right limit of the signal
                right_limit = 255 #CBF=53
            elif Phi_E[maxima[peak_nb+offset]] > peak_level:
                crossing = True
                right_limit = maxima[peak_nb+offset]
            else:
                offset += 1
        right_valley_idx = maxima[peak_nb] + argmax(peak_level-Phi_E[maxima[peak_nb]:right_limit])
        right_valley = peak_level - Phi_E[right_valley_idx]

        # Set prominence values
        if left_valley > right_valley:
            prominence = left_valley
        else:
            prominence = right_valley

    return prominence
