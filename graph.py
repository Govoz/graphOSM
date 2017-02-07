import pickle
from osmUtils import *
from Road import *
from visitGraph import *
import overpy
import networkx as nx
import matplotlib.pyplot as plt
import os.path
api = overpy.Overpass()

def manageGraph(gpsStart, idNode, radius, listIndication, gpsStop):

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

        makeGraph(G, idNode, gpsStart, radius)

        print("Grafo Esportato Start")
        exportGraph(G, idNode, radius)
        print("Grafo Esportato End")

    printGraph(G)

    #listIndication la uso come stack, quindi inverto l'ordine degli elementi in quanto pop e push dal fondo
    listIndication.reverse()


    print("------------")
    visitGraphBackTrack(G, idNode, listIndication)
    print(lastNodeVisitedGraphBackTrack)
    nodeObjGraphBacktrack = Intersection(lastNodeVisitedGraphBackTrack)
    print(getDistance(nodeObjGraphBacktrack.lat, nodeObjGraphBacktrack.lon, float(gpsStop['latitude']),
                      float(gpsStop['longitude'])))

    # print("------------")
    # nodeGraphBestDecision = visitGraphBestDecision(G, idNode, listIndication)
    # print(nodeGraphBestDecision)
    # nodeObjGraphBestDecision = Intersection(nodeGraphBestDecision)
    # print(getDistance(nodeObjGraphBestDecision.lat, nodeObjGraphBestDecision.lon , float(gpsStop['latitude']), float(gpsStop['longitude'])))

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


def makeGraph(G, nodeCurrent, gpsPointStart, radius):

    node = Intersection(nodeCurrent)
    distanceOrigin = getDistance(node.lat, node.lon, gpsPointStart['latitude'], gpsPointStart['longitude'])

    if (distanceOrigin <= radius):
        # ottengo la lista delle strada che posso raggiungere dal nodo appena aggiunto
        listWay = getListWayReached(nodeCurrent)
        # per ogni strada ottengo la lista dei possibili incroci
        for way in range(len(listWay)):
            listIntersection = getListIntersection(listWay[way])

            # per ogni incrocio richiamo la funzione
            for intersection in range(len(listIntersection)):
                # se non esiste l'arco lo aggiungo
                if not(G.has_edge(str(nodeCurrent), str(listIntersection[intersection]))) and str(nodeCurrent)!=str(listIntersection[intersection]):
                    nodeIntersection = Intersection(listIntersection[intersection])
                    distanceCurrentFrom = getDistance(node.lat, node.lon, nodeIntersection.lat, nodeIntersection.lon)

                    idCommonWay = getCommonWay(nodeIntersection.id, node.id)
                    road = Road(idCommonWay)
                    if road.name != "":
                        G.add_edge(str(nodeCurrent), str(listIntersection[intersection]), weight = round(distanceCurrentFrom,2))
                        print(str(nodeCurrent) + " - " + str(listIntersection[intersection]))
                        makeGraph(G, str(listIntersection[intersection]), gpsPointStart, radius)



def exportGraph(G, idRoot, radius):
    nameFile = str(idRoot) + "_" + str(radius) + ".graph"
    pickle.dump(G, open('graphExport/' + nameFile, 'wb'))


def importGraph(idRoot , radius):
    nameFile = str(idRoot) + "_" + str(radius) + ".graph"
    G = pickle.load(open('graphExport/' + nameFile, 'rb'))
    return G