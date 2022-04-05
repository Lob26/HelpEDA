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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from datetime import datetime as newDateTime
from datetime import strftime as getDate
from datetime import strptime as parseDate
from json import loads as parseList

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newCatalog():
	catalog = {
		"tracks" = None,
		"artists" = None,
		"albums" = None,
	}
	catalog["tracks"] = mp.newMap()
	catalog["artists"] = mp.newMap()
	catalog["albums"] = mp.newMap()
	return catalog

def newArtist():
	artist={
		"name":"",
		"artist_popularity":0,
		"followers":0,
		"relevant_track_name":"",
		"genres":lt.newList("ARRAY_LIST"),
		"tracks":lt.newList("ARRAY_LIST")
	}
	return artist

def newAlbum():
	album = {
		"name":"",
		"release_date":"",
		"relevant_track_name":"",
		"tracks_name":lt.newList("ARRAY_LIST"),
		"artist_album_name":"",
		"total_tracks":0,
		"album_type":"",
		"external_urls":"",
		"market":lt.newArrayList("ARRAY_LIST")
	}
	return album

def newTrack():
	track={
		"name":"",
		"popularity":0,
		"album_name":"",
		"disc_number":0,
		"track_number":0,
		"duration_ms":0,
		"artist_names":lt.newArrayList(),
		"href":""
	}
	return track

def addArtist(catalog, data:dict):
	artist = newArtist()
	artist.update(data)
	artist["genres"] = parseList(data["genres"])
	mp.put(catalog["artist"], data["id"], artist)

def addAlbum(catalog, data:dict):
	album = newAlbum()
	album.update(data)
	album["artist_album_name"] = getArtist(data["artist_id"])
	album["relevant_track_name"] = getTrack(data["track_id"])
	listMarket = parseList(data["available_markets"])
	for market in listMarket:
		lt.addLast(album["market"], market)
	mp.put(catalog["albums"], data["id"], album)

def addTrack(catalog, data:dict):
	track = newTrack()
	track.update(data)
	track["album_name"] = getAlbum(data["album_id"])["name"]
	lt.addLast(getAlbum(data["album_id"])["tracks_name"], track["name"])
	listArtists = parseList(data["arist_id"])
	for artistId in listArtits:
		artist = getArtist(artistId)
		lt.addLast(artist["tracks"], track["name"])
		lt.addLast(track["artist_names"], artist["name"])
		
	