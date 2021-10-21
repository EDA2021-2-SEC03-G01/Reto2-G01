"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import time
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Ordenar cronológicamente los artistas")
    print("3- Ordenar cronológicamente las adquisiciones")
    print("4- Clasificar las obras de un artista por su técnica")
    print("5- Clasificar las obras por la nacionalidad de sus creadores")
    print("6- Transportar obras de un departamento")
    print("7- BONO")
    print("8- Consultar las n obras más antiguas por un medio especifico")
    print("9- Consultar cuantas obras tienen una nacionalidad especifica")
    print("0- Salir")

def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1: 
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        start_time = time.process_time()
        loadData(catalog)
        stop_time = time.process_time()
        tiempo = (stop_time - start_time)*1000
        print('\nArtistas cargados: ' + str(mp.size(catalog['artists'])))
        print('\nÚltimos tres artistas:')
        ultimos_artistas = controller.getLastArtists(catalog)
        for artista in lt.iterator(ultimos_artistas):
            print(artista)
        print('\nObras cargadas: ' + str(mp.size(catalog['artworks'])))
        print('\nÚltimas tres obras:')
        ultimas_obras = controller.getLastArtworks(catalog)
        for obra in lt.iterator(ultimas_obras):
            print(obra)
        print("\nMedios cargados: " + str(mp.size(catalog["Medios"])))
        print("\nNacionalidades cargadas: " + str(mp.size(catalog["Nacionalidades"])))
        print("\nDepartamentos cargados: " + str(mp.size(catalog["Departamentos"])))
        print("\nEl tiempo de carga fue: " + str(tiempo)+"\n")

    elif int(inputs[0]) == 2:
        año_in = int(input("Ingrese el año inicial: "))
        año_fin = int(input("Ingrese el año final: "))
        (total, tiempo_req, artistas) = controller.req_1(catalog, año_in, año_fin)
        print("\nHay " + str(total) + " artistas entre " + str(año_in) + " y " + str(año_fin))
        print("\nA continuación se muestran los primeros y ultimos tres: ")
        for artista in lt.iterator(artistas):
            print(artista)
        print("\nEl tiempo de respuesta para este requerimiento fue: " + str(tiempo_req)+"\n")

    elif int(inputs[0]) == 3:
        fecha_in = (input("Ingrese la fecha inicial (YYYY-MM-DD): "))
        fecha_fin = (input("Ingrese la fecha final (YYYY-MM-DD): "))
        (total, purchase, tiempo_req, obras) = controller.req_2(catalog, fecha_in, fecha_fin)
        print("\nFueron adquiridas " + str(total) + " obras entre " + str(fecha_in) + " y " + str(fecha_fin))
        print(str(purchase) + " de estas fueron compradas. ")
        print("\nA continuación se muestran las primeras y ultimas tres: ")
        for obra in lt.iterator(obras):
            print(obra)
        print("\nEl tiempo de respuesta para este requerimiento fue: " + str(tiempo_req)+"\n")

    elif int(inputs[0]) == 4:
        artista=input("Ingrese el nombre del artista de interés:  ")
        (total_obras, total_tecnicas, mas_utilizada, tiempo_req, obras_tecnica, primeras_ultimas) = controller.req_3(catalog, artista)
        print("\n"+ artista + " tiene un total de " + str(total_obras) + " obras en el museo.")
        print("Hay " + str(total_tecnicas) + " tipos diferentes de medios/tecnicas en su colección.")
        print("Su tecnica mas utilizada es " + mas_utilizada)
        print("\nA continuación se muestran las obras en las que " + artista + " utilizó esta tecnica")
        for obra in lt.iterator(primeras_ultimas):
            print(obra)
        print("\nEl tiempo de respuesta para este requerimiento fue: " + str(tiempo_req)+"\n")

    elif int(inputs[0]) == 5:
        (sorted_dict, primeros_ultimos, nac_mas, tiempo_req, n_obras_nac_mas) = controller.req_4(catalog)
        print("\nEl Top 10 de nacionalidades en el MoMA es:\n " + str(sorted_dict))
        print("La nacionalidad más frecuente en el MoMA es " + (nac_mas) + " con " + str(n_obras_nac_mas) + " obras únicas.")
        print("\nA continuación se muestran las primeras y últimas tres: ")
        for obra in lt.iterator(primeros_ultimos):
            print(obra)
        print("\nEl tiempo de respuesta para este requerimiento fue: " + str(tiempo_req)+"\n")
    
    elif int(inputs[0]) == 6:
        dep = input("Ingrese el departamento del que desea transportar las obras: ")
        (total_obras, costo_tot, peso_tot, lista_transp_def, tiempo_req, obras_costos_def) = controller.req_5(catalog, dep)
        print("\nEl costo por transportar las obras del departamento " + dep + " fue: " + str(costo_tot))
        print("El numero total de obras por transportar es " + str(total_obras))
        print("El peso total de las obras es de: " + str(peso_tot))
        print("\nLas cinco obras más antiguas por transportar son: ")
        for obra in lt.iterator(lista_transp_def):
            print(obra)
        print("\nLas cinco obras más costosas por transportar son: ")
        for obra in lt.iterator(obras_costos_def):
            print(obra)
        print("\nEl tiempo de respuesta para este requerimiento fue: " + str(tiempo_req)+"\n")
    
    elif int(inputs[0]) == 7:
        año_in=input("Ingrese el año inicial: ")
        año_fin=input("Ingrese el año final: ")
        n=input("Ingrese el numero de artistas que desea consultar: ")
        (lista_def,tiempo_req) = controller.bono (catalog, año_in, año_fin, n)
        for artista in lt.iterator(lista_def):
            print(artista)
        print("\nEl tiempo de respuesta para este requerimiento fue: " + str(tiempo_req)+"\n")

    #LABORATORIOS
    elif int(inputs[0]) == 8:
        medio=input("Ingrese el medio de interés: ")
        n=input("Ingrese el numero de obras que desea consultar: ")
        lista_def=controller.lab_5(catalog, n, medio)
        print(lista_def)

    elif int(inputs[0]) == 9:
        nacionalidad=input("Ingrese la nacionalidad de interés: ")
        n_obras=controller.lab_6(catalog, nacionalidad)
        print(str(n_obras) + " obras tienen esta nacionalidad")

    else:
        sys.exit(0)

sys.exit(0)

#Drawings & Prints
