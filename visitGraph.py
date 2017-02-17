import random

from osmUtils import *

global listNodeVisitedGraph
listNodeVisitedGraph = []

global listNodeBacktrack
listNodeBacktrack = []

def visitGraphBackTrack(G, idRoot, listIndication, soup, nquadrant):

    # listNodeBacktrack mi serve per ricavare il nodo che ha consumato più indicazioni
    obj = {'node': idRoot, 'indicationLen': len(listIndication)}
    listNodeBacktrack.append(obj)

    # controllo se ho già consumato tutte le indicazioni e se il grafo ha quel determinato nodo
    if len(listIndication) > 0 and (G.has_node(str(idRoot))):

        # aggiungo il nodo alla lista dei nodi visitati
        listNodeVisitedGraph.append(str(idRoot))

        # mi ricavo l'indicazione da consumare
        indication = listIndication.pop()
        indicationDirection = indication['direction']

        # ottengo la lista di vicini
        listNeighbors = G.neighbors(str(idRoot))

        # se ha almeno un vicino
        if (len(listNeighbors) > 0):

            currentNode = Intersection(idRoot, soup)
            coordinateCurrentNode = (float(currentNode.lat), float(currentNode.lon))

            # per ogni vicino mi cerco la strada che la collega e mi ricavo il limite di velocità
            for element in range(len(listNeighbors)):

                # se l'elemento non è stato già visitato
                if not (str(listNeighbors[element]) in listNodeVisitedGraph):

                    # ottengo l'obj del neighbors
                    neighNode = Intersection(listNeighbors[element], soup)

                    # per ogni vicino guardo se è nella stessa direzione dell'indicazione
                    coordinateElement = (float(neighNode.lat), float(neighNode.lon))
                    directionElement = calculate_initial_compass_bearing(coordinateCurrentNode, coordinateElement)
                    labelDirectionElement = convertDegreeToLabel(directionElement, nquadrant)

                    # se il nodo che analizzo e il vicino sono nella stessa direzione, analizzo il vicino
                    if (str(labelDirectionElement) is str((indicationDirection))):

                        road = Road(getCommonWay(idRoot, listNeighbors[element], soup), soup)

                        speedLimit = float(road.speedLimit)

                        time = float(indication['time'])
                        meterXsec = float(speedLimit / 3.6)
                        # meter sono i metri fatti nella finestra temporale in indicationDirection
                        meterWindows = meterXsec * time

                        # mi calcolo la distanza tra i due nodi
                        distance = getDistance(currentNode.lat, currentNode.lon, neighNode.lat, neighNode.lon)

                        # se i metri nella windows sono maggiori rispetto a quelli consumati, mi calcolo i rimanenti e riappendo alla lista delle indicazioni
                        if meterWindows > distance:
                            meterRemaining = meterWindows - distance
                            # converto i metri in secondi tenendo conto dello speedLimit
                            timeRemaining = meterRemaining / meterXsec

                            obj = {'value': indication['value'], 'direction': labelDirectionElement,
                                   'time': timeRemaining}
                            listIndication.append(obj)

                        # TODO: gestire il fatto che mi possano servire più finestre per andare dal nodo corrente al vicino

                        visitGraphBackTrack(G, listNeighbors[element], listIndication, soup, nquadrant)

                    else:
                        print("Direzione Errata -> Ignoro")
                        print(labelDirectionElement)
                        listIndication.append(indication)


#data una lista di obj: id e indicationLen ottengo l'obj con il numero minore di indicationLen
def getMinListIndication(list):
    obj = list[0]
    nodeMin = obj['node']
    indicationLenMin = int(obj['indicationLen'])

    for i in range(len(list)):
        objTemp = list[i]
        node = objTemp['node']
        indicationLen = int(objTemp['indicationLen'])

        if indicationLen < indicationLenMin:
            indicationLenMin = indicationLen
            nodeMin = node

    return nodeMin


# dato un nodo corrente e una lista di nodi da visitare, restituisce il nodo che rispecchia l'indicazione
# se ce ne sono di più mi restituisce il più vicino
def decisionNeighbors(idCurrentNode, listNeighbors, indicationCurrent, soup, nquadrants):

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

        if str(labelBearing) == str(labelIndication):
            listNodeSameDirection.append(listNeighbors[i])

    # se ho più nodi da poter visitare restituisco il più vicino.
    if (len(listNodeSameDirection) > 1):
        nodeToVisit = getNearestNodeVisit(listNodeSameDirection, idCurrentNode, soup)
        print("NodeToVisit")
        print(nodeToVisit)
    elif (len(listNodeSameDirection) == 1):
        nodeToVisit = listNodeSameDirection[0]

    return nodeToVisit


