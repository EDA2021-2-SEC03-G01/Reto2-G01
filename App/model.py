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


from DISClib.DataStructures.arraylist import iterator
from DISClib.DataStructures.chaininghashtable import get
import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.DataStructures import mapentry as me
from datetime import date
from statistics import mode 
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos,
otra para las categorias de los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog={}

    catalog["artists"]=mp.newMap(30446, 
                                maptype='PROBING',
                                loadfactor=0.5, 
                                )
    catalog["artists_date"]=mp.newMap(30446, 
                                maptype='PROBING',
                                loadfactor=0.5, 
                                )
    catalog["artworks"]=mp.newMap(276300,
                                maptype='PROBING',
                                loadfactor=0.5,
                                )
    catalog["artworks_dateAcq"]=mp.newMap(276300, 
                                maptype='PROBING',
                                loadfactor=0.5, 
                                )
    catalog["Medios"]=mp.newMap(10597,
                                maptype='CHAINING',
                                loadfactor=2.0,
                                )
    catalog["Nacionalidades"]=mp.newMap(61,
                                maptype='CHAINING',
                                loadfactor=2.0,
                                )
    catalog["Nacionalidades2"]=mp.newMap(61,
                                maptype='CHAINING',
                                loadfactor=2.0,
                                )
    catalog["Departamentos"]=mp.newMap(5,
                                maptype='CHAINING',
                                loadfactor=2.0,
                                )
    catalog["ObjectIDs"] = lt.newList(datastructure="ARRAY_LIST")
    catalog["ConstituentIDs"] = lt.newList(datastructure="ARRAY_LIST")                         

    return catalog

# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    if not mp.contains(catalog["artists"], artist["ConstituentID"]):
        #Lista de Constituent IDs
        lt.addLast(catalog["ConstituentIDs"], artist["ConstituentID"])
        #Artistas por Constituent ID
        mp.put(catalog["artists"], artist["ConstituentID"], artist)
        #Artistas por Date
        if mp.contains(catalog["artists_date"], artist["BeginDate"]):
            lista_artistas = mp.get(catalog["artists_date"], artist["BeginDate"])["value"]
            lt.addLast(lista_artistas, artist)
            mp.put(catalog["artists_date"], artist["BeginDate"], lista_artistas)
        else:
            lista_artistas=lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lista_artistas, artist)
            mp.put(catalog["artists_date"], artist["BeginDate"], lista_artistas)  

