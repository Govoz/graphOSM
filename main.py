#!/usr/bin/python
from csvUtils import *
from graph import *

# per comodità setto già il file
pathFile = 'example.csv'
# #pathFile = sys.argv[1]

csv = importCsv(pathFile)

listIndication = getAzimuth(csv)
gpsStart = getGpsStart(csv)
gpsStop = getGpsStop(csv)
rootNode = reverseGeocoding(gpsStart)

#rootNode = 945250651
print(rootNode)
manageGraph(gpsStart, rootNode, 1000, listIndication, gpsStop)

#TODO: usare xmlDict per convertire l'xml in dict