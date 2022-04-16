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
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from datetime import datetime as dt
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newCatalog():
  catalog = {
  "players":None,
  "translatorShort":None,
  "translatorLong":None,
  "filled":None,
  }
  catalog["players"]=mp.newMap()#Map<Id, Player>
  catalog["translatorShort"]=mp.newMap()#Map<Player.shortname,Id>
  catalog["translatorLong"]=mp.newMap()#Map<Player.fullname, Id>
  catalog["filled"]=newReqs()
  return catalog

def newPlayer():
  player = {
  "short name":"",
  "long name":"",
  "age":0,
  "height":0,
  "weight":0,
  "d-o-b":None,
  "nacionality":"",
  "contract_value":0,
  "wage":0,
  "club":"",
  "asosiation date":None,
  "league":"",
  "potential":0.0,
  "overall":0,
  "positions":lt.newList(),
  "reputation":0.0,
  "tags":lt.newList(),
  "comments":"",
  "req6a":mp.newMap()
  }
  return player

def newReqs():
  reqs = {
  "req1":mp.newMap(),#Map<Club, List<Player>>
  "req2":mp.newMap(),#Map<Position, BST<Players(overall) -> BST<Players(potential) -> BST<Players(wage)>
  "req3":mp.newMap(),#Map<Tag,BST<Players(wage)>
  "req4":mp.newMap(),#Map<Trait, BST<Players(Date Of Birth)>>
  "req5":mp.newMap(),#Map<Propiety, Map<Player, Value>>
  "norm":mp.newMap(),#Map<Propiety, (float('inf'), float('-inf'))
  "req6b":mp.newMap()#Map<Position, List<Player>>
  }
  return reqs

def addData(catalog,playerData):
  #Build translators
  buildTranslator(catalog, playerData)
  
  #Build req1
  buildReq1(catalog, playerData)
  
  #Build req2(FirstStep)
  buildReq2(catalog, playerData)
  
  #Build req3
  buildReq3(catalog, playerData)
  
  #Build req4
  buildReq4(catalog, playerData)
  
  #Build player
  buildPlayer(catalog, playerData)



def buildTranslator(catalog, playerData):
  mp.put(catalog["translatorShort"], playerData["short_name"], playerData["sofifa_id"])
  mp.put(catalog["translatorLong"], playerData["long_name"], playerData["sofifa_id"])

def buildReq1(catalog, playerData):
  players = me.getValue(mp.get(catalog["filled"]["req1"], playerData["club_name"])) if mp.contains(catalog["filled"]["req1"], playerData["club_name"]) else lt.newList(cmpfunction=clubJoined)
  
  playerInfo1 = lt.newList()
  lt.addLast(playerInfo1, playerData["sofifa_id"])
  lt.addLast(playerInfo1, dt.strptime(playerData["club_joined"], "%Y-%m-%d"))
  
  lt.addLast(players, playerInfo1)
  mp.put(catalog["filled"]["req1"], playerData["club_name"], players)

def buildReq2(catalog, playerData):
  positionsData = playerData["player_positions"].split(",")
  for pos in positionsData:
    positions = me.getValue(mp.get(catalog["filled"]["req2"], pos)) if mp.contains(catalog["filled"]["req2"], pos) else om.newMap("BST", overall) #First level
    
    playerInfo2 = lt.newList()
    lt.addLast(playerInfo2, playerData["sofifa_id"])
    lt.addLast(playerInfo2, float(playerData["potential"]))
    lt.addLast(playerInfo2, float(playerData["wage_eur"]))
    
    om.put(positions, playerData["overall"], playerInfo2)
    mp.put(catalog["filled"]["req2"], pos, positions)

def buildReq3(catalog, playerData):
  tagsData = playerData["player_tags"].replace("#","").split(",")
  for tag in tagsData:
    tags = me.getValue(mp.get(catalog["filled"]["req3"], tag)) if mp.contains(catalog["filled"]["req3"], tag) else om.newMap("BST", wage_eur)
    
    om.put(tags, playerData["wage_eur"], playerData["sofifa_id"])
    mp.put(catalog["filled"]["req3"], tag, tags)

def buildReq4(catalog, playerData):
  traitsData = playerData["player_traits"].split(",")
  for trait in traitsData:
    traits = me.getValue(mp.get(catalog["filled"]["req4"], trait)) if mp.contains(catalog["filled"]["req4"], trait) else om.newMap("BST", dob)
    
    om.put(traits, playerData["dob"], playerData["sofifa_id"])
    mp.put(catalog["filled"]["req4"], trait, traits)

def buildReq5(catalog, playerData):
  extracted(catalog, playerData, "overall")
  extracted(catalog, playerData, "potential")
  extracted(catalog, playerData, "value_eur")
  extracted(catalog, playerData, "wage_eur")
  extracted(catalog, playerData, "age")
  extracted(catalog, playerData, "height_cm")
  extracted(catalog, playerData, "weight_kg")
  extracted(catalog, playerData, "release_clause_eur")

def extracted(catalog, playerData, key):
  pair = me.getValue(mp.get(catalog["filled"]["req5"], key)) if mp.contains(catalog["filled"]["req5"], key) else mp.newMap()
  
  mp.put(pair, playerData["sofifa_id"], playerData[key])
  mp.put(catalog["filled"]["req5"], key, pair)

