#!/usr/bin/python
from csvUtils import *
from graph import *
from Road import *
from Intersection import Intersection

# per comodità setto già il file
# pathFile = 'example.csv'
# #pathFile = sys.argv[1]
#
# csv = importCsv(pathFile)
#
#gpsStart = getGpsStart(csv)
#rootWay = reverseGeocoding(gpsStart)

gpsStart = {'latitude': 44.6597209, 'longitude': 11.1419101}

rootNode = 531295041

#passo a create graph, il punto gps iniziale, l'ID del nodo da cui partire a creare e la distanza massima tra un qualunque nodo dal nodo root
#createGraph(gpsStart, rootNode, 1000)

getOrientamentWay(32336792)
