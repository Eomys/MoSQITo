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

spectrum_pink_4_sample = [
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
pink_noise_samples = [spectrum_pink_first_sample, spectrum_pink_second_sample, spectrum_pink_third_sample, spectrum_pink_4_sample]
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

def max_level_3oct(spectrum_signal_samples, freq):

    main_freq = np.zeros(spectrum_signal_samples.shape[0])
    max_level_3oct = np.zeros(freq.shape[0])
    for i in range(freq.shape[0]):
        for j in range(spectrum_signal_samples.shape[0]):
            main_freq[j] = spectrum_signal_samples[j,i]
        
        max_level_3oct[i] = max(main_freq) 

        print(freq[i])
        print(max_level_3oct)
    
    return max_level_3oct

max_level_3oct(pink_noise_signal,freq)