def addArtworks(catalog, artwork):
    if not mp.contains(catalog["artworks"], artwork["ObjectID"]):
        #Lista de Object IDs
        lt.addLast(catalog["ObjectIDs"], artwork["ObjectID"])
        #Obras por Object ID
        mp.put(catalog["artworks"], artwork["ObjectID"], artwork)
        #Obras por DateAcquired
        if artwork["DateAcquired"] == "":
            artwork["DateAcquired"] = "0001-01-01"
        if mp.contains(catalog["artworks_dateAcq"], artwork["DateAcquired"]):
            lista_obras = mp.get(catalog["artworks_dateAcq"], artwork["DateAcquired"])["value"]
            lt.addLast(lista_obras, artwork)
            mp.put(catalog["artworks_dateAcq"], artwork["DateAcquired"], lista_obras)
        else:
            lista_obras=lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lista_obras, artwork)
            mp.put(catalog["artworks_dateAcq"], artwork["DateAcquired"], lista_obras)  
        #Lista de IDs de autores
        listaIDs = artwork["ConstituentID"]
        listaIDs = listaIDs.replace("[", "").replace("]", "").split(", ")
        lista_nombres = lt.newList(datastructure="ARRAY_LIST")
        for id in listaIDs:
            if mp.contains(catalog["artists"], id):
                #Lista de nombres de autores
                artista = mp.get(catalog["artists"], id)["value"]
                nombre = artista["DisplayName"]
                lt.addLast(lista_nombres, nombre)
                #Mapa Nacionalidades
                nacionalidad = artista["Nationality"]
                if mp.contains(catalog["Nacionalidades"], nacionalidad):
                    lista_obras = mp.get(catalog["Nacionalidades"], nacionalidad)["value"]
                    lt.addLast(lista_obras, artwork)
                    mp.put(catalog["Nacionalidades"], nacionalidad, lista_obras)
                else:
                    lista_obras = lt.newList(datastructure="ARRAY_LIST", cmpfunction=compareDate)
                    lt.addLast(lista_obras, artwork)
                    mp.put(catalog["Nacionalidades"], nacionalidad, lista_obras)
                #Mapa Nacionalidades (obras únicas)
                if mp.contains(catalog["Nacionalidades2"], nacionalidad):
                    lista_obras = mp.get(catalog["Nacionalidades2"], nacionalidad)["value"]
                    if artwork not in lista_obras['elements']:
                        lt.addLast(lista_obras, artwork)
                    mp.put(catalog["Nacionalidades2"], nacionalidad, lista_obras)
                else:
                    lista_obras = lt.newList(datastructure="ARRAY_LIST", cmpfunction=compareDate)
                    lt.addLast(lista_obras, artwork)
                    mp.put(catalog["Nacionalidades2"], nacionalidad, lista_obras)
        #Agregar lista de nombres de autores al dic de cada obra
        artwork["AuthorsNames"] = lista_nombres
        #Mapa Medios
        if mp.contains(catalog["Medios"], artwork["Medium"]):
            lista_obras = mp.get(catalog["Medios"], artwork["Medium"])["value"]
            lt.addLast(lista_obras, artwork)
            mp.put(catalog["Medios"], artwork["Medium"], lista_obras)
        else:
            lista_obras=lt.newList(datastructure="ARRAY_LIST", cmpfunction=compareDateAcquired)
            lt.addLast(lista_obras, artwork)
            mp.put(catalog["Medios"], artwork["Medium"], lista_obras)
        #Mapa Departamentos
        if mp.contains(catalog["Departamentos"], artwork["Department"]):
            lista_obras = mp.get(catalog["Departamentos"], artwork["Department"])["value"]
            lt.addLast(lista_obras, artwork)
            mp.put(catalog["Departamentos"], artwork["Department"], lista_obras)
        else:
            lista_obras=lt.newList(datastructure="ARRAY_LIST")
            lt.addLast(lista_obras, artwork)
            mp.put(catalog["Departamentos"], artwork["Department"], lista_obras)


# Funciones de consulta
def getFirtsArtists (catalog):
    pimeros = lt.newList(datastructure="ARRAYLIST")
    listaConsIDs = catalog["ConstituentIDs"]
    id1 = lt.getElement(listaConsIDs, 1)
    id2 = lt.getElement(listaConsIDs, 2)
    id3 = lt.getElement(listaConsIDs, 3)
    artista1 = mp.get(catalog["artists"], id1)["value"]
    artista2 = mp.get(catalog["artists"], id2)["value"]
    artista3 = mp.get(catalog["artists"], id3)["value"]
    lt.addLast(pimeros, artista1)
    lt.addLast(pimeros, artista2)
    lt.addLast(pimeros, artista3)
    return pimeros

def getFirstsArtworks (catalog):
    pimeros = lt.newList(datastructure="ARRAYLIST")
    listaObjIDs = catalog["ObjectIDs"]
    id1 = lt.getElement(listaObjIDs, 1)
    id2 = lt.getElement(listaObjIDs, 2)
    id3 = lt.getElement(listaObjIDs, 3)
    obra1 = mp.get(catalog["artworks"], id1)["value"]
    obra2 = mp.get(catalog["artworks"], id2)["value"]
    obra3 = mp.get(catalog["artworks"], id3)["value"]
    lt.addLast(pimeros, obra1)
    lt.addLast(pimeros, obra2)
    lt.addLast(pimeros, obra3)
    return pimeros

