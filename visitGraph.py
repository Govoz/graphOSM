import random

from osmUtils import *
global listNodeVisitedGraph
listNodeVisitedGraph = []
global lastNodeVisitedGraphBackTrack
lastNodeVisitedGraphBackTrack = None

def visitGraphBackTrack(G, idRoot, listIndication, soup, nquadrant):
    print("Nodo corrente: " + str(idRoot))

    # evito di estrarre un elemento da una lista vuota
    if len(listIndication) > 0 and (G.has_node(str(idRoot))):
        indication = listIndication.pop()

        listNodeVisitedGraph.append(str(idRoot))

        indicationDirection = indication['direction']

        print("Indicazione")
        print(indicationDirection)

        # ottengo la lista di vicini
        listNeighbors = G.neighbors(str(idRoot))
        if (len(listNeighbors) > 0):
            print("Lista Vicini:")
            print(listNeighbors)

            currentNode = Intersection(idRoot, soup)
            coordinateCurrentNode = (float(currentNode.lat), float(currentNode.lon))

            # per ogni vicino mi cerco la strada che la collega e mi ricavo il limite di velocità
            for element in range(len(listNeighbors)):

                # se l'elemento non è stato già visitato
                if not (str(listNeighbors[element]) in listNodeVisitedGraph):

                    print("Neighbor che esamino: ")
                    print(listNeighbors[element])

                    # ottengo l'obj del neighbors
                    neighNode = Intersection(listNeighbors[element], soup)

                    # per ogni vicino guardo se è nella stessa direzione dell'indicazione
                    coordinateElement = (float(neighNode.lat), float(neighNode.lon))
                    directionElement = calculate_initial_compass_bearing(coordinateCurrentNode, coordinateElement)
                    labelDirectionElement = convertDegreeToLabel(directionElement, nquadrant)

                    print("Il current per arrivare a Neighboor deve andare a " + str(labelDirectionElement))

                    if (str(labelDirectionElement) is str((indicationDirection))):
                        print("Stessa Direzione -> Analizzo")

                        road = Road(getCommonWay(idRoot, listNeighbors[element], soup), soup)
                        print("La strada è : ")
                        print(road)

                        speedLimit = float(road.speedLimit)
                        speedLimit = 20

                        time = float(indication['time'])
                        meterXsec = float(speedLimit / 3.6)
                        # meter sono i metri fatti nella finestra temporale in indicationDirection
                        meterWindows = meterXsec * time

                        print("Nella windows ho percorso: " + str(meterWindows))

                        # mi calcolo la distanza tra i due nodi
                        distance = getDistance(currentNode.lat, currentNode.lon, neighNode.lat, neighNode.lon)
                        print("Tra i due nodi la distanza è : " + str(distance))

                        # se i metri nella windows sono maggiori rispetto a quelli consumati, mi calcolo i rimanenti e riappendo alla lista delle indicazioni
                        if meterWindows > distance:
                            meterRemaining = meterWindows - distance
                            # converto i metri in secondi tenendo conto dello speedLimit
                            timeRemaining = meterRemaining / meterXsec

                            obj = {'value': indication['value'], 'direction': labelDirectionElement,
                                   'time': timeRemaining}
                            listIndication.append(obj)

                        #lastNodeVisitedGraphBackTrack = str(idRoot)
                        visitGraphBackTrack(G, listNeighbors[element], listIndication, soup, nquadrant)

                    else:
                        print("Direzione Errata -> Ignoro")
                        listIndication.append(indication)

    else:
        print("La visita si è fermata a: " + str(idRoot))


# dato un nodo corrente e una lista di nodi da visitare, restituisce il nodo che rispecchia l'indicazione
# se ce ne sono di più mi restituisce il più vicino
def decisionNeighbors(idCurrentNode, listNeighbors, indicationCurrent, soup, nquadrants):
    print(listNeighbors)
    labelIndication = indicationCurrent['direction']
    listNodeSameDirection = []
    nodeToVisit = None

    currentNode = Intersection(idCurrentNode, soup)

    for i in range(len(listNeighbors)):
        neighborCurrent = Intersection(listNeighbors[i], soup)
        bearing = calculate_initial_compass_bearing(currentNode.getTuplesCoordinate(),
                                                    neighborCurrent.getTuplesCoordinate())
        labelBearing = convertDegreeToLabel(bearing, nquadrants)

        print(listNeighbors[i])
        print("Bearing: " + str(bearing))
        print("Bearing Label: " + str(labelBearing))
        print("Indicazione: " + str(labelIndication))

        if labelBearing == labelIndication:
            listNodeSameDirection.append(listNeighbors[i])

    if (len(listNodeSameDirection) > 1):
        nodeToVisit = getNearestNodeVisit(listNodeSameDirection, idCurrentNode, soup)
    elif (len(listNodeSameDirection) == 1):
        nodeToVisit = listNodeSameDirection[0]

    return nodeToVisit


