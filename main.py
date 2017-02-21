# !/usr/bin/env python  # -*- coding: utf-8 -*-

import sys
from csvUtils import *
from graph import *
from visitGraph import *
from osmUtils import *

# osmfilter.exe osmFile\test\353755078_2000.osm --parameter-file=my_parameters --drop-relations > osmFile\test\353755078_2000osmfilter.osm

# esporto tutto con raggio 2000m, non cambiare
radius = 2000
# windowsTime = 10
# nQuadrants = 2
# # 0  backtrack, 1  bestDecision, 2 randomDecision, 3 deadReckoning
# algorithm = 2
# speedLimit = 50

nQuadrantsRange = [2, 4, 8]
windowsTimeRange = [20, 10, 5, 1]
algorithmRange = [0, 1, 2, 3]
speedLimitRange = [30, 50, 70, 90]


pathFile = 'csvFile/Sensor_record_20170129_102209_AndroSensor.csv'

# windowsTime = 10
# nQuadrants = 2
# algorithm = 1
# speedLimit = 0

csv = importCsv(pathFile)
gpsStart = getGpsStart(csv)
gpsStop = getGpsStop(csv)

distanceStartStop = getDistance(gpsStart['latitude'], gpsStart['longitude'], gpsStop['latitude'], gpsStop['longitude'])

# ottengo un nodo generico da cui creare il .osm
nodeToCreateSoupFile = reverseGeocoding(gpsStart, 100)
soup = getOSMfile(nodeToCreateSoupFile, radius)
# ora cerco il nodo da cui far cominciare il grafo, deve appartenere ad una strada.
rootNodeId = reverseGeocodingGraph(gpsStart, 200, soup)

i = 0

for alg in range(len(algorithmRange)):
    for quadrant in range(len(nQuadrantsRange)):
        for time in range(len(windowsTimeRange)):
            for speed in range(len(speedLimitRange)):

                windowsTime = windowsTimeRange[time]
                nQuadrants = nQuadrantsRange[quadrant]
                algorithm = algorithmRange[alg]
                speedLimit = speedLimitRange[speed]

                listIndication = getAzimuth(csv, windowsTime, nQuadrants)

                distance = manageGraph(gpsStart, rootNodeId, radius, listIndication, gpsStop, soup, nQuadrants, algorithm, speedLimit)
                print(distance)
                print(algorithm)
                writeResultOnTxt(pathFile, nQuadrants, windowsTime, algorithm, speedLimit, distance)
                i += 1
                print(str(i) + "/192")

# #
# windowsTime = 10
# nQuadrants = 2
# algorithm = 1
# listIndication = getAzimuth(csv, windowsTime, nQuadrants)
#
# distance = manageGraph(gpsStart, rootNodeId, radius, listIndication, gpsStop, soup, nQuadrants, algorithm, 50)