def getLastArtists (catalog):
    ultimos = lt.newList(datastructure="ARRAYLIST")
    listaConsIDs = catalog["ConstituentIDs"]
    sizeConsIds = int(lt.size(listaConsIDs))
    id1 = lt.getElement(listaConsIDs, sizeConsIds-2)
    id2 = lt.getElement(listaConsIDs, sizeConsIds-1)
    id3 = lt.getElement(listaConsIDs, sizeConsIds)
    artista1 = mp.get(catalog["artists"], id1)["value"]
    artista2 = mp.get(catalog["artists"], id2)["value"]
    artista3 = mp.get(catalog["artists"], id3)["value"]
    lt.addLast(ultimos, artista1)
    lt.addLast(ultimos, artista2)
    lt.addLast(ultimos, artista3)
    return ultimos

def getLastArtworks (catalog):
    ultimas = lt.newList(datastructure="ARRAYLIST")
    listaObjIDs = catalog["ObjectIDs"]
    sizeObjIds = int(lt.size(listaObjIDs))
    id1 = lt.getElement(listaObjIDs, sizeObjIds-2)
    id2 = lt.getElement(listaObjIDs, sizeObjIds-1)
    id3 = lt.getElement(listaObjIDs, sizeObjIds)
    obra1 = mp.get(catalog["artworks"], id1)["value"]
    obra2 = mp.get(catalog["artworks"], id2)["value"]
    obra3 = mp.get(catalog["artworks"], id3)["value"]
    lt.addLast(ultimas, obra1)
    lt.addLast(ultimas, obra2)
    lt.addLast(ultimas, obra3)
    return ultimas

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

def compareNumeroObras(artista1, artista2):
    if (int(artista1["Total Obras"]) <= int(artista2["Total Obras"])):
        return True
    else:
        return False

def compareNumeroTecnicas(artista1, artista2):
    if (int(artista1["Total Tecnicas"]) <= int(artista2["Total Tecnicas"])):
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

def compareValues(dic1, dic2):
    v1 = list(dic1.values())[0]
    v2 = list(dic2.values())[0]
    if v1 >= v2:
        return True
    else:
        return False

# Funciones de ordenamiento
def sort_obras_nac (lista_obras):
    lista_obras = sa.sort(lista_obras, compareDate)
    return lista_obras

def sort_obras_medios (lista_obras):
    lista_obras = sa.sort(lista_obras, compareDateAcquired)
    return lista_obras

#Encontrar los n primeros y ultimos de una lista
def f_primeros_ultimos(lista, n):
    lista_def = lt.newList(datastructure="ARRAYLIST")
    for pos in range(1, n+1):
        element = lt.getElement(lista, pos)
        lt.addLast(lista_def, element)
    largoLista = int(lt.size(lista))
    for pos in range(1, largoLista + 1):
        if (largoLista - pos) < n:
            element = lt.getElement(lista, pos)
            lt.addLast(lista_def, element)
    return lista_def


# Requerimientos 

#listo
def req_1(catalog, año_in, año_fin):
    start_time = time.process_time()
    lista = lt.newList(datastructure="ARRAY_LIST")
    total = 0
    artistas_date = catalog["artists_date"]
    lista_dates = mp.keySet(artistas_date)
    for date in lt.iterator(lista_dates):
        if int(date) >= int(año_in) and int(date) <= int(año_fin):
            lista_artistas = mp.get(artistas_date, date)["value"]
            for artista in lt.iterator(lista_artistas):
                dic_artist = {"nombre": artista["DisplayName"], "Fecha de nacimiento": artista["BeginDate"], 
                "Fecha de fallecimiento": artista["EndDate"],  "Nacionalidad": artista["Nationality"],  "Genero": artista["Gender"] }
                lt.addLast(lista, dic_artist)
                total += 1
    #Primeros y últimos tres
    lista_ord = ms.sort(lista, compareYears)
    lista_def = f_primeros_ultimos(lista_ord, 3)
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (total, tiempo_req, lista_def)