def visitGraphBestDecision(G, idCurrentNode, listIndication, soup, nquadrant):
    lastBestNeighborsID = None

    # smetto di iterare quando ho finito le indicazioni da consumare
    while (len(listIndication) > 0):

        #se il grafo contiene questo nodo allora vuol dire che mi trovo in un nodo valido
        if (G.has_node(str(idCurrentNode))):

            print("CurrentNode: " + str(idCurrentNode))

            #ottengo l'indicazione corrente e il nodo da cui parto a consumarla
            indicationCurrent = listIndication.pop()
            currentNode = Intersection(idCurrentNode, soup)

            # indico che il nodo che sto esaminando è stato visitato
            listNodeVisitedGraph.append(idCurrentNode)

            # ottengo la lista dei vicini
            listNeighbors = (G.neighbors(str(idCurrentNode)))
            bestNeighborsID = decisionNeighbors(idCurrentNode, listNeighbors, indicationCurrent, soup, nquadrant)

            if (bestNeighborsID != None):
                bestNeighborsNode = Intersection(bestNeighborsID, soup)

                print("BestChoise: " + str(bestNeighborsID))

                road = Road(getCommonWay(idCurrentNode, bestNeighborsID, soup), soup)
                speedLimit = float(road.speedLimit)

                time = float(indicationCurrent['time'])
                meterXsec = float(speedLimit / 3.6)
                # meter sono i metri fatti nella finestra temporale in indicationDirection
                meterWindows = meterXsec * time

                # mi calcolo la distanza tra i due nodi
                distance = getDistance(currentNode.lat, currentNode.lon, bestNeighborsNode.lat, bestNeighborsNode.lon)

                # se i metri nella windows sono maggiori rispetto a quelli consumati, mi calcolo i rimanenti e riappendo alla lista delle indicazioni
                if meterWindows > distance:
                    meterRemaining = meterWindows - distance
                    # converto i metri in secondi tenendo conto dello speedLimit
                    timeRemaining = meterRemaining / meterXsec

                    obj = {'value': indicationCurrent['value'], 'direction': indicationCurrent, 'time': timeRemaining}
                    listIndication.append(obj)

                idCurrentNode = bestNeighborsID
                lastBestNeighborsID = bestNeighborsID
            else:
                print("Nessuna scelta possibile")
                break

    return (lastBestNeighborsID)


def getNearestNodeVisit(listNodeId, idCurrentNode, soup):
    distanceMin = 1000000000000000000000
    idNearest = 0

    currentNode = Intersection(idCurrentNode, soup)

    for i in range(len(listNodeId)):
        node = Intersection(listNodeId[i], soup)

        lat = node.lat
        lon = node.lon
        id = node.id

        distance = getDistance(lat, lon, currentNode.lat, currentNode.lon)

        if distance < distanceMin:
            idNearest = id
            distanceMin = distance

    return idNearest

def visitGraphRandomDecision(G, idCurrentNode, listIndication, soup, nquadrant):
    lastRandomNeighborsID = None

    # passo per valore la lista
    listIndication = listIndication[:]

    # smetto di iterare quando ho finito le indicazioni da consumare
    while (len(listIndication) > 0):

        #se il grafo contiene questo nodo allora vuol dire che mi trovo in un nodo valido
        if (G.has_node(str(idCurrentNode))):
            #print("CurrentNode: " + str(idCurrentNode))

            #ottengo l'indicazione corrente e il nodo da cui parto a consumarla
            indicationCurrent = listIndication.pop()
            currentNode = Intersection(idCurrentNode, soup)

            # indico che il nodo che sto esaminando è stato visitato
            listNodeVisitedGraph.append(idCurrentNode)

            # ottengo la lista dei vicini
            listNeighbors = (G.neighbors(str(idCurrentNode)))
            NextNeighborsID = randomDecision(idCurrentNode, listNeighbors, indicationCurrent, soup, nquadrant)

            if (NextNeighborsID != None):
                bestNeighborsNode = Intersection(NextNeighborsID, soup)

                #print("RandomChoise: " + str(NextNeighborsID))

                road = Road(getCommonWay(idCurrentNode, NextNeighborsID, soup), soup)
                speedLimit = float(road.speedLimit)

                time = float(indicationCurrent['time'])
                meterXsec = float(speedLimit / 3.6)
                # meter sono i metri fatti nella finestra temporale in indicationDirection
                meterWindows = meterXsec * time

                # mi calcolo la distanza tra i due nodi
                distance = getDistance(currentNode.lat, currentNode.lon, bestNeighborsNode.lat, bestNeighborsNode.lon)

                # se i metri nella windows sono maggiori rispetto a quelli consumati, mi calcolo i rimanenti e riappendo alla lista delle indicazioni
                if meterWindows > distance:
                    meterRemaining = meterWindows - distance
                    # converto i metri in secondi tenendo conto dello speedLimit
                    timeRemaining = meterRemaining / meterXsec

                    obj = {'value': indicationCurrent['value'], 'direction': indicationCurrent, 'time': timeRemaining}
                    listIndication.append(obj)

                idCurrentNode = NextNeighborsID
                lastRandomNeighborsID = NextNeighborsID
            else:
                print("Nessuna scelta possibile")
                break

    return (lastRandomNeighborsID)

def randomDecision(idCurrentNode, listNeighbors, indicationCurrent, soup, nquadrant):
    labelIndication = indicationCurrent['direction']
    listNodeSameDirection = []
    nodeToVisit = None
    currentNode = Intersection(idCurrentNode, soup)

    for i in range(len(listNeighbors)):
        neighborCurrent = Intersection(listNeighbors[i], soup)
        bearing = calculate_initial_compass_bearing(currentNode.getTuplesCoordinate(),
                                                    neighborCurrent.getTuplesCoordinate())
        labelBearing = convertDegreeToLabel(bearing, nquadrant)

        if labelBearing == labelIndication:
            listNodeSameDirection.append(listNeighbors[i])

    if (len(listNodeSameDirection) > 1):
        # ho più possibili nodi in cui andare, scelgo random
        nodeChoose = random.randint(0, len(listNodeSameDirection) - 1)

        nodeToVisit = listNodeSameDirection[nodeChoose]

    elif (len(listNodeSameDirection) == 1):
        nodeToVisit = listNodeSameDirection[0]

    return nodeToVisit