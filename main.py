#!/usr/bin/python
from csvUtils import *
from graph import *

pathFile = 'csvFile/example.csv'
radius = 1000
windowsTime = 10
nQuadrants = 2

csv = importCsv(pathFile)

listIndication = getAzimuth(csv, windowsTime, nQuadrants)
gpsStart = getGpsStart(csv)
gpsStop = getGpsStop(csv)

rootNodeId = reverseGeocoding(gpsStart, 50)

soup = getOSMfile(rootNodeId, radius)

manageGraph(gpsStart, rootNodeId, radius, listIndication, gpsStop, soup, nQuadrants)