#listo
def req_2(catalog, fecha_in, fecha_fin):
    start_time = time.process_time()
    lista = lt.newList(datastructure="ARRAY_LIST")
    total = 0
    purchase = 0
    obras_dateAcq = catalog["artworks_dateAcq"]
    lista_dateAcq = mp.keySet(obras_dateAcq)
    for dateAcq in lt.iterator(lista_dateAcq):
        dateAcqq = date.fromisoformat(dateAcq)
        fecha_inn = date.fromisoformat(fecha_in)
        fecha_finn = date.fromisoformat(fecha_fin)
        if dateAcqq > fecha_inn and dateAcqq < fecha_finn:
            lista_obras = mp.get(obras_dateAcq, dateAcq)["value"]
            for obra in lt.iterator(lista_obras):
                #Crear el diccionario
                dic_artwork = {"Titulo": obra["Title"], "Artistas": obra["AuthorsNames"], "Fecha": obra["Date"], "Medio": obra["Medium"], "Dimensiones": obra["Dimensions"], "Adquisicion": obra["DateAcquired"]  }
                lt.addLast(lista, dic_artwork)
                total += 1
                if obra["CreditLine"] == "Purchase":
                    purchase += 1       
    if lt.size(lista) > 0:
        lista_ord = ms.sort(lista, compareDateAcquired)
        #Primeros y últimos tres
        lista_def = f_primeros_ultimos(lista_ord, 3)       
    else:
        lista_def = None
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (total, purchase, tiempo_req, lista_def)

#TOMÁS - listo
def req_3(catalog, nom_artista):
    start_time = time.process_time()
    artista=nom_artista
    lista=lt.newList(datastructure="ARRAYLIST")
    obras_tecnica = lt.newList(datastructure="ARRAY_LIST")
    total_obras = 0
    total_tecnicas = 0
    mas_utilizada = ""
    obras = catalog["artworks"]
    lista_obras = mp.keySet(obras)
    lista_tecnicas=lt.newList(datastructure="ARRAYLIST")
    for id_obra in lt.iterator(lista_obras):
        obra=mp.get(obras, id_obra)["value"]
        for autor in lt.iterator(obra["AuthorsNames"]):
            if autor == artista:
                total_obras += 1
                lt.addLast(lista_tecnicas, obra["Medium"])
    lista_tecnicas_def=lt.newList(datastructure="ARRAYLIST")
    for tecnica in lt.iterator(lista_tecnicas):
        if tecnica not in lista_tecnicas_def:
            lt.addLast(lista_tecnicas_def,tecnica)
            total_tecnicas += 1
    mayor=0
    for tecnica_def in lt.iterator(lista_tecnicas_def):
        for tecnica in lt.iterator(lista_tecnicas):
            num_tecnica=0
            if tecnica == tecnica_def:
                num_tecnica +=1
        if num_tecnica>mayor:
            mayor=num_tecnica
            mas_utilizada=tecnica
    for id_obra in lt.iterator(lista_obras):
        obra=mp.get(obras, id_obra)["value"]
        if artista in obra["AuthorsNames"]["elements"] and obra["Medium"]==mas_utilizada:
            dic_obra={"Titulo": obra["Title"], "Fecha": obra["Date"], "Medio": obra["Medium"], "Dimensiones": obra["Dimensions"]}
            lt.addLast(obras_tecnica, dic_obra)
    primeras_ultimas = f_primeros_ultimos(obras_tecnica, 3)
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (total_obras, total_tecnicas, mas_utilizada, tiempo_req, obras_tecnica, primeras_ultimas)

