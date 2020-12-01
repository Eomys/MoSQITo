# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:25:12 2020

@author: wantysal
"""
# import SciDataTool objects
from SciDataTool import Data1D, DataTime, DataFreq, DataLinspace

# import Mosqito functions
from mosqito.signal.load import load
from mosqito.oct3filter.comp_third_spectrum import comp_third_spec
from mosqito.loudness_zwicker.comp_loudness import comp_loudness
from mosqito.sharpness.comp_sharpness import comp_sharpness
from mosqito.roughness_danielweber.comp_roughness import comp_roughness


class SoundQuality():
    """ Audio signal loading and analysis: from .wav or .uff files compute 
    loudness, sharpness and roughness values thanks to the Mosqito package,
    Results plotting thanks to the SciDataTool package. """
    

    def __init__(self):
        """Constructor of the class."""
        
        self.signal = None
        self.is_stationary = bool()
        self.fs = int()
        self.time_axis = None
        self.third_spec = None
        self.loudness = None
        self.loudness_specific = None
        self.sharpness = None
        self.roughness = None
        self.roughness_specific = None
        
    
    def import_signal(self, is_stationary, file, calib=1 ):
        """ Method to load the signal from a .wav or .uff file
        
        Parameters
        ----------
        is_stationary : boolean
            TRUE if the signal is stationary, FALSE if it is time-varying
        file : string
            string path to the signal file
        calib : float
            calibration factor for the signal to be in [pa]
    
        Outputs
        -------
        signal : numpy.array
            time signal values
        fs : integer
            sampling frequency        
      
        """
        
        self.is_stationary = is_stationary
        values, self.fs = load(self.is_stationary, file, calib=1 )
        self.signal = Data1D(
            values = values,
            name = "Audio signal",
            unit = 'Pa'
            )
        
        self.time_axis = DataLinspace(
            initial = 0,
            final = len(self.signal.values)/self.fs,
            step = 1/self.fs,
            )

    
    def comp_3oct_spec(self):
        """ Method to compute third-octave spectrum according to ISO"""
        
        third_axis = Data1D(
            name = 'Third-octave frequency axis',
            unit = 'Hertz')
        
        third_spec, third_axis.values = comp_third_spec(self.is_stationary, self.signal.values, self.fs)
        
        self.third_spec = DataFreq(
            symbol = "3oct",
            axes = [third_axis],
            values = third_spec,            
            name = "Third-octave spectrum",
            unit = "dB ref 2e-05",
            normalizations={"ref":1e-12})
    
    def compute_loudness(self, field_type = 'free'):
        """ Method to compute the loudness according to Zwicker's method
        
        Parameter
        ----------
        field-type: string
            'free' by default or 'diffuse'
        
               
        """
        bark_axis = Data1D(
            name = 'Frequency Bark scale',
            unit = 'Bark')

        N, N_spec, bark_axis.values = comp_loudness(
            self.is_stationary, 
            self.third_spec.values, 
            self.third_spec.axes[0].values, 
            field_type)
        
        self.loudness = Data1D(
            values = [N],
            name = "Loudness",
            unit = "Sones"
            )
        self.loudness_specific = DataFreq(
            symbol = "N'",
            axes = [bark_axis],
            values = N_spec,
            name = "Specific loudness",
            unit = "Sones"
            )

        
    def compute_sharpness(self, method = 'din'):        
        """ Method to cumpute the sharpness according to the given method
        
        Parameter
        ---------
        method: string
            'din' by default, 'aures', 'bismarck', 'fastl'
        """
        
        S = comp_sharpness(self.signal.values, self.fs)
        self.sharpness = Data1D(
            values = [S],
            name = "Sharpness",
            unit = "Acum"
            )


    def compute_roughness(self, overlap=0):
        """ Method to compute roughness according to the Daniel and Weber implementation
        
        Parameter
        ---------
        overlap: float
            overlapping coefficient for the time windows of 200ms 
        """
        freqs = Data1D(
            name = 'Frequency Bark scale',
            unit = 'Bark')
        
        time = Data1D(
            name = 'Time',
            unit = 's')

        R, R_spec,time.values, freqs.values = comp_roughness(self.signal.values, self.fs, overlap)

        self.roughness = DataTime(
            axes = [time],
            values = R,
            name = "Roughness",
            unit = "Asper"
            )

        self.roughness_specific = DataTime(
            axes = [time, freqs],
            values = R_spec,
            name = "Specific roughness",
            unit = "Asper"
            )






