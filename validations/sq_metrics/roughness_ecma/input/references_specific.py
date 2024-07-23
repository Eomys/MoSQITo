import pandas as pd

def ref_artemis(file, fc, fmod):
    """Give the reference values for specific roughness by linear interpolation
    of the data computed with Artemis.

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
