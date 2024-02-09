import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from mosqito.sq_metrics.roughness.roughness_ecma.roughness_ecma import roughness_ecma



def ref_artemis(file, fc, fmod):
    """Give the reference value for roughness by linear interpolation from the data
    obtained with Artemis

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer
        modulation frequency

    Output
    ------
    reference roughness value from Artemis
    """

    if fc == 125:
        if fmod == 20:
            sheet = "Sheet1"
        elif fmod == 30:
            sheet = "Sheet2"
        elif fmod == 40:
            sheet = "Sheet3"
        elif fmod == 50:
            sheet = "Sheet4"
        elif fmod == 60:
            sheet = "Sheet5"
        elif fmod == 70:
            sheet = "Sheet6"
        elif fmod == 80:
            sheet = "Sheet7"
        elif fmod == 90:
            sheet = "Sheet8"
        elif fmod == 100:
            sheet = "Sheet9"
        elif fmod == 120:
            sheet = "Sheet10"
        elif fmod == 140:
            sheet = "Sheet11"
        elif fmod == 160:
            sheet = "Sheet12"
        elif fmod == 200:
            sheet = "Sheet13"
        elif fmod == 300:
            sheet = "Sheet14"
        elif fmod == 400:
            sheet = "Sheet15"
    elif fc == 250:
        if fmod == 20:
            sheet = "Sheet16"
        elif fmod == 30:
            sheet = "Sheet17"
        elif fmod == 40:
            sheet = "Sheet18"
        elif fmod == 50:
            sheet = "Sheet19"
        elif fmod == 60:
            sheet = "Sheet20"
        elif fmod == 70:
            sheet = "Sheet21"
        elif fmod == 80:
            sheet = "Sheet22"
        elif fmod == 90:
            sheet = "Sheet23"
        elif fmod == 100:
            sheet = "Sheet24"
        elif fmod == 120:
            sheet = "Sheet25"
        elif fmod == 140:
            sheet = "Sheet26"
        elif fmod == 160:
            sheet = "Sheet27"
        elif fmod == 200:
            sheet = "Sheet28"
        elif fmod == 300:
            sheet = "Sheet29"
        elif fmod == 400:
            sheet = "Sheet30"
    elif fc == 500:
        if fmod == 20:
            sheet = "Sheet31"
        elif fmod == 30:
            sheet = "Sheet32"
        elif fmod == 40:
            sheet = "Sheet33"
        elif fmod == 50:
            sheet = "Sheet34"
        elif fmod == 60:
            sheet = "Sheet35"
        elif fmod == 70:
            sheet = "Sheet36"
        elif fmod == 80:
            sheet = "Sheet37"
        elif fmod == 90:
            sheet = "Sheet38"
        elif fmod == 100:
            sheet = "Sheet39"
        elif fmod == 120:
            sheet = "Sheet40"
        elif fmod == 140:
            sheet = "Sheet41"
        elif fmod == 160:
            sheet = "Sheet42"
        elif fmod == 200:
            sheet = "Sheet43"
        elif fmod == 300:
            sheet = "Sheet44"
        elif fmod == 400:
            sheet = "Sheet45"
    elif fc == 1000:
        if fmod == 20:
            sheet = "Sheet46"
        elif fmod == 30:
            sheet = "Sheet47"
        elif fmod == 40:
            sheet = "Sheet48"
        elif fmod == 50:
            sheet = "Sheet49"
        elif fmod == 60:
            sheet = "Sheet50"
        elif fmod == 70:
            sheet = "Sheet51"
        elif fmod == 80:
            sheet = "Sheet52"
        elif fmod == 90:
            sheet = "Sheet53"
        elif fmod == 100:
            sheet = "Sheet54"
        elif fmod == 120:
            sheet = "Sheet55"
        elif fmod == 140:
            sheet = "Sheet56"
        elif fmod == 160:
            sheet = "Sheet57"
        elif fmod == 200:
            sheet = "Sheet58"
        elif fmod == 300:
            sheet = "Sheet59"
        elif fmod == 400:
            sheet = "Sheet60"
    elif fc == 2000:
        if fmod == 20:
            sheet = "Sheet61"
        elif fmod == 30:
            sheet = "Sheet62"
        elif fmod == 40:
            sheet = "Sheet63"
        elif fmod == 50:
            sheet = "Sheet64"
        elif fmod == 60:
            sheet = "Sheet65"
        elif fmod == 70:
            sheet = "Sheet66"
        elif fmod == 80:
            sheet = "Sheet67"
        elif fmod == 90:
            sheet = "Sheet68"
        elif fmod == 100:
            sheet = "Sheet69"
        elif fmod == 120:
            sheet = "Sheet70"
        elif fmod == 140:
            sheet = "Sheet71"
        elif fmod == 160:
            sheet = "Sheet72"
        elif fmod == 200:
            sheet = "Sheet73"
        elif fmod == 300:
            sheet = "Sheet74"
        elif fmod == 400:
            sheet = "Sheet75"
    elif fc == 4000:
        if fmod == 20:
            sheet = "Sheet76"
        elif fmod == 30:
            sheet = "Sheet77"
        elif fmod == 40:
            sheet = "Sheet78"
        elif fmod == 50:
            sheet = "Sheet79"
        elif fmod == 60:
            sheet = "Sheet80"
        elif fmod == 70:
            sheet = "Sheet81"
        elif fmod == 80:
            sheet = "Sheet82"
        elif fmod == 90:
            sheet = "Sheet83"
        elif fmod == 100:
            sheet = "Sheet84"
        elif fmod == 120:
            sheet = "Sheet85"
        elif fmod == 140:
            sheet = "Sheet86"
        elif fmod == 160:
            sheet = "Sheet87"
        elif fmod == 200:
            sheet = "Sheet88"
        elif fmod == 300:
            sheet = "Sheet89"
        elif fmod == 400:
            sheet = "Sheet90"
    elif fc == 8000:
        if fmod == 20:
            sheet = "Sheet91"
        elif fmod == 30:
            sheet = "Sheet92"
        elif fmod == 40:
            sheet = "Sheet93"
        elif fmod == 50:
            sheet = "Sheet94"
        elif fmod == 60:
            sheet = "Sheet95"
        elif fmod == 70:
            sheet = "Sheet96"
        elif fmod == 80:
            sheet = "Sheet97"
        elif fmod == 90:
            sheet = "Sheet98"
        elif fmod == 100:
            sheet = "Sheet99"
        elif fmod == 120:
            sheet = "Sheet100"
        elif fmod == 140:
            sheet = "Sheet101"
        elif fmod == 160:
            sheet = "Sheet102"
        elif fmod == 200:
            sheet = "Sheet103"
        elif fmod == 300:
            sheet = "Sheet104"
        elif fmod == 400:
            sheet = "Sheet105"
    a = pd.read_excel(io=file, sheet_name=sheet, skiprows=13, usecols="A, B", names=["freq", "R_spec"]).to_numpy()
    R = pd.read_excel(io=file, sheet_name=sheet, skiprows=8, usecols="B", names=["R"]).to_numpy()[0][0]
    return a, R

