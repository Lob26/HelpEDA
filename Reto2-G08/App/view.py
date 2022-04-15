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
from DISClib.ADT import map as mp
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
    print("3- Encontrar los artistas por popularidad")
    print("4- Encontrar las caciones por popularidad")
    print("5- Encontrar la cancion mas popular de un artista")
    print("6- Encontrar la discografia de un artista")
    print("7- Clasificar canciones de artistas con mayor distribucion")


catalog = None
filePrefix = ("spotify-albums-utf8", "spotify-artists-utf8" , "spotify-tracks-utf8")
fileSize = ("-01pct.csv","-small.csv", "-large.csv", "-5pct.csv", "-10pct.csv", "-20pct.csv", "-30pct.csv", "-50pct.csv", "-80pct.csv")
file = [[f'{prefix}{size}' for prefix in filePrefix] for size in fileSize]


def fifth(artistName):
	singles,compilations,albums,threeFirstLast,mostPopular = controller.r5TracksByArtist(catalog, artistName)
	print(f'Numero de sencillos: {singles}\nNumero de compilations: {compilations}\nNumero de albums: {albums}')
	for i in range(1, 7):
		print(lt.getElement(threeFirstLast, i))
	print(f'{mostPopular}')
"""
Menu principal
"""
def info(album):
  print("Informacion album:\n", album)

while True:
  printMenu()
  inputs = input('Seleccione una opción para continuar\n')
  if int(inputs[0]) == 1:
    print("Cargando información de los archivos ....")
    t1Start = process_time()
    catalog = controller.initCatalog()
    controller.loadCatalog(file[1], catalog)
    t1End = process_time()
    print("\nTiempo de ejecucion:",t1End-t1Start,"segundos")
  elif int(inputs[0]) == 2:
    pass
  elif int(inputs[0]) == 3:
    pass
  elif int(inputs[0]) == 4:
    pass
  elif int(inputs[0]) == 5:
    pass
  elif int(inputs[0]) == 6:
    #artista = input("Ingrese el nombre del artista")
    artista = "Trixie Whitley"
    fifth(artista)
  else:
    sys.exit(0)
sys.exit(0)
