#!/usr/bin/python
from csvUtils import *
from graph import *

pathFile = 'csvFile/example.csv'
radius = 1000

csv = importCsv(pathFile)

listIndication = getAzimuth(csv)
gpsStart = getGpsStart(csv)
gpsStop = getGpsStop(csv)

rootNodeId = reverseGeocoding(gpsStart, 50)

soup = getOSMfile(rootNodeId, radius)

manageGraph(gpsStart, rootNodeId, radius, listIndication, gpsStop, soup)