def signal_test(fs, d, fc, fmod, dB, mdepth=1):
    dt = 1 / fs
    time = np.arange(0, d, dt)

    signal = (
        0.5
        * (1 + mdepth * (np.sin(2 * np.pi * fmod * time)))
        * np.sin(2 * np.pi * fc * time)
    )    
    
    rms = np.sqrt(np.mean(np.power(signal, 2)))
    ampl = 0.00002 * np.power(10, dB / 20) / rms
    signal = signal * ampl
    return signal

def _auditory_filters_centre_freq():
    """
    Auditory filter bank center frequencies generation

    This function generates the Auditory filter bank center frequencies according
    to ECMA-418-2 section 5.1.4.1 equation 9

    Parameters
    ----------

    Returns
    -------
    centre_freq: ndarray
        Vector of auditory filter bank center frequencies

    """

    z = np.arange(0.5,27,0.5)
    df_0 = 81.9289  # ECMA-418-2
    c = 0.1618  # ECMA-418-2

    # Central frequency
    center_freq = (df_0 / c) * np.sinh(c * z)

    return center_freq



if __name__ == "__main__":
    file = r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\sq_metrics\roughness_ecma\validation_specific_roughness_ecma.xlsx"
    import matplotlib.colors as mcolors
    fc = [125,250,500,1000,2000,4000,8000]
    fmod = [20,30,40,50,60,70,80,90,100,120,140,160,200,300,400]
    fs = 48000
    d = 1
    dB = 60
    mdepth = 1
    # fc = [1000]
    # fmod = [70]
    Ro = np.empty((len(fc), len(fmod)))
    Rref = np.empty((len(fc), len(fmod)))
    for i in range(len((fc))):
        for j in range(len((fmod))):
            carrier = fc[i]
            mod = fmod[j]
            ref_spec, ref_R = ref_artemis(file, carrier, mod)
            stimulus = signal_test(fs, d, carrier, mod, dB, mdepth)
            R_spec, _, R = roughness_ecma(stimulus, fs)
            Ro[i,j] = R
            Rref[i,j] = float(ref_R[:-6])
            
            # plt.figure()
            # plt.step(ref_spec[:,0], ref_spec[:,1], label="Artemis", color="k")
            # plt.step(_auditory_filters_centre_freq(), R_spec, label="Mosqito", color="#69c3c5")
            # plt.title("Artemis="+ref_R+"\n MOSQITO="+f"{R:.3f}"+" asper")
            # plt.legend()
            # plt.xlim(-5,9000)
            # plt.xlabel("Asper/Bark")
            # plt.ylabel("Frequency [Hz]")
            # # plt.show(block=True)
            # plt.savefig(r"C:\Users\SaloméWanty\Documents\Mosqito_roughness\validations\roughness\output\fc_" + f"{carrier}" +"_fmod_" + f"{mod}"+ ".png" )

    colors = plt.cm.rainbow(np.linspace(0,1,len(Ro)))
    plt.figure()
    for i in range(len((fc))):  
        plt.plot(np.array(fmod), Ro[i,:] + i, label=f"{fc[i]}", marker='o', color=colors[i])
        plt.plot(np.array(fmod), Rref[i,:] + i, marker='s', linestyle='--', color=colors[i])
    plt.legend()
    
    colors = plt.cm.rainbow(np.linspace(0,1,len(fmod)))
    plt.figure()
    for j in range(len((fmod))):  
        plt.plot(fc, Ro[:,j]+3*j, label=f"{fmod[j]}", marker='o', color=colors[j])
        plt.plot(fc, Rref[:,j]+3*j, marker='s', linestyle='--', color=colors[j])
    plt.legend()
    plt.show(block=True)
    
    from matplotlib import cm
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    Y, X = np.meshgrid(fc, fmod)
    ax.plot_surface(X, Y, Ro.T, cmap=cm.coolwarm)
    ax.plot_wireframe(X, Y, Rref.T, color='k')

    ax.set_xlabel('Fc Label')
    ax.set_ylabel('Fmod Label')
    ax.set_zlabel('R Label')
    

    plt.show(block=True)
    
    print('pause')
