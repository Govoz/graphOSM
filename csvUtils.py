#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from osmUtils import *
import time
import datetime

#includedColumn = [30, 16, 22, 23] #30 is time, 16 is azimuth, 22 is latitude, 23 is longitude (Bedo)
includedColumn = [17, 6, 9, 10]  #(Govo)


# importCSV restituisce una lista di obj composti da [time, azimuth]
def importCsv(pathFile):
    listData = []
    with open(pathFile, 'rt') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            content = list(row[i] for i in includedColumn)
            listData.append(content)

    print("CSV importato")

    return listData


def getGpsStart(csv):
    latitude = csv[1][2]
    longitude = csv[1][3]
    obj = {'latitude': latitude,
           'longitude': longitude}

    print("Il punto iniziale è: " + str(latitude) + "," + str(longitude))
    return obj

def getGpsStop(csv):
    latitude = csv[len(csv) - 1][2]
    longitude = csv[len(csv) - 1][3]
    obj = {'latitude': latitude,
           'longitude': longitude}

    print("Il punto finale è: " + str(latitude) + "," + str(longitude))
    return obj

def getAzimuth(csv, windowsTime, nquadrant):

    list = []
    for line in range(1, len(csv)):
        value = csv[line][1]
        time = csv[line][0]
        obj = {'value': value, 'time': time}
        list.append(obj)

    # in secondi
    lastWindowsTime = float(list[-1]['time']) % (float(windowsTime) * 1000) / 1000

    #filtro per finestra temporale e faccio la media
    listFiltered = []
    listCurrent = []
    limit = int(list[0]['time']) + (int(windowsTime) * 1000)

    for line in range(len(list)):
        valueTime = int(list[line]['time'])

        if valueTime < limit:
            listCurrent.append(float(list[line]['value']))
        else:
            listFiltered.append(listCurrent[:])
            del listCurrent[:]
            limit = valueTime + (int(windowsTime) * 1000)
            listCurrent.append(float(list[line]['value']))

    listFiltered.append(listCurrent[:])

    #listFiltered è una lista di liste, ogni sottolista appartiene ad una finestra temporale
    listAverageValue = []
    for list in range(len(listFiltered)):
        sum = 0
        for value in listFiltered[list]:
            sum += float(value)
        average = sum / len(listFiltered[list])

        listAverageValue.append(average)

    #listAveragueValue contiene le direzioni medie misurate in una finestra temporale
    listDirection = []

    for element in range(len(listAverageValue)):
        value = float(listAverageValue[element])
        quadrant = convertDegreeToLabel(value, nquadrant)

        obj = {'value': value, 'direction': quadrant, 'time': windowsTime}

        listDirection.append(obj)

    # l'ultimo elemento avrà una durata inferiore alla windowsTime
    listDirection[-1]['time'] = lastWindowsTime

    # listIndication la uso come stack, quindi inverto l'ordine degli elementi in quanto pop e push dal fondo
    #listDirection.reverse()

    print("ListIndication generate")
    return listDirection


def writeResultOnTxt(pathFile, nQuadrants, windowsTime, algorithm, speedLimit, distance):

    nameFile = pathFile.replace("csvFile/","")
    text_file = open("output\output.csv", "a")
    stringAlgorithm = ''

    if algorithm == 0:
        stringAlgorithm = 'Backtrack'
        distance = str(distance['distanceNode']) + ',' + str(distance['distanceMin'])
    elif algorithm == 1:
        stringAlgorithm = 'BestDecision'
    elif algorithm == 2:
        stringAlgorithm = 'RandomDecision'
    elif algorithm == 3:
        stringAlgorithm = 'DeadReckoning'

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    string = st + "," + str(nameFile) + "," + str(nQuadrants) + "," + str(windowsTime) + "," + str(speedLimit) + "," + str(stringAlgorithm) + "," + str(distance)

    text_file.write(string + "\n")
    text_file.close()
    print("Scrittura eseguita con successo")


