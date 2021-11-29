"""
    Autor: Cristina Taboada (TinaTabo)
    Fecha inicio: 27/11/2021
    Fecha última modificación: 27/11/2021
    Descripción: Funcion para calcular el valor del parámetro de correccion Kt
                 descrita en el Anexo IV punto 3.3. Correcion por componentes tonales (Kt),
                 impulsiva (Ki) y bajas frecuencias (Kf), del RD 1763/2007.
"""

#-- Librerias
import csv

#-- Importar función
from tonality_iso1996K import tone_detector

"""
        Parameters
        ----------
        - prominent_tones: diccionario obtenido con la funcion "tone_detector", donde se localizan
                           los tonos prominentes.
        - file: fichero.csv con los Lp promedio de las banda de tercio de octava.

        Outputs
        -------
        - Kt: parámetro de corrección por componentes tonales Kt.
"""
#------- BORRAR CUANDO SE PASE A FUNCION-------

#-- Archivo.csv con los datos correspondientes a las bandas de tercio de octava
file = 'data.csv'

#-- Diccionario con los tonos prominentes
prominent_tones = tone_detector(file)
print("--------DICCIONARIO TONOS---------")
print(prominent_tones)
print("----------------------------------")

#-- Leer el archivo y extraer los datos
with open(file, 'r') as csvfile:
    data = list(csv.reader(csvfile, delimiter=","))

#-- Obtener las listas de las frec.centrales y los Lp_promedio.
fc = data[0][1:32]
Lp_mean = data[1][1:32]

#-- Longitud de las listas, las 2 tienen la misma long.
Lp_len = len(Lp_mean)

#-- Buscar los índices correspondientes a los Key del diccionario para poder operar con las listas.
#-- Lista de índices donde se localizan tonos prominentes en las listas.
index_list = []

for key in prominent_tones:
    idx = fc.index(key)
    index_list.append(idx)

print("--------POSICIONES DE LOS TONOS EN LA LISTA---------")
print(index_list)
print("----------------------------------------------------")


#-- Ya tenemos localizados los indices vamos a proceder con los calculos.
#-- Lista de Kt de cada tono prominente.
Kt_list = []

for x in index_list:
    #-- Obtengo Lf
    Lf = int(Lp_mean[x])

    #-- Calculo Ls
    Lf_prev = int(Lp_mean[x-1])
    Lf_post = int(Lp_mean[x+1])
    Ls = (Lf_post - Lf_prev)/2

    #-- Calculo Lt
    Lt = Lf - Ls

    #-- Obtengo el valor de Kt, segun Lt y el rango de frecuencia donde se encuentre el 
    #-- tono prominente.
    if x > 0 and x < 9:
        #-- "BAJA FRECUENCIA --> diferencia entre 8 y 12 dB"
        if Lt < 8:
            Kt = 0
            print("-----punto 1 -------")
        elif Lt >= 8 and Lt <= 12:
            Kt = 3
            print("-----punto 2 -------")
        elif Lt > 12:
            Kt = 6
            print("-----punto 3 -------")
        
        Kt_list.append(Kt)
    elif x > 8 and x < 14:
        #-- "MEDIA FRECUENCIA --> diferencia entre 5 y 8 dB"
        if Lt < 5:
            Kt = 0
            print("-----punto 4 -------")
        elif Lt >= 5 and Lt <= 8:
            Kt = 3
            print("-----punto 5 -------")
        elif Lt > 8:
            Kt = 6
            print("-----punto 6 -------")
        
        Kt_list.append(Kt)
    elif x > 3 and x < 5:
        #-- "ALTA FRECUENCIA --> diferencia 3 y 5 dB"
        if Lt < 8:
            Kt = 0
            print("-----punto 7 -------")
        elif Lt >= 8 and Lt <= 12:
            Kt = 3
            print("-----punto 8 -------")
        elif Lt > 12:
            Kt = 6
            print("-----punto 9 -------")
        
        Kt_list.append(Kt)

print(Kt_list)
    