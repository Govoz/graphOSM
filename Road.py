from Intersection import *
import math

class Road:
    def __init__(self, idWay, soup):
        self.id = str(idWay)

        allWay = soup.find_all('way')

        nameWay = ""
        highway = ""
        maxSpeed = 50

        for i in range(len(allWay)):
            id = allWay[i].attrs['id']
            if id == str(idWay):
                # per way si possono intendere anche aree, le road hanno il tag highway, controllo anche che abbia il name per evitare le strade di servizio e parcheggi
                # TODO: controllare
                highwayDict = allWay[i].find('tag', k='highway')
                nameWayDict = allWay[i].find('tag', k='name')

                if highwayDict != None and nameWayDict != None:
                    highway = highwayDict['v']
                    nameWay = nameWayDict['v']

                    maxSpeedDict = allWay[i].find('tag', k='maxSpeed')
                    if maxSpeedDict != None:
                        maxSpeed = maxSpeedDict['v']

        self.name = nameWay
        self.highway = highway
        self.speedLimit = maxSpeed
        #self.orientation = getOrientamentWay(self.id)

    def __str__(self):
        string = str(self.id) + " - " + str(self.name) + " - " + str(self.highway) + " - " + str(self.speedLimit)
        return string

def getListIntersection(idWay, soup):
    # ottengo tutti i nodi che appartengono alla way
    allWay = soup.find_all('way')

    listNode = []

    for i in range(len(allWay)):
        road = allWay[i]
        id = road.attrs['id']

        # ho trovato la way
        if id == str(idWay):
            # ottengo la lista di nodi all'interno del tag way
            for i in range(len(road.contents)):
                node = road.contents[i]
                if (node.name == 'nd'):
                    idNode = node['ref']
                    listNode.append(idNode)

    # filtro gli incroci
    listNodeFiltered = []
    for i in range(len(listNode)):
        listWayIntersect = getListWayReached(listNode[i], soup)
        if (len(listWayIntersect) > 1):
            listNodeFiltered.append(listNode[i])
    return list(set(listNodeFiltered))

def getListWayReached(idNode, soup):
    allNode = soup.find_all('nd')
    listWay = []

    for i in range(len(allNode)):
        node = allNode[i]

        if node['ref'] == str(idNode):
            id = node.find_parent("way", id=True)["id"]

            objWay = Road(id, soup)
            if objWay.highway != '':
                listWay.append(id)

    return listWay

#dati due ID di nodi trovo l'id della way che li congiunge
def getCommonWay(x,y, soup):
    listX = getListWayReached(x, soup)
    listY = getListWayReached(y, soup)

    listcommon =  list(set(listX).intersection(listY))
    return listcommon[0]

def getOrientamentWay(idWay, soup):
    #ottengo la lista di tutti i nodi, cerco quelli più a nord e più a sud e calcolo l'angolazione
    listIntersectionID = getListIntersection(idWay, soup)
    listIntersection = []

    for i in range(len(listIntersectionID)):
        obj = Intersection(listIntersectionID[i], soup)

        listIntersection.append(obj)

    nodeNord = getNodeNord(listIntersection)
    nodeSud = getNodeSud(listIntersection)

    latNord = math.radians(float(nodeNord.lat))
    latSud = math.radians(float(nodeSud.lat))
    lonNord = math.radians(float(nodeNord.lon))
    lonSud = math.radians(float(nodeSud.lon))

    objA = (latNord, lonNord)
    objB = (latSud, lonSud)

    x = calculate_initial_compass_bearing(objA, objB)
    return x

def getNodeNord(listIntersection):
    #get max lat
    maxLat = 0
    nodeNord = None
    for i in range(len(listIntersection)):
        if float(listIntersection[i].lat) > maxLat:
            maxLat = float(listIntersection[i].lat)
            nodeNord = listIntersection[i]

    return nodeNord

def getNodeSud(listIntersection):
    #get max lat
    minLat = 100000000
    nodeSud = None
    for i in range(len(listIntersection)):
        if float(listIntersection[i].lat) < minLat:
            minLat = float(listIntersection[i].lat)
            nodeSud = listIntersection[i]

    return nodeSud

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")


    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing