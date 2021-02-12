# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:25:12 2020

@author: wantysal
"""
import sys
sys.path.append('..')

# Standard library import
import numpy as np
import matplotlib.pyplot as plt

# import SciDataTool objects
from SciDataTool import Data1D, DataTime, DataFreq, DataLinspace

# import Mosqito functions
from mosqito.functions.shared.load import load
from mosqito.functions.shared.cut import cut_signal
from mosqito.functions.shared.A_weighting import A_weighting
from mosqito.functions.oct3filter.calc_third_octave_levels import calc_third_octave_levels
from mosqito.functions.oct3filter.oct3spec import oct3spec
from mosqito.functions.loudness_zwicker.loudness_zwicker_stationary import loudness_zwicker_stationary
from mosqito.functions.loudness_zwicker.loudness_zwicker_time import loudness_zwicker_time
from mosqito.functions.sharpness.sharpness_aures import comp_sharpness_aures
from mosqito.functions.sharpness.sharpness_din import comp_sharpness_din
from mosqito.functions.sharpness.sharpness_bismarck import comp_sharpness_bismarck
from mosqito.functions.sharpness.sharpness_fastl import comp_sharpness_fastl
from mosqito.functions.roughness_danielweber.comp_roughness import comp_roughness
from mosqito.functions.tonality_tnr_pr.comp_tnr import comp_tnr
from mosqito.functions.tonality_tnr_pr.comp_pr import comp_pr

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
        self.third_spec_db = None
        self.third_spec_dba = None
        self.level_db = None
        self.level_dba = None
        self.loudness_zwicker = None
        self.loudness_zwicker_specific = None
        self.sharpness_aures = None
        self.sharpness_bismarck = None
        self.sharpness_din = None
        self.sharpness_fastl = None
        self.roughness_dw = None
        self.tonality_tnr = None
        self.tonality_pr = None
        
    
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
    
    def comp_3oct_spec(self, unit='dB'):
        """ Method to compute third-octave spectrum according to ISO
        
        Parameter
        ---------
        unit : string
            'dB' or 'dBA'        
        
        """
        
        freqs = Data1D(
            name = 'freqs',
            unit = 'Hertz')        
        
        if self.is_stationary == True:
            third_spec, freqs.values = oct3spec(self.signal.values, self.fs)
            np.squeeze(third_spec)            
            self.third_spec_db = DataFreq(
                symbol = "3oct",
                axes = [freqs],
                values = third_spec,            
                name = "Third-octave spectrum",
                unit = "dB ref 2e-05")
            
            if unit == 'dBA':
                self.third_spec_dba = DataFreq(
                    symbol = "3oct",
                    axes = [freqs],
                    values = A_weighting(third_spec, freqs.values),           
                    name = "Third-octave spectrum",
                    unit = "dBA ref 2e-05")


        elif self.is_stationary == False:    
            time = Data1D(
                name = 'time',
                unit = 's')
            third_spec, freqs.values, time.values = calc_third_octave_levels(self.signal.values, self.fs)
            np.squeeze(third_spec) 
            
            self.third_spec_db = DataFreq(
                symbol = "3oct",
                axes = [freqs, time],
                values = third_spec,            
                name = "Third-octave spectrum",
                unit = "dB ref 2e-05")
            
            if unit == 'dBA':
                self.third_spec_dba = DataFreq(
                    symbol = "3oct",
                    axes = [freqs, time],
                    values = A_weighting(third_spec, freqs.values),         
                    name = "Third-octave spectrum",
                    unit = "dBA ref 2e-05")

    
    def compute_level(self, unit):
        """ Overall Sound Pressure Level calculation in the chosen unit 
        
        Parameter:
        ----------
        unit : string
             'dB' or 'dBA' to apply A-weighting
        plot : boolean
            if True, the overall level is plotted along time (non-steady signals)
        """
 
        if unit == 'dB':
            # Third octave spectrum calculation
            if self.third_spec_db == None:
                self.comp_3oct_spec()
            
            L = 10 * np.log10(sum(np.power(10,self.third_spec_db.values/10)))

            if self.is_stationary == True:
                self.level_db = Data1D(
                    values = [L],
                    name = "Overall Sound Pressure Level",
                    unit = "dB"
                    )
                
            else :               
                time = Data1D(
                    symbol = "T",
                    name = "Time axis",
                    unit = "s",
                    values = np.linspace(0, len(self.signal.values)/self.fs, self.third_spec_db.values.shape[1]))
                
                self.level_db = DataTime(
                    symbol = "dB",
                    axes = [time],
                    values = L,
                    name = "Overall Sound Pressure Level",
                    unit = "dB"
                    )
       
        elif unit == 'dBA':
            # Third octave spectrum calculation
            if self.third_spec_dba == None:
                self.comp_3oct_spec(unit='dBA')
                
        
                L = 10 * np.log10(sum(np.power(10,self.third_spec_dba.values/10)))
        
            if self.is_stationary == True :
                self.level_dba = Data1D(
                        values = [L],
                        name = "Overall Sound Pressure Level",
                        unit = "dBA"
                        )      
            else:
                time = Data1D(
                    symbol = "T",
                    name = "Time axis",
                    unit = "s",
                    values = np.linspace(0, len(self.signal.values)/self.fs, self.third_spec_dba.values.shape[1]))

                self.level_dba = DataTime(
                    symbol = "dBA",
                    axes = [time],
                    values = L,
                    name = "Overall Sound Pressure Level",
                    unit = "dBA"
                    )

    
    def compute_loudness(self, field_type = 'free'):
        """ Method to compute the loudness according to Zwicker's method
        
        Parameter
        ----------
        field-type: string
            'free' by default or 'diffuse'      
               
        """
        if self.third_spec_db == None:
            self.comp_3oct_spec()
    
        if self.is_stationary == True:
            N, N_specific = loudness_zwicker_stationary(self.third_spec_db.values, self.third_spec_db.axes[0].values, field_type)
        elif self.is_stationary == False: 
            N, N_specific = loudness_zwicker_time(self.third_spec_db.values, field_type)
           
        barks = Data1D(
            name = 'Frequency Bark scale',
            unit = 'Bark', 
            values = np.linspace(0.1, 24, int(24 / 0.1)))
        
        if self.is_stationary == True:
            self.loudness_zwicker = Data1D(
                values = [N],
                name = "Loudness",
                unit = "Sones"
                )
            self.loudness_zwicker_specific = DataFreq(
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
            
            self.loudness_zwicker = DataTime(
                symbol = "N",
                axes = [time],
                values = N,
                name = "Loudness",
                unit = "Sones"
                )
            self.loudness_zwicker_specific = DataFreq(
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
       
        if self.loudness_zwicker == None:
            self.compute_loudness()
        
    
        if method == 'din' or method == 'all':
            S = comp_sharpness_din(self.loudness_zwicker.values, self.loudness_zwicker_specific.values, self.is_stationary )      
            
            if self.is_stationary == True:
                self.sharpness_din = Data1D(
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
                
                self.sharpness_din = DataTime(
                    symbol = "S",
                    axes = [time],
                    values = S,
                    name = "Sharpness",
                    unit = "Acum"
                    )
        
        
        elif method == 'aures' or method == 'all':
            S = comp_sharpness_aures(self.loudness_zwicker.values, self.loudness_zwicker_specific.values, self.is_stationary ) 

            if self.is_stationary == True:
                self.sharpness_aures = Data1D(
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
                
                self.sharpness_aures = DataTime(
                    symbol = "S",
                    axes = [time],
                    values = S,
                    name = "Sharpness",
                    unit = "Acum"
                    )

        elif method == 'bismarck' or method == 'all':
            S = comp_sharpness_bismarck(self.loudness_zwicker.values, self.loudness_zwicker_specific.values, self.is_stationary )                    

            if self.is_stationary == True:
                self.sharpness_bismarck = Data1D(
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
                
                self.sharpness_bismarck = DataTime(
                    symbol = "S",
                    axes = [time],
                    values = S,
                    name = "Sharpness",
                    unit = "Acum"
                    )

        elif method == 'fastl' or method == 'all':
            S = comp_sharpness_fastl(self.loudness_zwicker.values, self.loudness_zwicker_specific.values, self.is_stationary ) 
                   
            if self.is_stationary == True:
                self.sharpness_fastl = Data1D(
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
                
                self.sharpness_fastl = DataTime(
                    symbol = "S",
                    axes = [time],
                    values = S,
                    name = "Sharpness",
                    unit = "Acum"
                    )
      
                
    def compute_roughness(self, method='danielweber' overlap=0):
        """ Method to compute roughness according to the Daniel and Weber implementation
        
        Parameter
        ---------
        method : string
            method used to do the computation 'danielweber' is the only one for now
        overlap : float
            overlapping coefficient for the time windows of 200ms 
        """
        roughness = comp_roughness(self.signal.values, self.fs, overlap)
        
        time = Data1D(
            name = 'Time',
            unit = 's',
            values = roughness['time'])

        self.roughness_dw = DataTime(
            symbol = "R",
            axes = [time],
            values = roughness['values'],
            name = "Roughness",
            unit = "Asper"
            )

    def compute_tonality(self, method, prominence=True, plot=True):
        """ Method to compute tonality metrics according to the given method
        
        Parameter
        ---------
        method : string
            'tnr' for the tone-to-noise ratio, 
            'pr' for the prominence ratio, 
            'all' for both       
        prominence : boolean
            give only the prominent tones
        plot : boolean
            if True the results are plotted
        """

        if method == 'tnr' or method == 'all':
            T = comp_tnr(self.is_stationary, self.signal.values, self.fs,prominence=prominence, plot=plot)
            
            freqs = Data1D(
                    symbol = "F",
                    name = "Tones frequencies",
                    unit = "Hz",
                    values = T['freqs'])
            

            
            if self.is_stationary == True:
       
                self.tonality_tnr = DataFreq(
                symbol = 'TNR',
                axes = [freqs],
                values = T['values'],
                name = "Tone-to-noise ratio",
                unit = "dB"
                )
                
                self.tonality_ttnr = Data1D(
                    symbol = "T-TNR",
                    name = "Total TNR value",
                    unit = "dB",
                    values = [T['global value']]
                    )

                
            elif self.is_stationary == False:
            
                time = Data1D(
                    symbol = "T",
                    name = "Time axis",
                    unit = "s",
                    values = T['time']
                    )    
                                
                self.tonality_tnr = DataFreq(
                    symbol = "TNR",
                    axes = [freqs, time] ,
                    values = T['values'],
                    name = "Tone-to-noise ratio",
                    unit = "dB"
                    )
                
                self.tonality_ttnr = Data1D(
                    symbol = "T-TNR",
                    name = "Total TNR value",
                    unit = "dB",
                    values = T['global value']
                    )

            
        if method == 'pr' or method == 'all':
            T = comp_pr(self.is_stationary, self.signal.values, self.fs, prominence=prominence, plot=plot)
            
            freqs = Data1D(
                    symbol = "F",
                    name = "Tones frequencies",
                    unit = "Hz",
                    values = T['freqs'])



            if self.is_stationary == True:
                
                self.tonality_pr = DataFreq(
                symbol = 'PR',
                axes = [freqs],
                values = T['values'],
                name = "Prominence ratio",
                unit = "dB"
                )
                
                self.tonality_tpr = Data1D(
                    symbol = "T-TNR",
                    name = "Total TNR value",
                    unit = "dB",
                    values = [T['global value']]
                    )

                
            elif self.is_stationary == False:
                time = Data1D(
                    symbol = "T",
                    name = "Time axis",
                    unit = "s",
                    values = T['time']
                    )
                
                self.tonality_pr = DataFreq(
                    symbol = "PR",
                    axes = [freqs, time],
                    values = T['values'],
                    name = "Prominence ratio",
                    unit = "dB"
                    )
                
                self.tonality_tpr = Data1D(
                    symbol = "T-TNR",
                    name = "Total TNR value",
                    unit = "dB",
                    values = T['global value']
                    )
