#!/usr/bin/python
from csvUtils import *
from graph import *
from Road import *
from Intersection import Intersection

# per comodità setto già il file
pathFile = 'example.csv'
# #pathFile = sys.argv[1]
#
csv = importCsv(pathFile)
#
# listIndication = getAzimuth(csv)
nameGraph = '945250651.graph'

gpsStart = getGpsStart(csv)
rootNode = reverseGeocoding(gpsStart)

#passo a create graph, il punto gps iniziale, l'ID del nodo da cui partire a creare e la distanza massima tra un qualunque nodo dal nodo root
manageGraph(gpsStart, rootNode, 100, nameGraph)
