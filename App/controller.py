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
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog(tipo_artistas, tipo_obras):
   
    catalog = model.newCatalog(tipo_artistas, tipo_obras)
    return catalog

# Funciones para la carga de datos

def loadData(catalog):

    loadArtists(catalog)
    loadArtworks(catalog)
    loadMediums(catalog)

def loadArtists(catalog):
    artistsfile = cf.data_dir + 'MoMA/Artists-utf8-small.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

def loadArtworks(catalog):
    artworksfile = cf.data_dir + 'MoMA/Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artworksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtworks(catalog, artwork)

def loadMediums(catalog):
    artworksfile = cf.data_dir + 'MoMA/Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(artworksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addMedium(catalog, artwork)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getLastArtists(catalog):
    ultimos = model.getLastArtists(catalog)
    return ultimos

def getLastArtworks(catalog):
    ultimos = model.getLastArtworks(catalog)
    return ultimos

#Requerimientos
def req_1(catalog, año_in, año_fin, tipo_ord):
    (total,elapsed_time_mseg, tiempo_req, lista) = model.req_1(catalog, año_in, año_fin, tipo_ord)
    return (total, elapsed_time_mseg, tiempo_req, lista)

def req_2(catalog, fecha_in, fecha_fin, tipo_ord):
    (total, purchase, elapsed_time_mseg, tiempo_req, lista) = model.req_2(catalog, fecha_in, fecha_fin, tipo_ord)
    return (total, purchase, elapsed_time_mseg, tiempo_req, lista)

def req_3(catalog, artista):
    (total_obras, total_tecnicas, mas_utilizada, tiempo_req, lista_obras)=model.req_3(catalog, artista)
    return (total_obras, total_tecnicas, mas_utilizada, tiempo_req, lista_obras)

def req_4(catalog):
    (sorted_dict, lista_def, nac_mas, tiempo_req, n_obras_nac_mas) = model.req_4(catalog)
    return (sorted_dict, lista_def, nac_mas, tiempo_req, n_obras_nac_mas)

def req_5(catalog, dep):
    (total_obras, costo_tot, peso_tot, lista_transp_def, tiempo_req, obras_costos_def) = model.req_5(catalog, dep)
    return (total_obras, costo_tot, peso_tot, lista_transp_def, tiempo_req, obras_costos_def)

def req_6(catalog, ano_ini, ano_fin, Area_disp):
    (tot_obras_anos, tot_obras, Area_usada, tiempo_req, prim_ult_5)= model.req_6(catalog, ano_ini, ano_fin, Area_disp)
    return (tot_obras_anos, tot_obras, Area_usada, tiempo_req, prim_ult_5)

def lab_5(catalog, n, medio):
    lista_def=model.lab_5(catalog, n, medio)
    return lista_def