def visitGraphBestDecision(G, idCurrentNode, listIndication, soup, nquadrant):
    lastBestNeighborsID = None

    print(listIndication)

    # smetto di iterare quando ho finito le indicazioni da consumare
    while (len(listIndication) > 0):

        print(listIndication)

        # se il grafo contiene questo nodo allora vuol dire che mi trovo in un nodo valido
        if (G.has_node(str())):

            # print("CurrentNode: " + str(idCurrentNode))

            # ottengo l'indicazione corrente e il nodo da cui parto a consumarla
            indicationCurrent = listIndication.pop()
            currentNode = Intersection(idCurrentNode, soup)

            # indico che il nodo che sto esaminando è stato visitato
            listNodeVisitedGraph.append(idCurrentNode)

            # ottengo la lista dei vicini
            listNeighborsNotFiltered = (G.neighbors(str(idCurrentNode)))
            listNeighbors = [x for x in listNeighborsNotFiltered if x not in listNodeVisitedGraph]
            bestNeighborsID = decisionNeighbors(idCurrentNode, listNeighbors, indicationCurrent, soup, nquadrant)

            if (bestNeighborsID != None):
                bestNeighborsNode = Intersection(bestNeighborsID, soup)

                print("------------")
                print("BestChoise: " + str(bestNeighborsID))
                print("------------")

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

                #TODO: probabile bug quando i metri da consumare sono più di quelli della finestra temporale
                # if distance > meterWindows:
                #     meterRemaining = distance - meterWindows
                #     timeRemaining = meterRemaining / meterXsec
                #
                #     nextIndication = listIndication.pop()
                #     if indicationCurrent['direction'] == nextIndication['direction']:
                #         timeNext = float(nextIndication['time'])
                #         obj = {'value': indicationCurrent['value'], 'direction': indicationCurrent['direction'],
                #                'time': timeRemaining + timeNext}
                #         listIndication.append(obj)
                #     else:
                #         listIndication.append(nextIndication)

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

        # se il grafo contiene questo nodo allora vuol dire che mi trovo in un nodo valido
        if (G.has_node(str(idCurrentNode))):
            # print("CurrentNode: " + str(idCurrentNode))

            # ottengo l'indicazione corrente e il nodo da cui parto a consumarla
            indicationCurrent = listIndication.pop()
            currentNode = Intersection(idCurrentNode, soup)

            # indico che il nodo che sto esaminando è stato visitato
            listNodeVisitedGraph.append(idCurrentNode)

            # ottengo la lista dei vicini
            listNeighbors = (G.neighbors(str(idCurrentNode)))
            NextNeighborsID = randomDecision(idCurrentNode, listNeighbors, indicationCurrent, soup, nquadrant)

            if (NextNeighborsID != None):
                bestNeighborsNode = Intersection(NextNeighborsID, soup)

                # print("RandomChoise: " + str(NextNeighborsID))

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
                #print("Nessuna scelta possibile")
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


# faccio i calcoli e ottengo delle coordinate. Ottengo il nodo più vicino a quelle coordinate. Controllo se ha una
# road Common Way assieme al nodeId

def getNewCoordinates(lat, lon, distance, direction):
    x1 = math.radians(float(lat))
    y1 = math.radians(float(lon))

    direction = math.radians(direction)

    R = 6378.1  # Radius of the Earth
    x2 = math.asin(math.sin(x1) * math.cos(distance / R) + math.cos(x1) * math.sin(distance / R) * math.cos(direction))
    y2 = y1 + math.atan2(math.sin(direction) * math.sin(distance / R) * math.cos(x1),
                         math.cos(distance / R) - math.sin(x1) * math.sin(x2))

    x2 = math.degrees(x2)
    y2 = math.degrees(y2)

    gps = {'latitude': x2,
           'longitude': y2}

    return gps


def algorithmDeadReckoning(coordinate, listIndication, speedLimit):
    listIndication.reverse()
    lat = coordinate['latitude']
    lon = coordinate['longitude']
    obj = {'latitude': float(lat),
           'longitude': float(lon)}
    newCoordinate = None

    while (len(listIndication) > 0):
        indicationCurrent = listIndication.pop()

        direction = float(indicationCurrent['value'])
        time = float(indicationCurrent['time'])
        meterXsec = float(speedLimit / 3.6)

        # metri percorsi
        meterConsumed = (meterXsec * time) / 1000
        #print(meterConsumed)

        newCoordinate = getNewCoordinates(lat, lon, meterConsumed, direction)
        #print(newCoordinate)
        lat = newCoordinate['latitude']
        lon = newCoordinate['longitude']

        coordinateFinal = str(lat) + " , " + str(lon)
        print(coordinateFinal)

    return newCoordinate
