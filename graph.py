from osmUtils import *
from Intersection import Intersection
from Road import *
import overpy
import networkx as nx
import matplotlib.pyplot as plt

api = overpy.Overpass()

global G
G = nx.Graph()
global listNodeVisited
listNodeVisited = []


def createGraph(gpsPoint, idNode, radius):
    #creiamo il grafo

    nodeRoot = Intersection(idNode)
    G.add_node(nodeRoot.id, data=nodeRoot)

    makeGraph(idNode, idNode, gpsPoint, radius)

    printGraph(G)


def printGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    plt.show()


# Questa è ricorsiva. (G è il grafo in cui opero, nodeFrom è il nodo da cui parte l'edge, nodeCurrent è il nodo che sto analizzando, radius è il raggio
def makeGraph(nodeFrom, nodeCurrent, gpsPointStart, radius):

    listNodeVisited.append(nodeCurrent)

    nodeNew = Intersection(nodeCurrent)
    nodeOld = Intersection(nodeFrom)

    # mi calcolo la distanza da Root del nodo corrente
    distanceOrigin = getDistance(nodeNew.lat, nodeNew.lon, gpsPointStart['latitude'], gpsPointStart['longitude'])
    # mi calcolo la distanza tra i due nodi analizzati, sarà il peso dell'edge
    distanceCurrentFrom = getDistance(nodeNew.lat, nodeNew.lon, nodeOld.lat, nodeOld.lon)

    # se la distanza è minore allora lo considero
    if (distanceOrigin <= radius):

        # controllo se i nodi sono diversi, utile nella prima istanza della funzione
        if nodeNew.id != nodeOld.id:

            # ottengo l'id dell'edge
            idCommonWay = getCommonWay(nodeOld.id, nodeNew.id)

            road = Road(idCommonWay)

            # mi creo il nuovo nodo
            G.add_node(nodeNew.id, data = nodeNew)

            print("CREATO NODO " + str(nodeNew.id))

            # collego il nuovo nodo a quello parent (?) dovrei aggiungere anche distanceCurrentFrom
            G.add_edge(nodeNew.id, nodeOld.id, data = road)

            print("CREATO EDGE " + str(nodeNew.id) + " - " + str(nodeOld.id))

            #printGraph(G)

            nodeOld = nodeNew

            # ottengo la lista delle strada che posso raggiungere dal nodo appena aggiunto
            listWay = getListWayReached(nodeOld.id)

            # per ogni strada ottengo la lista dei possibili incroci
            for way in range(len(listWay)):
                listIntersection = getListIntersection(listWay[way])

                # per ogni incrocio richiamo la funzione
                for intersection in range(len(listIntersection)):
                    if not(listIntersection[intersection] in listNodeVisited):
                        makeGraph(nodeOld.id, listIntersection[intersection], gpsPointStart, radius)

            return

        # è il caso in cui gli id sono gli stessi (quindi la prima istanza
        else:
            # ottengo la lista delle strada che posso raggiungere dal nodo appena aggiunto
            listWay = getListWayReached(nodeOld.id)

            # per ogni strada ottengo la lista dei possibili incroci
            for way in range(len(listWay)):
                listIntersection = getListIntersection(listWay[way])

                # per ogni incrocio richiamo la funzione
                for intersection in range(len(listIntersection)):
                    if not (listIntersection[intersection] in listNodeVisited):
                        makeGraph(nodeOld.id, listIntersection[intersection], gpsPointStart, radius)

            return

    return



