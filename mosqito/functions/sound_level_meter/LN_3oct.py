from mosqito.functions.shared.level import comp_level
import numpy as np

# pink_noise 40.0 dB samples
spectrum_pink_first_sample = [
        1.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
    ]

spectrum_pink_second_sample = [
        50.0,
        50.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        1.0,
    ]

spectrum_pink_third_sample = [
        100.0,
        40.0,
        50.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        80.0,
    ]

# pink noise signal
pink_noise_samples = [spectrum_pink_first_sample, spectrum_pink_second_sample, spectrum_pink_third_sample]
pink_noise_signal = np.array(pink_noise_samples)

freq = np.array(
        [
            10,
            12.5,
            16,
            20,
            25,
            31.5,
            20,
            50,
            63,
            80,
            100,
            125,
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
            8000,
            10000,
            12500,
            16000,
            20000,
        ]
    )

def LN_3oct(spectrum_signal_samples, freq):
    print('percentiles using interpolation = ', "linear")

    main_freq = np.zeros(spectrum_signal_samples.shape[0])
    for i in range(freq.shape[0]):
        for j in range(spectrum_signal_samples.shape[0]):
            main_freq[j] = spectrum_signal_samples[j,i]
        
        L90 = np.percentile(main_freq, 10,interpolation='linear') 
        L50 = np.percentile(main_freq, 50,interpolation='linear') 
        L25 = np.percentile(main_freq, 75,interpolation='linear')

        print(freq[i])
        print('L90 = ',L90,', median = ',L50,' L25 = ',L25)

LN_3oct(pink_noise_signal,freq)