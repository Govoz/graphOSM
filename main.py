#!/usr/bin/python
from csvUtils import *
from graph import *
from visitGraph import *
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir('csvFile') if isfile(join('csvFile', f))]

#pathFile = 'csvFile/' + onlyfiles[i]

print("**************")
pathFile = 'csvFile/Sensor_record_20170129_094650_AndroSensor.csv'
print(pathFile)

# esporto tutto con raggio 2000m, non cambiare
radius = 2000
windowsTime = 30
nQuadrants = 2

# 0  backtrack, 1  bestDecision, 2 randomDecision, 3 deadReckoning
algorithm = 1

csv = importCsv(pathFile)

listIndication = getAzimuth(csv, windowsTime, nQuadrants)

gpsStart = getGpsStart(csv)
gpsStop = getGpsStop(csv)
print(gpsStart)
print(gpsStop)

#ottengo un nodo generico da cui creare il .osm
nodeToCreateSoupFile = reverseGeocoding(gpsStart, 100)
print("nodeToCreateSoupFile: " + str(nodeToCreateSoupFile))

soup = getOSMfile(nodeToCreateSoupFile, radius)
# osmfilter.exe osmFile\test\353755078_2000.osm --parameter-file=my_parameters --drop-relations > osmFile\test\353755078_2000osmfilter.osm


# ora cerco il nodo da cui far cominciare il grafo, deve appartenere ad una strada.
rootNodeId = reverseGeocodingGraph(gpsStart, 200, soup)
print("RootNodeId: " + str(rootNodeId))


manageGraph(gpsStart, rootNodeId, radius, listIndication, gpsStop, soup, nQuadrants, algorithm)

