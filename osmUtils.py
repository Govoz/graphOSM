import gpxpy.geo
import overpass
import overpy
from Road import *

api = overpy.Overpass()
api2 = overpass.API()

global osmFile
osmFile = None

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

def reverseGeocoding(gpsPoint):
    coordinate = str(gpsPoint['latitude']) + "," + str(gpsPoint['longitude'])

    query = "(node(around:50," + coordinate + "););out center;"
    print(query)
    result = api.query(query)
    listNode = result.nodes

    node = getNearestNode(listNode, gpsPoint)

    print("ReverseGeocoding: Node: " + str(node['id']))

    return node['id']

#TODO: rendere parametrica con numero di quadranti in cui dividere (?)
def convertDegreeToLabel(value):
    value = float(value)
    # if value > 315 or value <= 45:
    #     quadrant = "N"
    # elif 45 < value <= 135:
    #     quadrant = "E"
    # elif 135 < value <= 225:
    #     quadrant = "S"
    # elif 225 < value <= 315:
    #     quadrant = "W"

    if value > 0 and value < 180:
        quadrant = "E"
    else:
        quadrant = "O"
    return quadrant

def getBoundingBox(lat, lon, offset):
    print(type(offset))
    latRadian = math.radians(float(lat))

    degLatKm = 110.574235
    degLongKm = 110.572833 * math.cos(latRadian)
    deltaLat = offset / 1000.0 / degLatKm
    deltaLong = offset / 1000.0 / degLongKm
    print(deltaLat)
    print(deltaLong)
    minLat = float(lat) - deltaLat
    minLong = float(lon) - deltaLong
    maxLat = float(lat) + deltaLat
    maxLong = float(lon) + deltaLong

    boundingBox = {'minLat': minLat,
                   'minLon': minLong,
                   'maxLat': maxLat,
                   'maxLon': maxLong}

    return boundingBox


# dato un ID e un radius mi ottengo il .osm dentro alla relativa bounding box
def getOSMfile(rootId, radius):

    percentualeToAdd = 20
    offset = radius + (radius / 100 * percentualeToAdd)

    rootNode = Intersection(rootId)
    latNode = rootNode.lat
    lonNode = rootNode.lon

    boundingBox = getBoundingBox(latNode, lonNode, offset)

    query = "(node(" + str(boundingBox['minLat']) +"," + str(boundingBox['minLon']) + "," + str(boundingBox['maxLat']) + "," + str(boundingBox['maxLon']) + ");<;);out meta;"
    print(query)
    #osm = api2.Get(query, responseformat="xml")
