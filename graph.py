import datetime
import time
import pickle
from visitGraph import *
import overpy
import networkx as nx
import matplotlib.pyplot as plt
import os.path
api = overpy.Overpass()

def manageGraph(gpsStart, idNode, radius, listIndication, gpsStop, soup, nquadrant, algorithm):

    print(idNode)

    nameFile = "graphExport/" + str(idNode) + "_" + str(radius) + ".graph"
    print(nameFile)

    if os.path.isfile(nameFile):
        print("Grafo importato")
        # importiamo il grafo
        G = importGraph(idNode, radius)
    else:
        print("Grafo generato")
        # Generiamo il grafo
        G = nx.Graph()

        getTime()
        makeGraph(G, idNode, gpsStart, radius, soup)
        getTime()

        print("Grafo Esportato Start")
        exportGraph(G, idNode, radius)
        print("Grafo Esportato End")

    #printGraph(G)

    if algorithm == 0:
        print("------------")
        visitGraphBackTrack(G, idNode, listIndication, soup, nquadrant)
        print(listNodeBacktrack)
        node = getMinListIndication(listNodeBacktrack)
        print(node)
        nodeObjGraphBacktrack = Intersection(str(node), soup)
        print(nodeObjGraphBacktrack)
        print(getDistance(nodeObjGraphBacktrack.lat, nodeObjGraphBacktrack.lon, float(gpsStop['latitude']),
                          float(gpsStop['longitude'])))
        print("Numero di output")
        print(len(listNodeBacktrack))

        for i in range(len(listNodeBacktrack)):
            print("-------------")
            nodeObjGraphBacktrack = Intersection(str(listNodeBacktrack[i]['node']), soup)
            print(nodeObjGraphBacktrack.id)
            print(getDistance(nodeObjGraphBacktrack.lat, nodeObjGraphBacktrack.lon, float(gpsStop['latitude']),
                          float(gpsStop['longitude'])))

    elif algorithm == 1:
        print("------------")
        newCoordinate = visitGraphBestDecision(G, idNode, listIndication, soup, nquadrant)
        #print(nodeGraphBestDecision)
        #nodeObjGraphBestDecision = Intersection(nodeGraphBestDecision, soup)
        print(getDistance(newCoordinate['latitude'], newCoordinate['longitude'] , float(gpsStop['latitude']), float(gpsStop['longitude'])))

    elif algorithm == 2:
        listOutput = []
        sumDistance = 0
        for i in range(20):
            print("------------")
            nodeGraphRandomDecision = visitGraphRandomDecision(G, idNode, listIndication, soup, nquadrant)

            distance = getDistance(nodeGraphRandomDecision['latitude'], nodeGraphRandomDecision['longitude'], float(gpsStop['latitude']),
                              float(gpsStop['longitude']))
            sumDistance += distance
            listOutput.append(distance)
        print("Media")
        print(sumDistance / len(listOutput))

    elif algorithm == 3:
        calculate = algorithmDeadReckoning(gpsStart, listIndication, 50)
        print(getDistance(calculate['latitude'], calculate['longitude'], gpsStop['latitude'], gpsStop['longitude']))

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


def makeGraph(G, nodeCurrent, gpsPointStart, radius, soup):

    node = Intersection(nodeCurrent, soup)

    print("Node")
    print(node)

    distanceOrigin = getDistance(node.lat, node.lon, gpsPointStart['latitude'], gpsPointStart['longitude'])

    if (distanceOrigin <= radius):
        # ottengo la lista delle strada che posso raggiungere dal nodo appena aggiunto
        listWay = getListWayReached(nodeCurrent, soup)

        print("listWay")
        print(listWay)

        # per ogni strada ottengo la lista dei possibili incroci
        for way in range(len(listWay)):
            listIntersection = getListIntersection(listWay[way], soup)

            print("listIntersection")
            print(listIntersection)

            # per ogni incrocio richiamo la funzione
            for intersection in range(len(listIntersection)):
                # se non esiste l'arco lo aggiungo
                if not(G.has_edge(str(nodeCurrent), str(listIntersection[intersection]))) and str(nodeCurrent)!=str(listIntersection[intersection]):
                    nodeIntersection = Intersection(listIntersection[intersection], soup)
                    distanceCurrentFrom = getDistance(node.lat, node.lon, nodeIntersection.lat, nodeIntersection.lon)

                    idCommonWay = getCommonWay(nodeIntersection.id, node.id, soup)
                    road = Road(idCommonWay, soup)

                    print("Road:")
                    print(road)

                    if road.highway != "":
                        G.add_edge(str(nodeCurrent), str(listIntersection[intersection]), weight = round(distanceCurrentFrom,2))
                        print(str(nodeCurrent) + " - " + str(listIntersection[intersection]))
                        makeGraph(G, str(listIntersection[intersection]), gpsPointStart, radius, soup)



def exportGraph(G, idRoot, radius):
    nameFile = str(idRoot) + "_" + str(radius) + ".graph"
    pickle.dump(G, open('graphExport/' + nameFile, 'wb'))


def importGraph(idRoot , radius):
    nameFile = str(idRoot) + "_" + str(radius) + ".graph"
    G = pickle.load(open('graphExport/' + nameFile, 'rb'))
    return G

def getTime():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st)