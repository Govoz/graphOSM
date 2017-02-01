import lxml
from bs4 import BeautifulSoup

global soup

soup = BeautifulSoup(open('map.osm'), 'xml')


class Road:
    def __init__(self, idWay):
        self.id = str(idWay)

        allWay = soup.find_all('way')

        nameWay = ""
        highway = ""
        maxSpeed = 50

        for i in range(len(allWay)):
            id = allWay[i].attrs['id']
            if id == str(idWay):
                # per way si possono intendere anche aree, le road hanno il tag highway
                # TODO: controllare
                highwayDict = allWay[i].find('tag', k='highway')
                if highwayDict != None:
                    highway = highwayDict['v']

                    nameWayDict = allWay[i].find('tag', k='name')
                    if nameWayDict != None:
                        nameWay = nameWayDict['v']

                    maxSpeedDict = allWay[i].find('tag', k='maxSpeed')
                    if maxSpeedDict != None:
                        maxSpeed = maxSpeedDict['v']

        self.name = nameWay
        self.highway = highway
        self.speedLimit = maxSpeed
        self.orientation = 0

    def __str__(self):
        string = str(self.id) + " - " + str(self.name) + " - " + str(self.highway) + " - " + str(self.speedLimit) + " - " + str(self.orientation)
        return string

def getListIntersection(idWay):
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
        listWayIntersect = getListWayReached(listNode[i])
        if (len(listWayIntersect) > 1):
            listNodeFiltered.append(listNode[i])
    return listNodeFiltered

def getListWayReached(idNode):
    allNode = soup.find_all('nd')
    listWay = []

    for i in range(len(allNode)):
        node = allNode[i]
        # idNodeTuples =
        if node['ref'] == str(idNode):
            id = node.find_parent("way", id=True)["id"]
            listWay.append(id)

    return listWay

#dati due ID di nodi trovo l'id della way che li congiunge
def getCommonWay(x,y):
    listX = getListWayReached(x)
    listY = getListWayReached(y)

    listcommon =  list(set(listX).intersection(listY))
    return listcommon[0]
