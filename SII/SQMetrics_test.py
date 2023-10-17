# External libraries imports
import numpy 
from scipy.signal import resample
from mosqito.sq_metrics import (
  loudness_zwst,
  loudness_zwtv,
  loudness_zwst_freq,
  sharpness_din_st,
  sharpness_din_tv,
  sharpness_din_freq,
  sharpness_din_from_loudness,
  roughness_dw,
  roughness_dw_freq,
  tnr_ecma_st,
  tnr_ecma_tv,
  tnr_ecma_freq,
  pr_ecma_st,
  pr_ecma_tv,
  pr_ecma_freq
  )

class SQMetrics():
  """ Class to compute SQ metrics from Actran's time or frequency domain
  values using MOSQITO package. """

  def __init__(self, x, y, domain='frequency', signal_type=None, spectrum_type='spectrum', calibration_type='factor', calibration_level=1, sound_field_type='free'):
    """ Constructor of the class.

    Parameters:
    -----------
    x : array of float / integer
      Axis corresponding to time / frequency with size [nperseg].
    y : array of float / complex
      Pressure or frequency data with size [nperseg x nseg].
    domain : string 
      Parameter to indicate either y is given in 'time' or 'frequency' domain. Default is 'frequency'.
    signal_type : string
      'stationary' or 'transient'. Default is 'stationary'.
    spectrum_type : string
      'spectrum' or 'psd'. Default is 'spectrum'.
    calibration_type : string 
      'dB' or 'factor'. Default is 'factor'.
    calibration_level : float 
      Calibration value to set the level of y according to the calibration type. Default is 1.
    sound_field_type : string
      'free' or 'diffuse'.

    """
    ##############
    # Attributes #
    ##############

    if len(x) != len(y):
      raise ValueError('x and y must have the same size.')
    self.x = x
    self.y = y

    if (domain != 'time') & (domain != 'frequency'):
      raise ValueError("To specify the input domain, use 'time' or 'frequency'.")
    self.domain = domain

    if domain == 'frequency':
      if numpy.iscomplexobj(numpy.array(y)) == False:
        raise ValueError('Input spectrum must be complex.')

    if domain == 'time':
      dt = numpy.around(numpy.diff(x[1:] - x[:-1]), decimals = 5)
      if dt.any() != 0:
        raise ValueError('The given time axis is not correct, the time step should be constant.')
      self.fs = int(numpy.around(1 / numpy.mean(x[1:] - x[:-1])))
      if self.fs != 48000:
        self.y = resample(y, int(48000 * len(y) / self.fs))
        self.fs = 48000
    
    if signal_type is not None:
      if (signal_type != 'stationary') & (signal_type != 'transient'):
        raise ValueError("To indicate the time data series nature, use 'stationary' or 'transient.")
      if signal_type == 'stationary':
        self.is_stationary = True
      elif signal_type == 'transient':
        self.is_stationary = False

    if spectrum_type is not None:
      if (spectrum_type != 'spectrum') & (spectrum_type != 'psd'):
        raise ValueError("To indicate the frequency data series nature, use 'spectrum' or 'psd'.")
      if spectrum_type == 'spectrum':
        self.is_psd = False
      elif spectrum_type == 'psd':
        self.is_psd = True

    if (calibration_type!='dB') & (calibration_type !='factor'):
      raise ValueError('To specify calibration type, use "factor" or "dB".') 

    # Calibration factor for the data to be in Pa
    if calibration_type=='factor':
      if calibration_level==0:
        raise ValueError('Calibration factor is set to 0, signal will be cancelled.')   
      else:   
        self.y *= calibration_level
    elif calibration_type == 'dB':
      max_amplitude = numpy.max(numpy.abs(self.y))
      ref_pressure = 2e-5
      self.y *= ref_pressure * 10**(calibration_level / 20) / max_amplitude

    if (sound_field_type != 'free') & (sound_field_type != 'diffuse'):
      raise ValueError('Sound field type must be "free" or "diffuse".')        
    self.sound_field_type = sound_field_type

    ###########
    # Methods #
    ###########

    # All the methods are built on the same scheme: the user just has to call the metric name,
    # and the methods automatically use the right MOSQITO function according to the data type.
    # The output is always a dictionary including the metric name, the values and the axis.

  ### Loudness ISO 532 B ###
  def loudness_iso(self):
    if self.domain == 'time':
      if self.is_stationary:
        N, N_spec, bark_axis = loudness_zwst(self.y, self.fs, self.sound_field_type)
        time = None
      else:
        N, N_spec, bark_axis, time = loudness_zwtv(self.y, self.fs, self.sound_field_type)
    else:
      RMS_spec = rms_spectrum(self.y)
      N, N_spec, bark_axis = loudness_zwst_freq(RMS_spec, self.x, self.sound_field_type)
      time = None
    output = {
      "name": "Loudness ISO532B",
      "global value": N,
      "specific values": N_spec,
      "frequency": bark_axis,
      "frequency unit": 'Bark',
      "time": time,
      }
    return output

  ### Sharpness DIN 45692 ###
  def sharpness_din(self, global_loudness=None, specific_loudness=None):
    # To skip double loudness computation if already done
    if (global_loudness is not None) & (specific_loudness is not None):
      S = sharpness_din_from_loudness(global_loudness, specific_loudness, weighting = "din", skip = 0.1)
      time = None
    else:
      if self.domain == 'time':
        if self.is_stationary:
          S = sharpness_din_st(self.y, self.fs, weighting="din", field_type=self.sound_field_type)
          time = None
        else:
          S, time = sharpness_din_tv(self.y, self.fs, weighting="din", field_type=self.sound_field_type, skip=0.1)
      else:
        RMS_spec = rms_spectrum(self.y, self.is_psd)
        S = sharpness_din_freq(RMS_spec, self.x, weighting="din", field_type=self.sound_field_type)
        time = None

    output = {
      "name": "Sharpness DIN45692",
      "global value": S,
      "time": time,
      }

    return output

  ### Roughness by Daniel and Weber ###
  def roughness_dw(self, overlap=0):

    if self.domain == 'time':
      R, R_spec, bark_axis, time = roughness_dw(numpy.sqrt(self.y) if self.is_psd else self.y, self.fs, overlap)
      if self.is_stationary == True:
        output = {
          "name": "Roughness",
          "global value": numpy.mean(R),
          "specific values": numpy.mean(R_spec, axis=1),
          "frequency": bark_axis,
          "frequency unit": 'Bark',
          "time": None,
        }
      else:
        output = {
          "name": "Roughness",
          "global value": R,
          "specific values": R_spec,
          "frequency": bark_axis,
          "frequency unit": 'Bark',
          "time": time,
        }
    else:
      R, R_spec, bark_axis = roughness_dw_freq(self.y, self.x)
      output = {
        "name": "Roughness",
        "global value": R,
        "specific values": R_spec,
        "frequency": bark_axis,
        "frequency unit": 'Bark',
        "time": None,
      }
    return output

  ### Tone-to-noise Ratio ECMA 74 ###
  def tnr_ecma(self, prominence=False, overlap=0):

    if (overlap < 0) or (overlap > 1):
      fft.Message.Message('FATAL', "Overlap must be between 0 and 1.", 1)
      return None

    if self.domain == 'time':
      if self.is_stationary == True:
        t_tnr, tnr, prominence, frequency = tnr_ecma_st(self.y, self.fs, prominence)
        time = None
      else:
        t_tnr, tnr, prominence, frequency, time = tnr_ecma_tv(self.y, self.fs, prominence, overlap)
    else:
      t_tnr, tnr, prominence, frequency = tnr_ecma_freq(numpy.sqrt(self.y) if self.is_psd else self.y, self.x, prominence)
      time = None

    output = {
      "name": "Tone-to-noise Ratio ECMA74",
      "global value": t_tnr,
      "specific values": tnr,
      "prominence criterion": prominence,
      "frequency": frequency,
      "frequency unit": 'Hertz',
      "time": time,
      }
    return output

  ### Prominence Ratio ECMA 74 ###
  def pr_ecma(self, prominence=False, overlap=0):


    if self.domain == 'time':
      if self.is_stationary == True:
        t_pr, pr, prominence, frequency = pr_ecma_st(self.y, self.fs, prominence)
        time = None
      else:
        t_pr, pr, prominence, frequency, time = pr_ecma_tv(self.y, self.fs, prominence, overlap)
    else:
      t_pr, pr, prominence, frequency = pr_ecma_freq(numpy.sqrt(self.y) if self.is_psd else self.y, self.x, prominence)
      time = None

    output = {
      "name": "Prominence Ratio ECMA74",
      "global value": t_pr,
      "specific values": pr,
      "prominence criterion": prominence,
      "frequency": frequency,
      "frequency unit": 'Hertz',
      "time": time,
    }
    return output

  ### Speech Intelligibility Index ANSI S3.5 ###
  def sii_ansi(self, method, noise, speech, speech_distance='default', speech_level='default', threshold=None):
    '''
    Method to compute the Speech Intelligibility Index.

    Parameters:
      method: string
        Frequency bands choice, either 'critical_bands', 'equal_critical_bands', 'third_octave_bands' or 'octave_bands'.
      noise: SQMetrics object / int / float
        SQMetric object to be used as background noise data or overall dB level.
      speech: SQMetrics object / string
        SQMetric object to be used as speech data or 'normal', 'raised', 'loud', 'shouted'.
      speech_distance:
        Distance from the talker\'s lips to the center of the listener\'s head in meters. 
        'default' is 1m.
      speech_level:
        If the speech was measured, the standard speech spectra can be adjusted to the measured overall level. 
        'default' is the standard level corresponding to the input method.
      threshold: string
        Either 'standard' to use ANSI standard threshold, or None (0 on all bands).
        Default is None.
    '''

    # sanity checks


    # load the calculation parameters corresponding to the chosen method
    if method == 'critical_bands':
      from SII_critical_band_procedure import (
        CENTER_FREQUENCIES,
        LOWER_FREQUENCIES,
        UPPER_FREQUENCIES,
        IMPORTANCE,
        REFERENCE_INTERNAL_NOISE_SPECTRUM,
        STANDARD_SPEECH_SPECTRUM_NORMAL,)
    elif method == 'equal_critical_bands':
      from SII_equal_critical_band_procedure import (
        CENTER_FREQUENCIES,
        LOWER_FREQUENCIES,
        UPPER_FREQUENCIES,
        IMPORTANCE, 
        REFERENCE_INTERNAL_NOISE_SPECTRUM,
        STANDARD_SPEECH_SPECTRUM_NORMAL,)    
    elif method == 'third_octave_bands':
      from SII_third_octave_band_procedure import (
        CENTER_FREQUENCIES,
        LOWER_FREQUENCIES,
        UPPER_FREQUENCIES,
        BANDWIDTH_ADJUSTEMENT,
        IMPORTANCE, 
        REFERENCE_INTERNAL_NOISE_SPECTRUM,
        STANDARD_SPEECH_SPECTRUM_NORMAL,)
    elif method == 'octave_bands':
      from SII_octave_band_procedure import (   
        CENTER_FREQUENCIES,
        LOWER_FREQUENCIES,
        UPPER_FREQUENCIES,
        BANDWIDTH_ADJUSTEMENT,
        IMPORTANCE, 
        REFERENCE_INTERNAL_NOISE_SPECTRUM,
        STANDARD_SPEECH_SPECTRUM_NORMAL,)
    nbands = len(CENTER_FREQUENCIES)

    # if noise is an overall dB level
    if (type(noise) == float) or (type(noise) == int):
      nbands = len(CENTER_FREQUENCIES)
      noise_data = numpy.empty((nbands))
      noise_data.fill(10*numpy.log10(10**(noise/10)/nbands))
      noise_axis = CENTER_FREQUENCIES

    # elif the noise is a SQMetrics object
    elif isinstance(noise, SQMetrics):
      if noise.domain == 'frequency':
        if noise.is_psd:
          noise_data = dB(numpy.sqrt(noise.y))
        elif noise.is_psd is False:
          noise_data = dB(noise.y)
        noise_axis = noise.x
      elif noise.domain == 'time':
        n = len(noise.x)
        # compute spectrum
        noise_data = dB(numpy.fft.fft(noise.y)[0:n//2])
        noise_axis = numpy.fft.fftfreq(n, 1/noise.fs)[0:n//2]

    # convert the data to match the frequency bands
    if numpy.array(noise_axis != CENTER_FREQUENCIES).any():
      N = compute_band_spectrum(noise_axis, noise_data, LOWER_FREQUENCIES, UPPER_FREQUENCIES)
    else:
      N = noise_data
    
    # if speech is an import from the standard
    if type(speech) == str:
      if method == 'critical_bands':
        if speech == 'normal':
          from SII_critical_band_procedure import STANDARD_SPEECH_SPECTRUM_NORMAL, OVERALL_SPEECH_LEVEL_NORMAL
          E = STANDARD_SPEECH_SPECTRUM_NORMAL
          reference_level = OVERALL_SPEECH_LEVEL_NORMAL
        elif speech == 'raised':
          from SII_critical_band_procedure import STANDARD_SPEECH_SPECTRUM_RAISED, OVERALL_SPEECH_LEVEL_RAISED
          E = STANDARD_SPEECH_SPECTRUM_RAISED
          reference_level = OVERALL_SPEECH_LEVEL_RAISED
        elif speech == 'loud':
          from SII_critical_band_procedure import STANDARD_SPEECH_SPECTRUM_LOUD, OVERALL_SPEECH_LEVEL_LOUD
          E = STANDARD_SPEECH_SPECTRUM_LOUD
          reference_level = OVERALL_SPEECH_LEVEL_LOUD
        elif speech == 'shouted':
          from SII_critical_band_procedure import STANDARD_SPEECH_SPECTRUM_SHOUT, OVERALL_SPEECH_LEVEL_SHOUT
          E = STANDARD_SPEECH_SPECTRUM_SHOUT
          reference_level = OVERALL_SPEECH_LEVEL_SHOUT
      elif method == 'equal_critical_bands':
        if speech == 'normal':
          from SII_equal_critical_band_procedure import STANDARD_SPEECH_SPECTRUM_NORMAL, OVERALL_SPEECH_LEVEL_NORMAL
          E = STANDARD_SPEECH_SPECTRUM_NORMAL
          reference_level = OVERALL_SPEECH_LEVEL_NORMAL
        elif speech == 'raised':
          from SII_equal_critical_band_procedure import STANDARD_SPEECH_SPECTRUM_RAISED, OVERALL_SPEECH_LEVEL_RAISED
          E = STANDARD_SPEECH_SPECTRUM_RAISED
          reference_level = OVERALL_SPEECH_LEVEL_RAISED
        elif speech == 'loud':
          from SII_equal_critical_band_procedure import STANDARD_SPEECH_SPECTRUM_LOUD, OVERALL_SPEECH_LEVEL_LOUD
          E = STANDARD_SPEECH_SPECTRUM_LOUD
          reference_level = OVERALL_SPEECH_LEVEL_LOUD
        elif speech == 'shouted':
          from SII_equal_critical_band_procedure import STANDARD_SPEECH_SPECTRUM_SHOUT, OVERALL_SPEECH_LEVEL_SHOUT
          E = STANDARD_SPEECH_SPECTRUM_SHOUT
          reference_level = OVERALL_SPEECH_LEVEL_SHOUT
      elif method == 'third_octave_bands':
        if speech == 'normal':
          from SII_third_octave_band_procedure import STANDARD_SPEECH_SPECTRUM_NORMAL, OVERALL_SPEECH_LEVEL_NORMAL
          E = STANDARD_SPEECH_SPECTRUM_NORMAL
          reference_level = OVERALL_SPEECH_LEVEL_NORMAL
        elif speech == 'raised':
          from SII_third_octave_band_procedure import STANDARD_SPEECH_SPECTRUM_RAISED, OVERALL_SPEECH_LEVEL_RAISED
          E = STANDARD_SPEECH_SPECTRUM_RAISED
          reference_level = OVERALL_SPEECH_LEVEL_RAISED
        elif speech == 'loud':
          from SII_third_octave_band_procedure import STANDARD_SPEECH_SPECTRUM_LOUD, OVERALL_SPEECH_LEVEL_LOUD
          E = STANDARD_SPEECH_SPECTRUM_LOUD
          reference_level = OVERALL_SPEECH_LEVEL_LOUD
        elif speech == 'shouted':
          from SII_third_octave_band_procedure import STANDARD_SPEECH_SPECTRUM_SHOUT, OVERALL_SPEECH_LEVEL_SHOUT
          E = STANDARD_SPEECH_SPECTRUM_SHOUT
          reference_level = OVERALL_SPEECH_LEVEL_SHOUT
      elif method == 'octave_bands':
        if speech == 'normal':
          from SII_octave_band_procedure import STANDARD_SPEECH_SPECTRUM_NORMAL, OVERALL_SPEECH_LEVEL_NORMAL
          E = STANDARD_SPEECH_SPECTRUM_NORMAL
          reference_level = OVERALL_SPEECH_LEVEL_NORMAL
        elif speech == 'raised':
          from SII_octave_band_procedure import STANDARD_SPEECH_SPECTRUM_RAISED, OVERALL_SPEECH_LEVEL_RAISED
          E = STANDARD_SPEECH_SPECTRUM_RAISED
          reference_level = OVERALL_SPEECH_LEVEL_RAISED
        elif speech == 'loud':
          from SII_octave_band_procedure import STANDARD_SPEECH_SPECTRUM_LOUD, OVERALL_SPEECH_LEVEL_LOUD
          E = STANDARD_SPEECH_SPECTRUM_LOUD
          reference_level = OVERALL_SPEECH_LEVEL_LOUD
        elif speech == 'shouted':
          from SII_octave_band_procedure import STANDARD_SPEECH_SPECTRUM_SHOUT, OVERALL_SPEECH_LEVEL_SHOUT
          E = STANDARD_SPEECH_SPECTRUM_SHOUT
          reference_level = OVERALL_SPEECH_LEVEL_SHOUT
      
      if speech_distance != 'default':
        # correct the level according to the distance between talker's lips and listener's head center
        E -= 20 * numpy.log10(speech_distance)
      if speech_level != 'default':
        # set dB level by comparison with standard data
        E += (speech_level - reference_level)

    # elif speech is a SQMetrics object
    elif isinstance(speech, SQMetrics):
      # set dB spectrum
      if speech.domain == 'frequency':
        if speech.is_psd:
          speech_data = dB(numpy.sqrt(speech.y))
        elif speech.is_psd is False:
          speech_data = dB(speech.y)
        speech_axis = speech.x
      elif speech.domain == 'time':
        n = len(speech.x)
        # compute spectrum
        speech_data = dB(numpy.fft.fft(speech.y)[0:n//2])
        speech_axis = numpy.fft.fftfreq(n, 1/speech.fs)[0:n//2]

      # convert the data to match the frequency bands
      if numpy.array(speech_axis != CENTER_FREQUENCIES).any():
        E = compute_band_spectrum(speech_axis, speech_data, LOWER_FREQUENCIES, UPPER_FREQUENCIES)
      else:
        E = speech_data

      # dB bandwidth adjustement
      if (method == 'critical_bands') or (method == 'equal_critical_bands'):
        E -= 10 * numpy.log10(UPPER_FREQUENCIES - LOWER_FREQUENCIES)
      elif (method == 'octave_bands') or (method == 'third_octave_bands'):
        E -= BANDWIDTH_ADJUSTEMENT

    if threshold == None:
      T = numpy.zeros((nbands))
    elif threshold == 'standard':
      from mosqito.utils.LTQ import LTQ
      from mosqito.utils.conversion import freq2bark
      T = LTQ(freq2bark(CENTER_FREQUENCIES))

    # Computation
    if method == 'octave_bands':
      Z = N   
    else:
      V = numpy.array(E) - 24
      B = numpy.maximum(N, V)
        
      if method == 'third_octave_bands':
        C = -80 + 0.6 * (B + 10*numpy.log10(CENTER_FREQUENCIES)-6.353)
        Z = numpy.zeros((nbands))
        for i in range(nbands): 
          s = 0
          for k in range(i):
            s += 10**(0.1*(B[k] + 3.32 * C[k] * numpy.log10(0.89 * CENTER_FREQUENCIES[i] / CENTER_FREQUENCIES[k])))
              
          Z[i] = 10 * numpy.log10(10**(0.1*N[i]) + s)
      else:
        C = -80 + 0.6 * (B + 10*numpy.log10(UPPER_FREQUENCIES - LOWER_FREQUENCIES))
        Z = numpy.zeros((nbands))
        for i in range(nbands): 
          s = 0
          for k in range(i-1):
            s += 10**(0.1*(B[k] + 3.32 * C[k] * numpy.log10(CENTER_FREQUENCIES[i] / UPPER_FREQUENCIES[k])))
                
            Z[i] = 10 * numpy.log10(10**(0.1*N[i]) + s)
      # 4.3.2.4
      Z[0] = B[0]
        
    # STEP 4
    X = REFERENCE_INTERNAL_NOISE_SPECTRUM + T

    # STEP 5
    D = numpy.maximum(Z, X)
    
    # STEP 6
    L = 1 - (E - STANDARD_SPEECH_SPECTRUM_NORMAL -10)/160
    L[numpy.where(L>1)] = 1
    
    # STEP 7
    K = (E - D + 15)/30
    K[numpy.where(K>1)] = 1
    K[numpy.where(K<0)] = 0
    A = L * K
    
    # STEP 8
    spec_sii = IMPORTANCE * A
    sii = numpy.sum(spec_sii)
    
    output = {
      "name": "Speech Intelligibility Index ANSI S3.5",
      "global value": sii,
      "specific values": spec_sii,
      "frequency": CENTER_FREQUENCIES,
      "frequency unit": 'Hertz',
      "time": None,
    }
    
    return output


  #############
  # Functions #
  #############

def rms_spectrum(y, is_psd=False):
  return numpy.abs(numpy.sqrt(y) / numpy.sqrt(2) / len(y)) if is_psd else numpy.abs(y / numpy.sqrt(2) / len(y))

def dB(y):
  return 20 * numpy.log10(numpy.abs(y) / len(y))

def compute_band_spectrum(x, y, lower_frequencies, upper_frequencies):
  nbands = len(lower_frequencies)
  band_spectrum = numpy.zeros((nbands))
  # convert spectrum on the selected frequency bands
  for i in range(nbands):
    # index of the frequencies within the band
    idx = numpy.where((x >= lower_frequencies[i]) & (x < upper_frequencies[i]))[0]
    band_spectrum[i] = 10 * numpy.log10(numpy.sum(10**(y[idx]/10)))
  return band_spectrum

y_speech = numpy.array([32.41,
        34.48,
        34.75,
        33.98,
        34.59,
        34.27,
        32.06,
        28.30,
        25.01,
        23.00,
        20.15,
        17.32,
        13.18,
        11.55,
        9.33,
        5.31,
        2.59,
        1.13])

y_speech = numpy.array([54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54,
        54])


x = numpy.array(
        [
        160,
        200,
        250,
        315,
        400,
        500,
        630,
        800,
        1000,
        1250,
        1600,
        2000,
        2500,
        3150,
        4000,
        5000,
        6300,
        8000
        ]
        )


y_noise = numpy.array([
        0.00,
        0.00,
        10.00,
        20.00,
        30.00,
        33.00,
        40.00,
        36.00,
        22.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00,
        00.00   
            ])

y_noise = numpy.array([
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
        -60,
            ])

import matplotlib.pyplot as plt

speech = SQMetrics(x, numpy.array(10**(y_speech/20)*2e-5,dtype=complex),domain='frequency',spectrum_type='spectrum')
noise = SQMetrics(x,numpy.array(10**(y_noise/20)*2e-5,dtype=complex),domain='frequency',spectrum_type='spectrum')

sii_from_speech = speech.sii_ansi('third_octave_bands', noise=noise, speech=speech, threshold=None)
sii_from_noise = noise.sii_ansi('third_octave_bands', noise=noise, speech='normal')

width = numpy.concatenate((numpy.diff(sii_from_noise['frequency']),[2000]))*0.4

ref = numpy.array([0.0083,
0.0095,
0.015,
0.0289,
0.044,
0.0578,
0.0653,
0.0711,
0.0818,
0.0844,
0.0882,
0.0898,
0.0868,
0.0844,
0.0771,
0.0527,
0.0364,
0.014325167])


plt.bar(sii_from_noise['frequency'], sii_from_noise['specific values'],width=width, color='#0097BA', label='Standard ANSI S3.5')
plt.bar(sii_from_noise['frequency']+width, ref,width=width, color='#A5D867', label='SQMetrics')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Specific values')
plt.legend(fontsize=12)
title ='Global SII = %.3f' %(sii_from_noise['global value']) + ', standard = 0.996'
plt.title(title, fontsize=14)
