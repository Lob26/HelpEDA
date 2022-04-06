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


from time import strptime
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from datetime import datetime 
from json import loads

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
#-------------
#Constructor
#-------------
def newCatalog():
	catalog = {
        "tracks": None,
		"artists": None,
		"albums": None,
	            }
	catalog["tracks"] = mp.newMap()
	catalog["artists"] = mp.newMap()
	catalog["albums"] = mp.newMap()
	return catalog

def newArtist():
	artist={
		"name":"",
		"artist_popularity":0.0,
		"followers":0,
		"track_id":"",
		"relevant_track_name":"",
		"genres":lt.newList("ARRAY_LIST"),
		"singles":lt.newList("ARRAY_LIST"),
		"compilations":lt.newList("ARRAY_LIST"),
		"albums":lt.newList("ARRAY_LIST")
	}
	return artist

def newAlbum():
	album = {
		"name":"",
		"release_date":None,
		"track_id":"",
		"relevant_track_name":"",
		"tracks_name":lt.newList("ARRAY_LIST"),
		"artist_id":"",
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
		"album_id":"",
		"album_name":"",
		"disc_number":0,
		"track_number":0,
		"duration_ms":0,
		"artists_id":lt.newList(),
		"artists_name":lt.newList(),
		"href":""
	}
	return track
#-------------
#Loader
#-------------
def addArtist(catalog, arData):
	artist = newArtist()
	artist["name"] = arData["name"]
	artist["artist_popularity"] = float(arData["artist_popularity"])
	artist["followers"] = int(float(arData["followers"]))
	artist["track_id"] = arData["track_id"]
	genres = parseList(arData["genres"])
	if type(genres) == str:
		lt.addLast(artist["genres"], genres)
	else:
		for genre in genres:
			lt.addLast(artist["genres"], genre)

	mp.put(catalog["artists"], arData["id"], artist)

def addAlbum(catalog, alData):
	album = newAlbum()
	album["name"] = alData["name"]
	album["release_date"] = cleanDate(alData["release_date"], alData["release_date_precision"])
	album["track_id"] = alData["track_id"]
	album["artist_id"] = alData["artist_id"]
	album["total_tracks"] = int(float(alData["total_tracks"]))
	album["album_type"] = alData["album_type"]
	album["external_urls"] = parseList(alData["external_urls"])
	markets = parseList(alData["available_markets"])
	if type(markets) == str:
		lt.addLast(album["market"], markets)
	else:
		for market in markets:
			lt.addLast(album["market"], market)
	mp.put(catalog["albums"], alData["id"], album)
	
def addTrack(catalog, trData):
	track = newTrack()
	track["name"] = trData["name"]
	track["popularity"] = float(trData["popularity"])
	track["album_id"] = trData["album_id"]
	track["disc_number"] = int(float(trData["disc_number"]))
	track["duration_ms"] = int(float(trData["duration_ms"]))
	artists = parseList(trData["artists_id"])
	if type(artists) == str:
		lt.addLast(track["artists_id"], artists)
	else:
		for artist in artists:
			lt.addLast(track["artists_id"], artist)
	track["href"] = trData["href"]
	mp.put(catalog["tracks"], trData["id"], track)

def purify(catalog):
	purifyTracks(catalog)
	purifyAlbums(catalog)
	purifyArtists(catalog)
	
def purifyTracks(catalog):
	keys = mp.keySet(catalog["tracks"])
	for id in range(lt.size(keys)):
		keyId = lt.getElement(keys, id)
		track = getTrack(catalog, keyId)
		tempAlb = getAlbum(catalog, track["album_id"])
		track["album_name"] = "" if tempAlb in (None, "") else tempAlb["name"]
		
		lt.addLast(tempAlb["tracks_name"],track["name"])
		mp.put(catalog["albums"], track["album_id"], tempAlb)
		
		listId = track["artists_id"]
		for i in range(lt.size(listId)):
			artistId = lt.getElement(listId, i)
			tempArt = getArtist(catalog, artistId)
			if tempArt in (None, ""):
				artist = ""
			else:
				artist = tempArt["name"]
				type = tempAlb["album_type"]
				if type == "single":
					lt.addLast(artist["single"],track["name"])
				elif type == "compilation":
					lt.addLast(artist["compilation"],track["name"])
				else:
					lt.addLast(artist["albums"],track["name"])
				mp.put(catalog["artists"], artistId, tempArt)
			lt.addLast(track["artists_name"], artist)
		mp.put(catalog["tracks"], keyId, track)

def purifyAlbums(catalog):
	keys = mp.keySet(catalog["albums"])
	for id in range(lt.size(keys)):
		keyId = lt.getElement(keys, id)
		album = getAlbum(catalog, keyId)
		tempArt = getArtist(catalog, album["artist_id"])
		album["artist_name"] = "" if tempArt in (None, "") else tempArt["name"]
		mp.put(catalog["albums"], keyId, album)

def purifyArtists(catalog):
	keys = mp.keySet(catalog["artists"])
	for id in range(lt.size(keys)):
		keyId = lt.getElement(keys, id)
		artist = getArtist(catalog, keyId)
		tempTra = getTrack(catalog, artist["track_id"])
		artist["relevant_track_name"] = "" if tempTra in (None, "") else tempTra["name"]
			
#-------------
#Helper
#-------------
def cleanDate(date, precision):
	if(precision=="year"):
		date+="-01-01"
	if(precision=="month"):
		date+="-01"
	return datetime.strptime(date, "%Y-%m-%d")

def parseList(var):
	var = f'"{var}"'
	return loads(var)
    
#-------------
#Getters
#-------------
def getAlbum(catalog, id):
	tempAlbum = mp.get(catalog["albums"], id)
	if tempAlbum is not None:
		return me.getValue(tempAlbum)
	return ""

def getArtist(catalog, id):
	tempArtist = mp.get(catalog["artists"], id)
	if tempArtist is not None:
		return me.getValue(tempArtist)
	return ""

def getTrack(catalog, id):
	tempTrack = mp.get(catalog["tracks"], id)
	if tempTrack is not None:
		return me.getValue(tempTrack)
	return ""

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