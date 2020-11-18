# -*- coding: utf-8 -*-
from pandas import ExcelFile, read_excel
from numpy import squeeze, zeros, transpose

def read_spectro_xls(file_name):
    """Read spectrogram as an xls file, format: A3:AN = time, B3:BN = speed, 
    C1:ZZ1 = DC, C2:ZZ2 = orders, C3:ZZN = spectrum
    and compute the frequencies

    Parameters
    ----------
    file_name : str
        name of the xls file

    Outputs
    -------
    spectrum : ndarray
        2D array of the spectrum
    freqs : array
        1D array of the computed frequencies
    time : array
        1D array of the time
    """
    
    xls_file = ExcelFile(file_name)
    
    # Read excel file
    spectrum = transpose(read_excel(xls_file, sheet_name="Sheet1", header=None, skiprows=2, usecols = 'C:ZZ', squeeze=True).to_numpy())
    time = squeeze(read_excel(xls_file, sheet_name="Sheet1", header=None, skiprows=2, usecols = 'A', squeeze=True).to_numpy())
    speed = squeeze(read_excel(xls_file, sheet_name="Sheet1", header=None, skiprows=2, usecols = 'B', squeeze=True).to_numpy())
    DC = squeeze(read_excel(xls_file, sheet_name="Sheet1", header=None, nrows=1, usecols = 'C:ZZ', squeeze=True).to_numpy())
    orders = squeeze(read_excel(xls_file, sheet_name="Sheet1", header=None, skiprows=1, nrows=1, usecols = 'C:ZZ', squeeze=True).to_numpy())
    
    # Compute frequencies
    freqs = zeros(spectrum.shape)
    for i in range(len(DC)):
        freqs[i,:] = DC[i] + orders[i] * speed / 60
    
    return spectrum, freqs, time
