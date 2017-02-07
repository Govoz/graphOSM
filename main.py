#!/usr/bin/python
from csvUtils import *
from graph import *
from Road import *


pathFile = 'example.csv'
radius = 1000

csv = importCsv(pathFile)

listIndication = getAzimuth(csv)
gpsStart = getGpsStart(csv)
gpsStop = getGpsStop(csv)

rootNodeId = reverseGeocoding(gpsStart)
getOSMfile(rootNodeId, radius)

manageGraph(gpsStart, rootNodeId, radius, listIndication, gpsStop)

