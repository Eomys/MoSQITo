from numpy import log10

def amp2db(amp, ref=1):
    """ Amplitude conversion into dB
    
    This function converts an amplitude signal into dB with the given reference value.

    Parameters
    -----------
    amp: array_like
        Amplitude values to be converted.
    ref: float
        Reference value.
        
    Returns
    --------
    db: array_like
        Values in dB.

    """
    if ref == 0:
        raise ValueError("Reference must be different from 0")
    elif ref != 0:
        ind = amp == 0
        amp[ind] = 2e-12  # To warning "divide by zero encountered in log10"
        db = 20 * log10(amp / ref)

    return db