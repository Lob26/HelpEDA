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


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def initCatalog():
	catalog = model.newCatalog()
	return catalog

def loadCatalog(dataFiles, catalog):
	albums, artists, tracks = dataFiles
	loadCSVFile(albums, artists, tracks)

def loadCSVFile(albumFile, artistFile, trackFile, sep=",", e = "utf-8-sig"):
	dialect = csv.excel()
	dialect.delimiter = sep
	
	with open(artistFile, encoding=e) as artistF:
		bufferArtist = csv.DictReader(artistF, dialect)
		
		
	with open(albumFile, encoding=e) as albumF:
		bufferAlbum = csv.DictReader(albumF, dialect)

	
	with open(trackFile, encoding=e) as trackF:
		bufferTrack = csv.DictReader(trackF, dialect)
		