#!/usr/bin/python
from csvUtils import *
from graph import *

# per comodità setto già il file
pathFile = 'example.csv'
# #pathFile = sys.argv[1]
#
csv = importCsv(pathFile)
#
listIndication = getAzimuth(csv)
gpsStart = getGpsStart(csv)
rootNode = reverseGeocoding(gpsStart)

manageGraph(gpsStart, rootNode, 1000, listIndication)