def buildReq6(catalog):
  allIds = mp.keySet(catalog["players"])
  for i in range(1, lt.size(allIds)+1):
    playerId = lt.getElement(allIds, i)
    playerData = me.getValue(mp.get(catalog["players"], playerId))
    
    
    potMin, potMax = me.getValue(mp.get(catalog["filled"]["norm"], "potential")) if mp.contains(catalog["filled"]["norm"]) else (float('inf'), float('-inf'))
    vrP = (playerData["potential"] - potMin)/(potMax-potMin)
    
    heiMin, heiMax = me.getValue(mp.get(catalog["filled"]["norm"], "height")) if mp.contains(catalog["filled"]["norm"]) else (float('inf'), float('-inf'))
    vrH = (playerData["height"] - heiMin)/(heiMax-heiMin)
    
    ageMin, ageMax = me.getValue(mp.get(catalog["filled"]["norm"], "age")) if mp.contains(catalog["filled"]["norm"]) else (float('inf'), float('-inf'))
    vrA = (playerData["age"] - ageMin)/(ageMax-ageMin)
    
    valMin, valMax = me.getValue(mp.get(catalog["filled"]["norm"], "value")) if mp.contains(catalog["filled"]["norm"]) else (float('inf'), float('-inf'))
    vrV = (playerData["contract_value"] - valMin)/(valMax-valMin)


def buildPlayer(catalog, playerData):
  player = newPlayer()
  
  player["short name"] = playerData["short_name"]
  player["long name"] = playerData["long_name"]
  player["comments"] = playerData["short_name"]
  
  player["age"] = float(playerData["age"])
  player["height"] = float(playerData["height_cm"])
  player["weight"] = float(playerData["weight_kg"])
  
  player["contract_value"] = float(playerData["value_eur"])
  player["wage"] = float(playerData["wage_eur"])
  player["reputation"] = float(playerData["international_reputation"])
  
  player["potential"] = float(playerData["potential"])
  player["overall"] = float(playerData["overall"])
  
  player["league"] = playerData["league_name"]
  player["club"] = playerData["club_name"]
  player["asosiation date"] = dt.strptime(playerData["club_joined"], "%Y-%m-%d")
  
  player["d-o-b"] = dt.strptime(playerData["dob"],"%Y-%m-%d")
  player["nacionality"] = playerData["nationality_name"]
  
  it = playerData["player_positions"].split(",")
  for pos in it:
    lt.addLast(player["positions"], pos)
    posList = me.getValue(mp.get(catalog["filled"]["req6b"], pos)) if mp.contains(catalog["filled"]["norm"], pos) else lt.newList()
    lt.addLast(posList, playerData["sofifa_id"])
    mp.put(catalog["filled"]["req6b"], pos, posList)
  normalizator(catalog, player["potential"], player["age"], player["height"], player["contract_value"])
  
  it = playerData["player_tags"].split(",")
  for tag in it:
    lt.addLast(player["tags"], tag)
  
  mp.put(catalog["players"], playerData["sofifa_id"], player)


def normalizator(catalog, pPot, pAge, pHei, pVal):
  minPot, maxPot = me.getValue(mp.get(catalog["filled"]["norm"], "potential")) if mp.contains(catalog["filled"]["norm"], "potential") else (float('inf'), float('-inf'))
  minPot, maxPot = min(minPot, pPot), max(maxPot, pPot)
  
  minAge, maxAge = me.getValue(mp.get(catalog["filled"]["norm"], "age")) if mp.contains(catalog["filled"]["norm"], "age") else (float('inf'), float('-inf'))
  minAge, maxAge = min(minAge, pAge), max(maxAge, pAge)
  
  minHei, maxHei = me.getValue(mp.get(catalog["filled"]["norm"], "height")) if mp.contains(catalog["filled"]["norm"], "height") else (float('inf'), float('-inf'))
  minHei, maxHei = min(minHei, pHei), max(maxHei, pHei)
  
  minVal, maxVal = me.getValue(mp.get(catalog["filled"]["norm"], "value")) if mp.contains(catalog["filled"]["norm"], "value") else (float('inf'), float('-inf'))
  minVal, maxVal = min(minVal, pVal), max(maxVal, pVal)
  
  mp.put(catalog["filled"]["norm"], "potential", (minPot, maxPot))
  mp.put(catalog["filled"]["norm"], "age", (minAge, maxAge))
  mp.put(catalog["filled"]["norm"], "height", (minHei, maxHei))
  mp.put(catalog["filled"]["norm"], "value", (minVal, maxVal))


def overall(oa1, oa2):
  return 0 if (oa1 == oa2) else (1 if (oa1 > oa2) else -1)

def potential(pot1, pot2):
  return 0 if (pot1 == pot2) else (1 if (pot1 > pot2) else -1)

def wage_eur(weur1, weur2):
  return 0 if (weur1 == weur2) else (1 if (weur1 > weur2) else -1)

def dob(dob1, dob2):
  return 0 if (dob1 == dob2) else (1 if (dob1 > dob2) else -1)

def clubJoined(player1, player2):
  doj1 = lt.getElement(player1, 2)
  doj2 = lt.getElement(player2, 2)
  return 0 if (doj1 == doj2) else (1 if (doj1 > doj2) else -1)