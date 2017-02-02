import gpxpy.geo
import overpy
from Road import *

api = overpy.Overpass()

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
    result = api.query(query)
    listNode = result.nodes

    node = getNearestNode(listNode, gpsPoint)

    return node['id']