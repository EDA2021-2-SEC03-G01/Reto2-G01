"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
from datetime import date
from statistics import mode 
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos,
otra para las categorias de los mismos.
"""

# Construccion de modelos
def newCatalog(tipo_artistas, tipo_obras):
    catalog={"artists":None,"artworks":None}
    if tipo_artistas == 1:
        tipo_artistas = "ARRAY_LIST"
    else:
        tipo_artistas = "LINKED_LIST"

    if tipo_obras == 1:
        tipo_obras = "ARRAY_LIST"
    else:
        tipo_obras = "LINKED_LIST"

    catalog["artists"]=lt.newList(datastructure = tipo_artistas, cmpfunction = compareArtists)
    catalog["artworks"]=lt.newList(datastructure = tipo_obras, cmpfunction = compareArtworks)
    catalog["Medios"]=mp.newMap(34500,
                                maptype='CHAINING',
                                loadfactor=4.0,
                                )

    return catalog

# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)
    
def addArtworks(catalog, artwork):
    lt.addLast(catalog["artworks"], artwork)


def addMedium(catalog, artwork):
    lista_obras=lt.newList()
    mp.put(catalog["Medios"], artwork["Medium"], lista_obras)
    lt.addLast(mp.get(catalog["Medios"], artwork["Medium"]), artwork)
        
            

    

# Funciones para creacion de datos


# Funciones de consulta

def getFirstArtists (catalog):
    primeros = lt.newList()
    for pos in range(1, 3):
        artista = lt.getElement(catalog["artists"], pos)
        lt.addLast(primeros, artista)

    return primeros

def getLastArtists (catalog):
    ultimos = lt.newList()
    largoLista = int(lt.size(catalog["artists"]))
    for pos in range(1, largoLista + 1):
        if (largoLista - pos) < 3:
            artista = lt.getElement(catalog["artists"], pos)
            lt.addLast(ultimos, artista)

    return ultimos

def getLastArtworks (catalog):
    ultimos = lt.newList()
    largoLista = int(lt.size(catalog["artworks"]))
    for pos in range(1, largoLista + 1):
        if (largoLista - pos) < 3:
            artista = lt.getElement(catalog["artworks"], pos)
            lt.addLast(ultimos, artista)

    return ultimos

# Funciones utilizadas para comparar elementos dentro de una lista

#Artists
def compareArtists (artista1, artista2):
    if artista1["DisplayName"] < artista2["DisplayName"]:
        return -1
    elif artista1["DisplayName"] > artista2["DisplayName"]:
        return 1
    else:
        return 0

def compareYears(artista1, artista2):
    if (int(artista1["Fecha de nacimiento"]) <= int(artista2["Fecha de nacimiento"])):
        return True
    else:
        return False

#Artworks
def compareArtworks(obra1, obra2):
    if obra1["ObjectID"] < obra2["ObjectID"]:
        return -1
    elif obra1["ObjectID"] > obra2["ObjectID"]:
        return 1
    else:
        return 0

def compareDateAcquired(obra1, obra2):
    if (date.fromisoformat(obra1["Adquisicion"]) <= date.fromisoformat(obra2["Adquisicion"])):
        return True
    else:
        return False

def compareDate(obra1, obra2):
    if int(obra1["Fecha"]) <= int(obra2["Fecha"]):
        return True
    else:
        return False

def compareCosto(obra1, obra2):
    if float(obra1["Costo transporte"]) >= float(obra2["Costo transporte"]):
        return True
    else:
        return False

# Funciones de ordenamiento

#Encontrar los n primeros y ultimos de una lista
def primeros_ultimos(lista, n):
    lista_def = lt.newList()
    for pos in range(1, n+1):
        element = lt.getElement(lista, pos)
        lt.addLast(lista_def, element)
    largoLista = int(lt.size(lista))
    for pos in range(1, largoLista + 1):
        if (largoLista - pos) < n:
            element = lt.getElement(lista, pos)
            lt.addLast(lista_def, element)
    return lista_def

#Medición de tiempos de ordenamiento
def tiempo_ord_sa (lista, compare):
    start_time = time.process_time()
    lista = sa.sort(lista, compare)
    stop_time = time.process_time()
    return (stop_time - start_time)*1000

def tiempo_ord_ins (lista, compare):
    start_time = time.process_time()
    lista = ins.sort(lista, compare)
    stop_time = time.process_time()
    return (stop_time - start_time)*1000

def tiempo_ord_ms (lista, compare):
    start_time = time.process_time()
    lista = ms.sort(lista, compare)
    stop_time = time.process_time()
    return (stop_time - start_time)*1000

def tiempo_ord_qs (lista, compare):
    start_time = time.process_time()
    lista = qs.sort(lista, compare)
    stop_time = time.process_time()
    return (stop_time - start_time)*1000


# Requerimientos 

def req_1(catalog, año_in, año_fin, tipo_ord):
    start_time = time.process_time()
    lista = lt.newList()
    total = 0
    artistas = catalog["artists"]
    for i in range(1, lt.size(artistas)+1) :
    
        artista = lt.getElement(artistas, i)
        if int(artista["BeginDate"]) >= int(año_in) and int(artista["BeginDate"]) <= int(año_fin):
            dic_artist = {"nombre": artista["DisplayName"], "Fecha de nacimiento": artista["BeginDate"], 
            "Fecha de fallecimiento": artista["EndDate"],  "Nacionalidad": artista["Nationality"],  "Genero": artista["Gender"] }
            lt.addLast(lista, dic_artist)
            total += 1
    #Medir tiempos
    if tipo_ord == 1:
        elapsed_time_mseg = tiempo_ord_sa (lista, compareYears)
    elif tipo_ord == 2:
        elapsed_time_mseg = tiempo_ord_ins (lista, compareYears)
    elif tipo_ord == 3:
        elapsed_time_mseg = tiempo_ord_ms (lista, compareYears)
    else:
        elapsed_time_mseg = tiempo_ord_qs (lista, compareYears)
    #Primeros y últimos tres
    lista_def = primeros_ultimos(lista, 3)
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (total, elapsed_time_mseg, tiempo_req, lista_def)

#Encontrar los nombres de los autores
def nombres_autores(artistas, obra):
    autores = lt.newList(datastructure="ARRAY_LIST")
    idprueba = ""
    cadena = str(obra["ConstituentID"])
    for j in range(1, len(cadena)):
        if cadena[j] != "[" and cadena[j] != "," and cadena[j] != " " and cadena[j] != "]":
            idprueba += cadena[j]
        elif cadena[j] == "," or cadena[j] == "]":
            seguir = True
            while seguir:
                for i in range(1, lt.size(artistas)+1):
                    autor = lt.getElement(artistas, i)
                    if int(idprueba) == int(autor["ConstituentID"]):
                        lt.addLast(autores, autor["DisplayName"])
                        seguir = False
            idprueba = ""
    return autores
        
def req_2(catalog, fecha_in, fecha_fin, tipo_ord):
    start_time = time.process_time()
    lista = lt.newList(datastructure="ARRAY_LIST")
    total = 0
    purchase = 0
    obras = catalog["artworks"]
    artistas = catalog["artists"]
    for i in range(1, lt.size(obras)+1) :
        obra = lt.getElement(obras, i)
        if obra["DateAcquired"] != "":
            fecha_adq = date.fromisoformat(obra["DateAcquired"])
        else:
            fecha_adq = date.fromisoformat("0001-01-01")
        fecha_ini = date.fromisoformat(fecha_in)
        fecha_final = date.fromisoformat(fecha_fin)
        if fecha_adq > fecha_ini and fecha_adq < fecha_final:
            #Encontrar los nombres de los autores
            autores = nombres_autores(artistas, obra)
            #Crear el diccionario
            dic_artwork = {"Titulo": obra["Title"], "Artistas": autores, "Fecha": obra["Date"], "Medio": obra["Medium"],  "Dimensiones": obra["Dimensions"], "Adquisicion": obra["DateAcquired"]  }
            lt.addLast(lista, dic_artwork)
            total += 1
            if obra["CreditLine"] == "Purchase":
                purchase += 1       
    #Medir tiempos
    if tipo_ord == 1:
        elapsed_time_mseg = tiempo_ord_sa (lista, compareDateAcquired)
    elif tipo_ord == 2:
        elapsed_time_mseg = tiempo_ord_ins (lista, compareDateAcquired)
    elif tipo_ord == 3:
        elapsed_time_mseg = tiempo_ord_ms (lista, compareDateAcquired)
    else:
        elapsed_time_mseg = tiempo_ord_qs (lista, compareDateAcquired)
    #Primeros y últimos tres
    lista_def = primeros_ultimos(lista, 3)
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (total, purchase, elapsed_time_mseg, tiempo_req, lista_def)


def req_3(catalog, nom_artista):
    start_time = time.process_time()
    artista=nom_artista
    lista=lt.newList()
    obras_tecnica = lt.newList(datastructure="ARRAY_LIST")
    total_obras = 0
    total_tecnicas = 0
    mas_utilizada = ""
    obras = catalog["artworks"]
    artistas = catalog["artists"]
    for i in range(1, lt.size(obras)+1) :
        obra = lt.getElement(obras, i)
        autores = nombres_autores(artistas, obra)
        dic_artworks = {"Titulo": obra["Title"], "Artistas": autores, "Fecha": obra["Date"], "Medio": obra["Medium"],  "Dimensiones": obra["Dimensions"], "Adquisicion": obra["DateAcquired"]  }
        lt.addLast(lista, dic_artworks)
    for k in range(1,lt.size(lista)+1):
        for l in range(1,lt.size((lista[k]["Artistas"])+1)):
            if lista[k]["Artistas"][l] == artista:
                total_obras=+1
                lista_tecnicas=lt.newList()
                lt.addLast(lista_tecnicas, lista[k]["Medio"])
    mas_utilizada=mode(lista_tecnicas)
    for m in range(1,lt.size(lista_tecnicas)+1):
        lista_tecnicas_def=lt.newList()
        if lista_tecnicas[m] not in lista_tecnicas_def:
            lt.addLast(lista_tecnicas_def,lista_tecnicas[m])
            total_tecnicas=+1
    for n in range(1, lt.size(lista)+1):
        if artista in lista[n]["Artistas"] and lista[n]["Medio"]==mas_utilizada:
            dic_obra={"Titulo": lista[n]["Titulo"], "Fecha": lista[n]["Fecha"], "Medio": lista[n]["Medio"], "Dimensiones": lista[n]["Dimensiones"]}
            lt.addLast(obras_tecnica, dic_obra)
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (total_obras, total_tecnicas, mas_utilizada, tiempo_req, obras_tecnica)

#Encontrar las nacionalidades de los autores
def nac_autores(artistas, obra):
    autores = lt.newList(datastructure="ARRAY_LIST")
    idprueba = ""
    cadena = str(obra["ConstituentID"])
    for j in range(1, len(cadena)):
        if cadena[j] != "[" and cadena[j] != "," and cadena[j] != " " and cadena[j] != "]":
            idprueba += cadena[j]
        elif cadena[j] == "," or cadena[j] == "]":
            seguir = True
            while seguir:
                for i in range(1, lt.size(artistas)+1):
                    autor = lt.getElement(artistas, i)
                    if int(idprueba) == int(autor["ConstituentID"]):
                        lt.addLast(autores, autor["Nationality"])
                        seguir = False
            idprueba = ""
    return autores

def req_4(catalog):
    start_time = time.process_time()
    obras = catalog["artworks"]
    artistas = catalog["artists"]
    solo_nac = lt.newList(datastructure="ARRAY_LIST")
    obras_nac_mas = lt.newList(datastructure="ARRAY_LIST")
    dic_nac = {}
    for o in range(1, lt.size(obras)+1):
        obra = lt.getElement(obras, o)
        nacs = nac_autores(artistas, obra)
        for n in range(1, lt.size(nacs)+1):
            nac = lt.getElement(nacs, n)
            if lt.isPresent(solo_nac, nac) == 0:
                nacionalidad = nac
                lt.addLast(solo_nac, nacionalidad)
                dic_nac[nacionalidad] = 1
                if nac == "":
                    dic_nac["Nationality unknown"] += 1
            else:
                if nac == "":
                    dic_nac["Nationality unknown"] += 1
                else:
                    dic_nac[nac] += 1
    sorted_values = sorted(dic_nac.values(), reverse=True)
    sorted_dict = {}
    for i in sorted_values:
        for k in dic_nac.keys():
            if dic_nac[k] == i:
                if  len(sorted_dict) < 10:
                    sorted_dict[k] = dic_nac[k]
                else:
                    break
    nac_mas = list(sorted_dict.keys())[0]
    for o in range(1, lt.size(obras)+1):
        obra = lt.getElement(obras, o)
        nacs = nac_autores(artistas, obra)
        if lt.isPresent(nacs, nac_mas) != 0:
            lt.addLast(obras_nac_mas, obra)
    n_obras_nac_mas = lt.size(obras_nac_mas)
    #Primeras y últimas tres
    lista_def = primeros_ultimos(obras_nac_mas, 3)
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (sorted_dict, lista_def, nac_mas, tiempo_req, n_obras_nac_mas)

def req_5(catalog, dep):
    start_time = time.process_time()
    obras = catalog["artworks"]
    artistas = catalog["artists"]
    costo_kg = 0.0
    costo_m2 = 0.0
    costo_m3 = 0.0
    costo_tot = 0.0
    peso_tot = 0.0
    tasa = 72.00
    total_obras = 0
    costo_def = 0.0
    obras_transp = lt.newList(datastructure="ARRAY_LIST")
    obras_costos = lt.newList(datastructure="ARRAY_LIST")
    for o in range(1, lt.size(obras)+1):
        obra = lt.getElement(obras, o)
        if obra["Department"] == dep:
            peso = obra["Weight (kg)"]
            diametro = obra["Diameter (cm)"]
            circum = obra["Circumference (cm)"]
            largo = obra["Length (cm)"] 
            alto = obra["Height (cm)"]
            ancho = obra["Width (cm)"]
            prof = obra["Depth (cm)"]

            #KG
            if peso != "":
                costo_kg = float(peso) * tasa
                peso_tot += peso

            #M2
            if alto != "" and ancho != "":
                costo_m2 = (float(alto)*0.01 *float(ancho)*0.01) * tasa
            elif alto != "" and largo != "":
                costo_m2 = (float(alto)*0.01 *float(largo)*0.01)  * tasa
            elif alto != "" and prof != "":
                costo_m2 = (float(alto)*0.01 *float(prof)*0.01)  * tasa
            elif ancho != "" and largo != "":
                costo_m2 = (float(ancho)*0.01 *float(largo)*0.01)  * tasa
            elif ancho != "" and prof != "":
                costo_m2 = (float(ancho)*0.01 *float(prof)*0.01)  * tasa
            elif largo != "" and prof != "":
                costo_m2 = (float(largo)*0.01 *float(prof)*0.01)  * tasa
            elif diametro != "":
                costo_m2 = ((((float(diametro)*0.01)/2)**2) * 3,14) * tasa
            elif circum  != "":
                costo_m2 = (((float(circum)*0.01)**2)/(4 * 3,14)) * tasa
            
            #M3
            if  alto != "" and ancho != "" and prof != "":
                costo_m3 = float(alto)*0.01 * float(ancho)*0.01 * float(prof)*0.01 * tasa
            elif  alto != "" and ancho != "" and largo != "":
                costo_m3 = float(alto)*0.01 * float(ancho)*0.01 * float(largo)*0.01 * tasa
            elif  alto != "" and prof != "" and largo != "":
                costo_m3 = float(alto)*0.01 * float(prof)*0.01 * float(largo)*0.01 * tasa
            elif  ancho != "" and prof != "" and largo != "":
                costo_m3 = float(ancho)*0.01 * float(prof)*0.01 * float(largo)*0.01 * tasa
            elif diametro != "" and alto != "":
                costo_m3 = (((float(diametro)*0.01)/2)**2) * 3,14 * float(alto) * tasa
            elif diametro != "" and ancho != "":
                costo_m3 = (((float(diametro)*0.01)/2)**2) * 3,14 * float(ancho) * tasa
            elif diametro != "" and prof != "":
                costo_m3 = (((float(diametro)*0.01)/2)**2) * 3,14 * float(prof) * tasa
            elif diametro != "" and largo != "":
                costo_m3 = (((float(diametro)*0.01)/2)**2) * 3,14 * float(largo) * tasa

            costo_def = max(costo_kg, costo_m2, costo_m3)
            if costo_def == 0.0:
                costo_def = 48.00
            costo_tot += costo_def
            total_obras += 1
            autores = nombres_autores(artistas, obra)
            if (obra["Date"]) == "":
                obra["Date"] = 3000
            dic_artwork = {"Titulo": obra["Title"], "Artistas": autores, "Clasificacion":obra["Classification"], "Fecha": obra["Date"], "Medio": obra["Medium"],  "Dimensiones": obra["Dimensions"], "Costo transporte":costo_def}
            lt.addLast(obras_transp, dic_artwork)
            lt.addLast(obras_costos, dic_artwork)
    obras_transp = ms.sort(obras_transp, compareDate)
    obras_costos = ms.sort(obras_costos, compareCosto)
    #cinco más viejas
    lista_transp_def = lt.newList()
    for pos in range(1, 6):
        obra = lt.getElement(obras_transp, pos)
        lt.addLast(lista_transp_def, obra)
    #cinco más caras
    obras_costos_def = lt.newList()
    for pos in range(1, 6):
        obra = lt.getElement(obras_costos, pos)
        lt.addLast(obras_costos_def, obra)
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (total_obras, costo_tot, peso_tot, lista_transp_def, tiempo_req, obras_costos_def)

def req_6(catalog, ano_ini, ano_fin, Area_disp ):
    start_time = time.process_time()
    tot_obras_anos=0
    tot_obras=0
    Area_usada=0
    obras_usadas=lt.newList(datastructure="ARRAY_LIST")
    obras = catalog["artworks"]
    artistas=catalog["artists"]
    for i in range(1,lt.size(obras)+1):
        obra=lt.getElement(obras,i)
        if obra["DateAcquired"] != "":
            fecha_adq = date.fromisoformat(obra["DateAcquired"])
        else:
            fecha_adq = date.fromisoformat("0001-01-01")
        fecha_ini = date.fromisoformat(ano_ini + "-01-01")
        fecha_final = date.fromisoformat(ano_fin + "-12-31")
        if fecha_adq < fecha_final and fecha_adq > fecha_ini:
            tot_obras_anos=+1
            diametro = obra["Diameter (cm)"]
            circum = obra["Circumference (cm)"]
            largo = obra["Length (cm)"] 
            alto = obra["Height (cm)"]
            ancho = obra["Width (cm)"]
            prof = obra["Depth (cm)"]
            while Area_usada<float(Area_disp):
                if alto != "" and ancho != "":
                    Area_usada += (float(alto)*0.01 *float(ancho)*0.01)
                elif alto != "" and largo != "":
                    Area_usada += (float(alto)*0.01 *float(largo)*0.01) 
                elif alto != "" and prof != "":
                    Area_usada += (float(alto)*0.01 *float(prof)*0.01)
                elif ancho != "" and largo != "":
                    Area_usada += (float(ancho)*0.01 *float(largo)*0.01)
                elif ancho != "" and prof != "":
                    Area_usada += (float(ancho)*0.01 *float(prof)*0.01)
                elif largo != "" and prof != "":
                    Area_usada += (float(largo)*0.01 *float(prof)*0.01)
                elif diametro != "":
                    Area_usada += ((((float(diametro)*0.01)/2)**2) * 3,14)
                elif circum  != "":
                    Area_usada += (((float(circum)*0.01)**2)/(4 * 3,14))
                tot_obras += 1
                autores = nombres_autores(artistas, obra)
                dic_obra={"Titulo":obra["Title"], "Artista(s)":autores, "Fecha":obra["Date"], "Clasificacion":obra["Classification"], "Medio":obra["Medium"], "Dimensiones":obra["Dimensions"], "Adquisicion":obra["DateAcquired"]}
                lt.addLast(obras_usadas, dic_obra)
    obras_ord=ms.sort(obras_usadas,compareDateAcquired)
    prim_ult_5=primeros_ultimos(obras_ord, 5)
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (tot_obras_anos, tot_obras, Area_usada, tiempo_req, prim_ult_5)

def lab_5(catalog, n, medio):
    lista_obras=lt.newList(datastructure="ARRAY_LIST")
    lista_obras=mp.get(catalog["Medios"], medio)
    print(lista_obras)
    sa.sort(lista_obras, compareDateAcquired )
    lista_def = lt.newList()
    for pos in range(1, n+1):
        element = lt.getElement(lista_obras, pos)
        lt.addLast(lista_def, element)
    return lista_def


