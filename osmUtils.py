import gpxpy.geo
import overpy

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
    precision = 5
    listWaysFiltered = []

    while (len(listWaysFiltered) == 0):
        query = "(way(around:" + str(precision) + "," + coordinate + "););out center;"
        result = api.query(query)
        listWays = result.ways
        precision += 5

        if (len(listWays) > 0):
            # Siccome possono esserci anche aree o quant'altro filtro le highway
            listWaysFiltered = []
            for way in range(len(listWays)):
                typeWay = listWays[way].tags.get("highway")
                if (typeWay != None):
                    listWaysFiltered.append(listWays[way])

    idWay = listWaysFiltered[0].id

    return idWay