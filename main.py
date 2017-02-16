#!/usr/bin/python
from csvUtils import *
from graph import *
from visitGraph import *
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir('csvFile') if isfile(join('csvFile', f))]


# pathFile = 'csvFile/example.csv'
# pathFile = 'csvFile/Sensor_record_20170214_091000_AndroSensor.csv'
#pathFile = 'csvFile/' + onlyfiles[i]
print("**************")
pathFile = 'csvFile/Sensor_record_20170214_173326_AndroSensor.csv'
print(pathFile)

# esporto tutto con raggio 2000m, non cambiare
radius = 2000
windowsTime = 10
nQuadrants = 2

csv = importCsv(pathFile)

listIndication = getAzimuth(csv, windowsTime, nQuadrants)
print(len(listIndication))
print(listIndication)

gpsStart = getGpsStart(csv)
gpsStop = getGpsStop(csv)
print(gpsStart)
print(gpsStop)

nodeToCreateSoupFile = reverseGeocoding(gpsStart, 100)
print("nodeToCreateSoupFile: " + str(nodeToCreateSoupFile))

soup = getOSMfile(nodeToCreateSoupFile, radius)
# osmfilter.exe osmFile\test\353755078_2000.osm --parameter-file=my_parameters --drop-relations > osmFile\test\353755078_2000osmfilter.osm


# ora cerco il nodo da cui far cominciare il grafo
rootNodeId = reverseGeocodingGraph(gpsStart, 200, soup)
print("RootNodeId: " + str(rootNodeId))


# calculate = algorithmDeadReckoning(gpsStart, listIndication, 50)
# print(getDistance(calculate['latitude'], calculate['longitude'], gpsStop['latitude'], gpsStop['longitude']))


manageGraph(gpsStart, rootNodeId, radius, listIndication, gpsStop, soup, nQuadrants)

