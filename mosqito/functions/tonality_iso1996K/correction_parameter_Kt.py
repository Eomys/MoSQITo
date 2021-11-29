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

"""
        Parameters
        ----------
        - file: fichero.csv con los Lp promedio de las banda de tercio de octava.

        Outputs
        -------
        - Kt: parámetro de corrección por componentes tonales Kt.
"""
#-- Archivo que luego obtendrá del usuario
file = 'data.csv'

#-- Leer el archivo y extraer los datos
with open(file, 'r') as csvfile:
    data = list(csv.reader(csvfile, delimiter=","))

#-- Obtener las listas de las frec.centrales y los Lp_promedio.
fc = data[0][1:32]
Lp_mean = data[1][1:32]

#-- Longitud de las listas, las 2 tienen la misma long.
Lp_len = len(Lp_mean)

#-- Lista donde se guardaran los indices correspondientes a las posiciones donde hay 
#-- un tono prominente
Kt_values = []

for x in range (0, Lp_len):
        if x > 0 and x < 30:
            #-- Variables a comparar
            print("---------------------------------------")
            Lf_prev = int(Lp_mean[x-1])
            print(Lf_prev)
            Lf = int(Lp_mean[x])
            print(Lf)
            Lf_post = int(Lp_mean[x+1])
            print(Lf_post)
            print("---------------------------------------")

            #-- calculamos Ls
            print("---------------------------------------")
            Ls = (Lf_post - Lf_prev) / 2
            print (Ls)

            #-- Calculamos Lt
            Lt = Lf - Ls
            print(Lt)
            print("---------------------------------------")

            #-- Comparar niveles para determinar si es un tono prominente.
            if x > 0 and x < 9:
                #-- "BAJA FRECUENCIA --> diferencia entre 8 y 12 dB"
                if Lt < 8:
                    Kt = 0
                elif Lt >= 8 and Lt <= 12:
                    Kt = 3
                elif Lt > 12:
                    Kt = 6
                #-- Guardo el valor de Kt para todas las banda de tercio de octaba en el rango
                #-- de baja frecuencia.
                Kt_values.append(Kt)
                print("Kt de BAJA FREC ")
                print(Kt)
            elif x > 8 and x < 14:
                #-- "MEDIA FRECUENCIA --> diferencia entre 5 y 8 dB"
                if Lt < 5:
                    Kt = 0
                elif Lt >= 5 and Lt <= 8:
                    Kt = 3
                elif Lt > 8:
                    Kt = 6
                #-- Guardo el valor de Kt para todas las banda de tercio de octaba en el rango
                #-- de media frecuencia.
                Kt_values.append(Kt)
                print("Kt de MEDIA FREC ")
                print(Kt)
            elif x > 13 and x < 28:
                #-- "ALTA FRECUENCIA --> diferencia entre 3 y 5 dB"
                if Lt < 3:
                    Kt = 0
                elif Lt >= 3 and Lt <= 5:
                    Kt = 3
                elif Lt > 5:
                    Kt = 6
                #-- Guardo el valor de Kt para todas las banda de tercio de octaba en el rango
                #-- de baja frecuencia.
                Kt_values.append(Kt)
                print("Kt de ALTA FREC ")
                print(Kt)
print("---------------------------------------")
print(Kt_values)