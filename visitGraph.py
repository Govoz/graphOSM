import random

from osmUtils import *

global listNodeVisitedGraph
listNodeVisitedGraph = []
global listNodeBacktrack
listNodeBacktrack = []

def visitGraphBackTrack(G, idRoot, listIndication, soup, nquadrant):

    # print("Nodo corrente: " + str(idRoot))
    print(listIndication)
    obj = {'node': idRoot, 'indicationLen': len(listIndication)}
    listNodeBacktrack.append(obj)

    # evito di estrarre un elemento da una lista vuota
    if len(listIndication) > 0 and (G.has_node(str(idRoot))):

        listNodeVisitedGraph.append(str(idRoot))

        indication = listIndication.pop()
        indicationDirection = indication['direction']

        # print("Indicazione")
        # print(indicationDirection)

        # ottengo la lista di vicini
        listNeighbors = G.neighbors(str(idRoot))
        if (len(listNeighbors) > 0):
            # print("Lista Vicini:")
            # print(listNeighbors)

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

                    # print("Il current per arrivare a Neighboor deve andare a " + str(labelDirectionElement))

                    if (str(labelDirectionElement) is str((indicationDirection))):
                        # print("Stessa Direzione -> Analizzo")

                        lastNodeVisitedGraphBackTrack = str(idRoot)
                        print(lastNodeVisitedGraphBackTrack)

                        road = Road(getCommonWay(idRoot, listNeighbors[element], soup), soup)
                        # print("La strada è : ")
                        # print(road)

                        speedLimit = float(road.speedLimit)
                        #speedLimit = 20

                        time = float(indication['time'])
                        meterXsec = float(speedLimit / 3.6)
                        # meter sono i metri fatti nella finestra temporale in indicationDirection
                        meterWindows = meterXsec * time

                        # print("Nella windows ho percorso: " + str(meterWindows))

                        # mi calcolo la distanza tra i due nodi
                        distance = getDistance(currentNode.lat, currentNode.lon, neighNode.lat, neighNode.lon)
                        # print("Tra i due nodi la distanza è : " + str(distance))

                        # se i metri nella windows sono maggiori rispetto a quelli consumati, mi calcolo i rimanenti e riappendo alla lista delle indicazioni
                        if meterWindows > distance:
                            meterRemaining = meterWindows - distance
                            # converto i metri in secondi tenendo conto dello speedLimit
                            timeRemaining = meterRemaining / meterXsec

                            obj = {'value': indication['value'], 'direction': labelDirectionElement,
                                   'time': timeRemaining}
                            listIndication.append(obj)

                        visitGraphBackTrack(G, listNeighbors[element], listIndication, soup, nquadrant)

                    else:
                        print("Direzione Errata -> Ignoro")
                        print(labelDirectionElement)
                        listIndication.append(indication)


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

def visitGraphBackTrackIterative(G, idRoot, listIndication, soup, nquadrant):
    listIndication = listIndication[:]
    stack = []
    listNodeVisited = set()
    objToAppendStack = {'node': idRoot, 'listIndication':listIndication}
    stack.append(objToAppendStack)
    lastNodeVisitedGraphBackTrack = None

    while(len(stack) > 0):
        print("******************************")
        objStack = stack.pop()
        currentNode = objStack['node']
        listIndicationStack = objStack['listIndication']
        print(listIndicationStack)

        print("Nodo corrente: " + str(currentNode))

        if currentNode in listNodeVisited:
            continue

        listNodeVisited.add(currentNode)

        #---------------------
        if len(listIndicationStack) > 0 and (G.has_node(str(currentNode))):
            indication = listIndicationStack.pop()

            indicationDirection = indication['direction']

            print("Indicazione")
            print(indicationDirection)

            # ottengo la lista di vicini
            listNeighbors = G.neighbors(str(currentNode))
            if (len(listNeighbors) > 0):
                print("Lista Vicini:")
                print(listNeighbors)

                nodeObj = Intersection(currentNode, soup)
                coordinateCurrentNode = (float(nodeObj.lat), float(nodeObj.lon))

                # per ogni vicino mi cerco la strada che la collega e mi ricavo il limite di velocità
                for element in range(len(listNeighbors)):
                    # se l'elemento non è stato già visitato
                    if not (str(listNeighbors[element]) in listNodeVisited):

                        # ottengo l'obj del neighbors
                        neighNode = Intersection(listNeighbors[element], soup)

                        # per ogni vicino guardo se è nella stessa direzione dell'indicazione
                        coordinateElement = (float(neighNode.lat), float(neighNode.lon))
                        directionElement = calculate_initial_compass_bearing(coordinateCurrentNode, coordinateElement)
                        labelDirectionElement = convertDegreeToLabel(directionElement, nquadrant)

                        print("Il current per arrivare a Neighboor deve andare a " + str(labelDirectionElement))

                        if (str(labelDirectionElement) is str((indicationDirection))):
                            print("Stessa Direzione -> Analizzo")

                            lastNodeVisitedGraphBackTrack = str(currentNode)
                            road = Road(getCommonWay(currentNode, listNeighbors[element], soup), soup)
                            print("La strada è : ")
                            print(road)

                            speedLimit = float(road.speedLimit)
                            # speedLimit = 20

                            time = float(indication['time'])
                            meterXsec = float(speedLimit / 3.6)
                            # meter sono i metri fatti nella finestra temporale in indicationDirection
                            meterWindows = meterXsec * time

                            print("Nella windows ho percorso: " + str(meterWindows))

                            # mi calcolo la distanza tra i due nodi
                            distance = getDistance(nodeObj.lat, nodeObj.lon, neighNode.lat, neighNode.lon)
                            print("Tra i due nodi la distanza è : " + str(distance))

                            # se i metri nella windows sono maggiori rispetto a quelli consumati, mi calcolo i rimanenti e riappendo alla lista delle indicazioni
                            if meterWindows > distance:
                                meterRemaining = meterWindows - distance
                                # converto i metri in secondi tenendo conto dello speedLimit
                                timeRemaining = meterRemaining / meterXsec

                                obj = {'value': indication['value'], 'direction': labelDirectionElement,
                                       'time': timeRemaining}
                                listIndicationStack.append(obj)

                            stackObj = {'node': str(listNeighbors[element]), 'listIndication': listIndicationStack}
                            stack.append(stackObj)

    return lastNodeVisitedGraphBackTrack




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

        if str(labelBearing) == str(labelIndication):
            listNodeSameDirection.append(listNeighbors[i])

    print(listNodeSameDirection)
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
        if (G.has_node(str(idCurrentNode))):

            print("CurrentNode: " + str(idCurrentNode))

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
                    listIndication.append(obj['direction'])

                #TODO: probabile bug quando i metri da consumare sono più di quelli della finestra temporale

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
