import os

import urllib.request
from xml.dom.minidom import parseString
import gpxpy.geo
import overpass
import overpy
from bs4 import BeautifulSoup

from Road import *

api = overpy.Overpass()
api2 = overpass.API()

def getNearestNode(listNode, coordinates):
    distanceMin = 1000000000000000000000
    latNearest = 0
    lonNearest = 0
    idNearest = 0

    for i in range(len(listNode)):
        lat = listNode[i].lat
        lon = listNode[i].lon
        id = listNode[i].id

        distance = getDistance(lat, lon, coordinates['latitude'], coordinates['longitude'])

        if distance < distanceMin:
            latNearest = lat
            lonNearest = lon
            idNearest = id
            distanceMin = distance

    obj = {'latitude': float(latNearest),
           'longitude': float(lonNearest),
           'id': idNearest}

    return obj

def getDistance(latStart, lonStart, latX, lonX):
    return gpxpy.geo.haversine_distance(float(latStart), float(lonStart), float(latX), float(lonX))

def reverseGeocoding(gpsPoint, radius):
    coordinate = str(gpsPoint['latitude']) + "," + str(gpsPoint['longitude'])

    query = "(node(around:"+ str(radius) + "," + coordinate + "););out center;"
    print(query)
    result = api.query(query)
    listNode = result.nodes

    node = getNearestNode(listNode, gpsPoint)

    print("ReverseGeocoding: Node: " + str(node['id']))

    return node['id']

#TODO: rendere parametrica con numero di quadranti in cui dividere (?)
def convertDegreeToLabel(value, nquadrants):
    value = float(value)
    quadrant = ""

    if nquadrants == 8:
        if value > 337.5 or value >= 22.5:
            quadrant = "N"
        elif 22.5 < value <= 67.5:
            quadrant = "NE"
        elif 67.5 < value <= 112.5:
            quadrant = "E"
        elif 112.5 < value <= 157.5:
            quadrant = "SE"
        elif 157.5 < value <= 202.5:
            quadrant = "S"
        elif 202.5 < value <= 247.5:
            quadrant = "SO"
        elif 247.5 < value <= 292.5:
            quadrant = "O"
        elif 292.5 < value <= 337.5:
            quadrant = "NO"

    if nquadrants == 4:
        if value > 315 or value <= 45:
            quadrant = "N"
        elif 45 < value <= 135:
            quadrant = "E"
        elif 135 < value <= 225:
            quadrant = "S"
        elif 225 < value <= 315:
            quadrant = "W"


    elif nquadrants == 2:
        if value > 0 and value < 180:
            quadrant = "E"
        else:
            quadrant = "O"


    return quadrant

def getBoundingBox(lat, lon, offset):

    latRadian = math.radians(float(lat))

    degLatKm = 110.574235
    degLongKm = 110.572833 * math.cos(latRadian)
    deltaLat = offset / 1000.0 / degLatKm
    deltaLong = offset / 1000.0 / degLongKm

    minLat = float(lat) - deltaLat
    minLong = float(lon) - deltaLong
    maxLat = float(lat) + deltaLat
    maxLong = float(lon) + deltaLong

    boundingBox = {'minLat': round(minLat,4),
                   'minLon': round(minLong,4),
                   'maxLat': round(maxLat,4),
                   'maxLon': round(maxLong,4)}

    return boundingBox

def getNodeDownDx(bb):
    up = bb['maxLon']
    sx = bb['minLat']

    obj = {'latitude': sx,
           'longitude': up}

    node = reverseGeocoding(obj, 200)

    return node

def getNodeUpSx(bb):
    down = bb['minLon']
    dx = bb['maxLat']

    obj = {'latitude': dx,
           'longitude': down}

    node = reverseGeocoding(obj, 200)
    return node

def importOSM(nameFile):
    url = 'osmFile/' + nameFile
    soup = BeautifulSoup(open(url, encoding="utf8"), 'xml')
    return soup

# dato un ID e un radius mi ottengo il .osm dentro alla relativa bounding box
def getOSMfile(rootId, radius):
    nameFile = str(rootId) + "_" + str(radius) + ".osm"
    if os.path.isfile("osmFile/" + nameFile):
        print("OSM importato")
        # importiamo il grafo
        osm = importOSM(nameFile)
        return osm
    else:
        print("OSM generato")
        percentualeToAdd = 20
        offset = radius + (radius / 100 * percentualeToAdd)

        #dall'id ottengo latNode e lonNode
        query = "(node("+ str(rootId) + "););out center;"
        result = api.query(query)
        listNode = result.nodes
        latNode = float(listNode[0].lat)
        lonNode = float(listNode[0].lon)

        boundingBox = getBoundingBox(latNode, lonNode, offset)

        downdxNode = getNodeDownDx(boundingBox)
        upsxNode = getNodeUpSx(boundingBox)

        query = "(node(" + str(downdxNode) + "););out center;"
        result = api.query(query)
        downdxNode = result.nodes

        query = "(node(" + str(upsxNode) + "););out center;"
        result = api.query(query)
        upsxNode = result.nodes

        url = "http://overpass-api.de/api/map?bbox=" + str(upsxNode[0].lon) + "," + str(downdxNode[0].lat) + "," +str(downdxNode[0].lon) + "," + str(upsxNode[0].lat)

        xml = urllib.request.urlopen(url)
        dom = parseString(xml.read())

        with open("osmFile/" + nameFile, "wb") as text_file:
            text_file.write(dom.toxml().encode('utf8'))

        url = 'osmFile/' + nameFile

        soup =  BeautifulSoup(open(url,encoding="utf8"), 'xml')
        return soup