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
#-------------
#Constructor
#-------------
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
		"release_date":None,
		"relevant_track_name":"",
		"tracks_name":lt.newList("ARRAY_LIST"),
		"artist_album_name":"",
		"total_tracks":0,
		"album_type":"",
		"external_urls":"",
		"market":lt.newList("ARRAY_LIST")
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
		"artist_names":lt.newList(),
		"href":""
	}
	return track
#-------------
#Loader
#-------------
def addArtist(catalog, data:dict):
	artist = newArtist()
	artist.update(data)
	artist["genres"] = parseList(data["genres"])
	mp.put(catalog["artist"], data["id"], artist)

def addAlbum(catalog, data:dict):
	album = newAlbum()
	album.update(data)
	album["artist_album_name"] = getArtist(catalog, data["artist_id"])
	album["relevant_track_name"] = getTrack(catalog, data["track_id"])
	album["release_date"] = cleanDate(date["release_date"], date["release_date_precision"])
	listMarket = parseList(data["available_markets"])
	for market in listMarket:
		lt.addLast(album["market"], market)
	mp.put(catalog["albums"], data["id"], album)

def addTrack(catalog, data:dict):
	track = newTrack()
	track.update(data)
	track["album_name"] = getAlbum(catalog, data["album_id"])["name"]
	lt.addLast(getAlbum(catalog, data["album_id"])["tracks_name"], track["name"])
	listArtists = parseList(data["arist_id"])
	for artistId in listArtits:
		artist = getArtist(catalog, artistId)
		lt.addLast(artist["tracks"], track["name"])
		lt.addLast(track["artist_names"], artist["name"])
	mp.put(catalog["tracks"], data["id"], track)

#-------------
#Helper
#-------------
def cleanDate(date:String, precision:String):
	if(precision=="month"):
		date+="-01-01"
	if(precision=="day"):
		date+="-01"
	return parseDate(date, "%Y-%m-%d")

#-------------
#Getters
#-------------
def getAlbum(catalog, id:String):
	return mp.get(catalog["albums"], id)

def getArtist(catalog, id:String):
	return mp.get(catalog["artists"], id)

def getTrack(catalog, id:String):
	return mp.get(catalog["tracks"], id)

#-------------
#Requeriments
#-------------
def examAlbumsInYear(catalog, year):
	totalAlbums=0
	firstMonthAlbums=0
	threeFirstLast=lt.newList("ARRAY_LIST")
	return (totalAlbums, firstMonthAlbums, threeFirstLast)

def findArtistByPopularity(catalog, popularity):
	artist=0
	threeFirstLast=lt.newList("ARRAY_LIST")
	return (artist, threeFirstLast)

def findTracksByPopularity(catalog, popularity):
	tracks=0
	threeFirstLast=lt.newList("ARRAY_LIST")
	return (tracks, threeFirstLast)

def findArtistMostPopularTrack(catalog, artist, market):
	tracksArtistMarket=0
	albumsArtistMarket=0
	mostPopular=None
	return (tracksArtistMarket, albumsArtistMarket)

def getDiscographyByArtist(catalog, artist):
	singles=0
	compilations=0
	albums=0
	threeFirstLast=lt.newList("ARRAY_LIST")
	mostPopular=None
	return (singles,compilations, albums,threeFirstLast, mostPopular)

def clasifyMostDistributedTracks(catalog, artist, market, number):
	mostCountedMarket=lt.newList("ARRAY_LIST")
	threeFirstLast=lt.newList("ARRAY_LIST")
	return (mostCountedMarket, threeFirstLast)