#DANIELA - listo
def req_4(catalog):
    start_time = time.process_time()
    #solo_nac = lt.newList(datastructure="ARRAY_LIST")
    nacs = lt.newList(datastructure="ARRAY_LIST", cmpfunction=compareValues)
    map_obras = catalog["Nacionalidades"]
    map_obras_unicas = catalog["Nacionalidades2"]
    lista_nac = mp.keySet(map_obras)
    for nac in lt.iterator(lista_nac):
        dic_nac = {}
        lista_obras = mp.get(map_obras, nac)["value"]
        v_nac = lt.size(lista_obras)
        dic_nac[nac] = v_nac
        lt.addLast(nacs, dic_nac)
    #Ordenar nacionalidades
    nacs_ord = ms.sort(nacs, compareValues)
    #Top 10 nacionalidades
    nac_top10 = lt.subList(nacs_ord, 1, 10)
    nac_top_dic = lt.getElement(nac_top10, 1)
    nac_top = str(list(nac_top_dic.keys())[0])
    #Lista obras ÚNICAS del Top nacionalidad
    obras_unicas_top = mp.get(map_obras_unicas, nac_top)["value"]
    #Número obras ÚNICAS del Top nacionalidad
    num_unicas_top = lt.size(obras_unicas_top)
    #Primeras y últimas tres obras UNICAS del Top nacionalidad
    primeros_ultimos = f_primeros_ultimos(obras_unicas_top, 3)
    #Tiempo
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (nac_top10, primeros_ultimos, nac_top, tiempo_req, num_unicas_top)

#listo
def req_5(catalog, dep):
    start_time = time.process_time()
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
    obras_dep = mp.get(catalog["Departamentos"], dep)["value"]
    for obra in lt.iterator(obras_dep):
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
            peso_tot += float(peso)

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
            costo_m2 = ((((float(diametro)*0.01)/2)**2) * 3.14) * tasa
        elif circum  != "":
            costo_m2 = (((float(circum)*0.01)**2)/(4 * 3.14)) * tasa
        
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
            costo_m3 = (((float(diametro)*0.01)/2)**2) * 3.14 * float(alto) * tasa
        elif diametro != "" and ancho != "":
            costo_m3 = (((float(diametro)*0.01)/2)**2) * 3.14 * float(ancho) * tasa
        elif diametro != "" and prof != "":
            costo_m3 = (((float(diametro)*0.01)/2)**2) * 3.14 * float(prof) * tasa
        elif diametro != "" and largo != "":
            costo_m3 = (((float(diametro)*0.01)/2)**2) * 3.14 * float(largo) * tasa

        costo_def = max(costo_kg, costo_m2, costo_m3)
        if costo_def == 0.0:
            costo_def = 48.00
        costo_tot += costo_def
        total_obras += 1
        if (obra["Date"]) == "":
            obra["Date"] = 3000
        dic_artwork = {"Titulo": obra["Title"], "Artistas": obra["AuthorsNames"], "Clasificacion":obra["Classification"], "Fecha": obra["Date"], "Medio": obra["Medium"],  "Dimensiones": obra["Dimensions"], "Costo transporte":costo_def}
        lt.addLast(obras_transp, dic_artwork)
        lt.addLast(obras_costos, dic_artwork)
    obras_transp = ms.sort(obras_transp, compareDate)
    obras_costos = ms.sort(obras_costos, compareCosto)
    #cinco más viejas
    lista_transp_def = lt.newList(datastructure="ARRAYLIST")
    for pos in range(1, 6):
        obra = lt.getElement(obras_transp, pos)
        lt.addLast(lista_transp_def, obra)
    #cinco más caras
    obras_costos_def = lt.newList(datastructure="ARRAYLIST")
    for pos in range(1, 6):
        obra = lt.getElement(obras_costos, pos)
        lt.addLast(obras_costos_def, obra)
    stop_time = time.process_time()
    tiempo_req = (stop_time - start_time)*1000
    return (total_obras, costo_tot, peso_tot, lista_transp_def, tiempo_req, obras_costos_def)


#LABORATORIOS
def lab_5(catalog, n, medio):
    lista_obras=lt.newList(datastructure="ARRAY_LIST")
    a=mp.get(catalog["Medios"], medio)
    print(a)
    lista_obras = me.getValue(a)
    print(lista_obras)
    sa.sort(lista_obras, compareDateAcquired )
    lista_def = lt.newList(datastructure="ARRAYLIST")
    for pos in range(1, n+1):
        element = lt.getElement(lista_obras, pos)
        lt.addLast(lista_def, element)
    return lista_def

def lab_6(catalog, nacionalidad):
    nacion=mp.get(catalog["Nacionalidades"], nacionalidad)
    lista_obras=me.getValue(nacion)
    return lt.size(lista_obras)
