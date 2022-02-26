import numpy as np


def _get_rns_index(array_nm, vector_rns, equal_too=False):
    """Function that returns the index in the array vector_rns for each value of srray _nm

    Parameters
    ----------
    array_nm : numpy.ndarray, values of the matrix toget the indexes

    vector_rns:reference vector to get indexes
    equal_too : boolean

    Outputs
    -------
    indexes :  numpy.ndarray
        Array of indexes
    """

    if len(array_nm.shape) == 1:
        (wide,) = array_nm.shape
        (deep,) = vector_rns.shape
        array_aux = np.round(np.tile(array_nm, [deep, 1]), 8)
        rns_array = np.round(np.ones([wide, deep]) * vector_rns, 8).T
    else:
        wide, length = array_nm.shape
        (deep,) = vector_rns.shape
        array_aux = np.round(np.tile(array_nm, [deep, 1, 1]), 8)
        rns_array = np.round((np.ones([wide, length, deep]) * vector_rns), 8).transpose(
            2, 0, 1
        )
        # indexes = (array_aux < rns_array).sum(axis=0)
        # indexes[indexes==18] = 17
    if equal_too:
        indexes = (array_aux <= rns_array).sum(axis=0)
    else:
        indexes = (array_aux < rns_array).sum(axis=0)
    indexes[indexes == 18] = 17

    return indexes
