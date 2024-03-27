from numpy import power

def db2amp(dB, ref=1):
    """Linearisation of a SPL level in dB
    
    This function linearizes a dB signal into a SPL amplitude signal.

    Parameters
    ----------
    dB : array_like
        dB values to be converted.
    ref: float
        Reference value.
        
    Returns
    --------
    amp : array_like
        Linearized amplitude values.
    """
    if ref == 0:
        raise ValueError("Reference must be different from 0")

    return power(10, 0.05 * dB) * ref