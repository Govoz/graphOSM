import json

import pickle
from networkx.readwrite import json_graph

from osmUtils import *
from Intersection import Intersection
from Road import *
import overpy
import networkx as nx
import matplotlib.pyplot as plt

api = overpy.Overpass()

# global G
# G = nx.Graph()
global listNodeVisited
listNodeVisited = []

def manageGraph(gpsPoint, idNode, radius):
    #creiamo il grafo

    # nodeRoot = Intersection(idNode)
    # print(nodeRoot)
    # G.add_node(nodeRoot.id)
    #
    # makeGraph(idNode, idNode, gpsPoint, radius)

    G = importGraph()
    printGraph(G)

    #visitGraph(idNode)

def visitGraph(idRoot):
    print(G.neighbors(idRoot))

#TODO: sistemare le coordinate in maniera che assomigli alla cartina
def printGraph(G):
    pos = nx.spring_layout(G)

    # nodes
    nx.draw_networkx_nodes(G, pos,node_size=100, alpha=0.3)
    nx.draw_networkx_edges(G, pos, scale=3)
    nx.draw_networkx_labels(G, pos, font_size=6)

    labels = nx.get_edge_attributes(G, 'data')

    for key in labels:
        name = labels[key].name
        labels[key] = name

    nx.draw_networkx_edge_labels(G, pos, font_size=6, edge_labels=labels)

    plt.axis('off')
    plt.show()  # display


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
        if str(nodeNew.id) != str(nodeOld.id):

            # ottengo l'id dell'edge
            idCommonWay = getCommonWay(nodeOld.id, nodeNew.id)

            road = Road(idCommonWay)
            if road.name != "":

                # mi creo il nuovo nodo
                G.add_node(nodeNew.id)

                print("CREATO NODO " + str(nodeNew.id))

                # collego il nuovo nodo a quello parent (?) dovrei aggiungere anche distanceCurrentFrom
                G.add_edge(nodeNew.id, nodeOld.id, weight = round(distanceCurrentFrom,2))

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


def exportGraph():
    pickle.dump(G, open('pippo.graph', 'wb'))


def importGraph():
    G = pickle.load(open('pippo.graph', 'rb'))
    return G