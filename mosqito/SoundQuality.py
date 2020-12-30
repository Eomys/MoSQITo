# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:25:12 2020

@author: wantysal
"""
import sys
sys.path.append('..')

# Standard library import
import numpy as np

# import SciDataTool objects
from SciDataTool import Data1D, DataTime, DataFreq, DataLinspace

# import Mosqito functions
from mosqito.functions.shared.load import load
from mosqito.functions.shared.cut import cut_signal
from mosqito.functions.oct3filter.calc_third_octave_levels import calc_third_octave_levels
from mosqito.functions.oct3filter.oct3spec import oct3spec
from mosqito.functions.loudness_zwicker.loudness_zwicker_stationary import loudness_zwicker_stationary
from mosqito.functions.loudness_zwicker.loudness_zwicker_time import loudness_zwicker_time
from mosqito.functions.sharpness.sharpness_aures import comp_sharpness_aures
from mosqito.functions.sharpness.sharpness_din import comp_sharpness_din
from mosqito.functions.sharpness.sharpness_bismarck import comp_sharpness_bismarck
from mosqito.functions.sharpness.sharpness_fastl import comp_sharpness_fastl
from mosqito.functions.roughness_danielweber.comp_roughness import comp_roughness


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
        
    
    def import_signal(self, is_stationary, file, calib=1, mat_signal='', mat_fs='' ):
        """ Method to load the signal from a .wav .mat or .uff file
        
        Parameters
        ----------
        is_stationary : boolean
            TRUE if the signal is stationary, FALSE if it is time-varying
        file : string
            string path to the signal file
        calib : float
            calibration factor for the signal to be in [pa]
        mat_signal : string
            in case of a .mat file, name of the signal variable
        mat_fs : string
            in case of a .mat file, name of the sampling frequency variable

    
        Outputs
        -------
        signal : numpy.array
            time signal values
        fs : integer
            sampling frequency        
      
        """
        
        self.is_stationary = is_stationary
        values, self.fs = load(self.is_stationary, file, calib, mat_signal, mat_fs )
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

    def cut_signal(self, start, stop):
        """ Method to keep only the signal values between 'start' and 'stop'
        
        Parameters
        ----------
        start : float
            beginning of the new signal in [s]
        stop : float
            end of the new signal in [s]
        
        """
        
        self.signal.values = cut_signal(self.signal.values, self.fs, start, stop)
    
    def comp_3oct_spec(self):
        """ Method to compute third-octave spectrum according to ISO"""
        
        freqs = Data1D(
            name = 'freqs',
            unit = 'Hertz')        
        
        if self.is_stationary == True:
            third_spec, freqs.values = oct3spec(self.signal.values, self.fs)
            np.squeeze(third_spec)            
            self.third_spec = DataFreq(
            symbol = "3oct",
            axes = [freqs],
            values = third_spec,            
            name = "Third-octave spectrum",
            unit = "dB ref 2e-05")

                     
        elif self.is_stationary == False:    
            time = Data1D(
                name = 'time',
                unit = 's')
            third_spec, freqs.values, time.values = calc_third_octave_levels(self.signal.values, self.fs)
            np.squeeze(third_spec) 
            
            self.third_spec = DataFreq(
            symbol = "3oct",
            axes = [freqs, time],
            values = third_spec,            
            name = "Third-octave spectrum",
            unit = "dB ref 2e-05")

       
    
    def compute_loudness(self, field_type = 'free'):
        """ Method to compute the loudness according to Zwicker's method
        
        Parameter
        ----------
        field-type: string
            'free' by default or 'diffuse'      
               
        """
        if self.third_spec == None:
            self.comp_3oct_spec()
    
        if self.is_stationary == True:
            N, N_specific = loudness_zwicker_stationary(self.third_spec.values, self.third_spec.axes[0].values, field_type)
        elif self.is_stationary == False: 
            N, N_specific = loudness_zwicker_time(self.third_spec.values, field_type)
           
        barks = Data1D(
            name = 'Frequency Bark scale',
            unit = 'Bark', 
            values = np.linspace(0.1, 24, int(24 / 0.1)))
        
        if self.is_stationary == True:
            self.loudness = Data1D(
                values = [N],
                name = "Loudness",
                unit = "Sones"
                )
            self.loudness_specific = DataFreq(
                symbol = "N'",
                axes = [barks],
                values = N_specific,
                name = "Specific loudness",
                unit = "Sones"
                )
        elif self.is_stationary == False:
            time = Data1D(
                symbol = "T",
                name = "Time axis",
                unit = "s",
                values = np.linspace(0, len(self.signal.values)/self.fs, num = N.size))
            
            self.loudness = DataTime(
                symbol = "N",
                axes = [time],
                values = N,
                name = "Loudness",
                unit = "Sones"
                )
            self.loudness_specific = DataFreq(
                symbol = "N'",
                axes = [barks, time],
                values = N_specific,
                name = "Specific loudness",
                unit = "Sones"
                )

        
    def compute_sharpness(self, method = 'din', skip=0.2):        
        """ Method to cumpute the sharpness according to the given method
        
        Parameter
        ---------
        method: string
            'din' by default, 'aures', 'bismarck', 'fastl', 'all'
        skip : float
            number of second to be cut at the beginning of the analysis

        """
        if method!= 'din' and method!='aures' and method !='fastl' and method != 'bismarck':
            raise ValueError("ERROR: method must be 'din', 'aures', 'bismarck' or 'fastl")
       
        if self.loudness == None:
            self.compute_loudness()
        
    
        if method == 'din':
            S = comp_sharpness_din(self.loudness.values, self.loudness_specific.values, self.is_stationary )      
        
        elif method == 'aures':
            S = comp_sharpness_aures(self.loudness.values, self.loudness_specific.values, self.is_stationary ) 

        elif method == 'bismarck':
            S = comp_sharpness_bismarck(self.loudness.values, self.loudness_specific.values, self.is_stationary )                    

        elif method == 'fastl':
            S = comp_sharpness_fastl(self.loudness.values, self.loudness_specific.values, self.is_stationary ) 
                   
        
        if self.is_stationary == True:
            self.sharpness = Data1D(
                values = [S],
                name = "Sharpness",
                unit = "Acum"
                )
        elif self.is_stationary == False:
            # Cut transient effect
            time = np.linspace(0, len(self.signal.values)/self.fs, len(S))
            cut_index = np.argmin(np.abs(time - skip))
            S = S[cut_index:]
        
            time = Data1D(
                symbol = "T",
                name = "Time axis",
                unit = "s",
                values = np.linspace(skip, len(self.signal.values)/self.fs, num = S.size))
            
            self.sharpness = DataTime(
                symbol = "S",
                axes = [time],
                values = S,
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
        roughness = comp_roughness(self.signal.values, self.fs, overlap)
        
        time = Data1D(
            name = 'Time',
            unit = 's',
            values = roughness['time'])

        self.roughness = DataTime(
            symbol = "R",
            axes = [time],
            values = roughness['values'],
            name = "Roughness",
            unit = "Asper"
            )








