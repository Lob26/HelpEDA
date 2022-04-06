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

import sys
import config as cf
import controller
from DISClib.ADT import list as lt
assert cf
from time import process_time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Examinar los albumes en un anio de interes")

catalog = None
filePrefix = ("spotify-albums-utf8", "spotify-artists-utf8" , "spotify-tracks-utf8")
fileSize = ("-01pct.csv","-small.csv", "-large.csv", "-5pct.csv", "-10pct.csv", "-20pct.csv", "-30pct.csv", "-50pct.csv", "-80pct.csv")
file = [[f'{prefix}{size}' for prefix in filePrefix] for size in fileSize]

"""
Menu principal
"""
while True:
	printMenu()
	inputs = input('Seleccione una opción para continuar\n')
	if int(inputs[0]) == 1:
		print("Cargando información de los archivos ....")
		t1Start = process_time()
		catalog = controller.initCatalog()
		controller.loadCatalog(file[0], catalog)
		t1End = process_time()
		print("\nTiempo de ejecucion:",t1End-t1Start,"segundos")
	
	elif int(inputs[0]) == 2:
		year = input("Ingrese el anio de interes")
		if (len(year)!= 4):
			print("Anio incorrecto")
		else:
			first(year)
	elif int(inputs[0]) == 3:
		pass
	elif int(inputs[0]) == 4:
		pass
	elif int(inputs[0]) == 5:
		pass
	elif int(inputs[0]) == 6:
		pass
	else:
		sys.exit(0)
sys.exit(0)

def first(year):
	totalNum, firstMonth, askedAlbums = controller.r1AlbumsInYear(catalog, year)
	for i in range(lt.size(askedAlbums)):
		album = lt.getElement(askedAlbums, i)

def second(popularity):
	artist, askedArtists = controller.r2ArtistByPopularity(catalog, popularity)
	for i in range(lt.size(askedArtists)):
		artist = lt.getElement(askedArtists, i)

def third(popularity):
	tracks, askedTracks = controller.r3FindTracksByPopularity(catalog, popularity)
	for i in range(lt.size(askedTracks)):
		track = lt.getElement(askedTracks, i)

def forth(artistName, market):
	tracksArtistMarket, albumsArtistMarket = controller.r4TrackMostPopularByArtist(catalog, artistName, market)

def fifth(artistName):
	singles,compilations,albums,threeFirstLast,mostPopular = controller.r5TracksByArtist()

def sixth(market, artistName, number):
	mostCountedMarket, threeFirstLast = controller.r6TracksMostDistributedByArtists(catalog, market, artistName, number)