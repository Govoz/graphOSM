import csv
import matplotlib.pyplot as plt
import numpy as np

def importCsv():
    listData = []
    with open('output/output.csv', 'rt') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            content = list(row[i] for i in range(9))
            listData.append(content)

    print("CSV importato")
    return listData

#fisso quadranti e windowsTime, faccio un istogramma in cui valuto gli errori in percentuale per ogni alg per ogni file
def firstGraph(listData, quadrant, windowsTime):

    n_file = int(len(listData) / 192)

    listDataBacktrack = []
    listDataBestDecision = []
    listDataRandomDecision = []
    listDataDeadReckoning = []

    # Per ogni algoritmo mi costruisco una lista di valori, ogni valore corrisponde ad un file.
    for row in range(1, len(listData)):
        element = listData[row]
        if int(element[4]) == quadrant and int(element[5]) == windowsTime:
            if element[7] == 'Backtrack':
                listDataBacktrack.append(element)
            elif element[7] == 'BestDecision':
                listDataBestDecision.append(element)
            elif element[7] == 'RandomDecision':
                listDataRandomDecision.append(element)
            elif element[7] == 'DeadReckoning':
                listDataDeadReckoning.append(element)


    newListDataBacktrack = []
    index = 0
    while (index< len(listDataBacktrack)):
        minTemp = float(listDataBacktrack[index][3])
        minRow = listDataBacktrack[index]
        for i in range(index, index + 4):
            if float(listDataBacktrack[i][3]) < minTemp:
                minTemp = float(listDataBacktrack[i][3])
                minRow = listDataBacktrack[i]
        newListDataBacktrack.append(minRow)

        index = index + 4


    newListBestDecision = []
    index = 0
    while (index< len(listDataBestDecision)):
        minTemp = float(listDataBestDecision[index][3])
        minRow = listDataBestDecision[index]
        for i in range(index, index + 4):
            if float(listDataBestDecision[i][3]) < minTemp:
                minTemp = float(listDataBestDecision[i][3])
                minRow = listDataBestDecision[i]
        newListBestDecision.append(minRow)

        index = index + 4

    newListRandomDecision = []
    index = 0
    while (index< len(listDataRandomDecision)):
        minTemp = float(listDataRandomDecision[index][3])
        minRow = listDataRandomDecision[index]
        for i in range(index, index + 4):
            if float(listDataRandomDecision[i][3]) < minTemp:
                minTemp = float(listDataRandomDecision[i][3])
                minRow = listDataRandomDecision[i]
        newListRandomDecision.append(minRow)

        index = index + 4

    newListDeadReckoning = []
    index = 0
    while (index< len(listDataDeadReckoning)):
        minTemp = float(listDataDeadReckoning[index][3])
        minRow = listDataDeadReckoning[index]
        for i in range(index, index + 4):
            if float(listDataDeadReckoning[i][3]) < minTemp:
                minTemp = float(listDataDeadReckoning[i][3])
                minRow = listDataDeadReckoning[i]
        newListDeadReckoning.append(minRow)

        index = index + 4

    # ora ho tutte le row che mi interessano

    # ottengo la lista dei nomi dei file
    listNameFile = []
    for i in range(len(newListDataBacktrack)):
        listNameFile.append(newListDataBacktrack[i][1])

    # ottengo le tuple per ogni algoritmo
    listTuplesBacktrack = []
    for i in range(len(newListDataBacktrack)):
        listTuplesBacktrack.append(float(newListDataBacktrack[i][3]))
    backtrackValue = tuple(listTuplesBacktrack)


    listTuplesBestDecision = []
    for i in range(len(newListBestDecision)):
        listTuplesBestDecision.append(float(newListBestDecision[i][3]))
    bestDecisionValue = tuple(listTuplesBestDecision)

    listTuplesRandomDecision = []
    for i in range(len(newListRandomDecision)):
        listTuplesRandomDecision.append(float(newListRandomDecision[i][3]))
    randomDecisionValue = tuple(listTuplesRandomDecision)

    listTuplesDeadReckoning = []
    for i in range(len(newListDeadReckoning)):
        listTuplesDeadReckoning.append(float(newListDeadReckoning[i][3]))
    deadReckoningValue = tuple(listTuplesDeadReckoning)

    # print('Backtrack')
    # print(backtrackValue)
    # print('BestDecision')
    # print(bestDecisionValue)
    # print('RandomDecision')
    # print(randomDecisionValue)
    # print('DeadReckoning')
    # print(deadReckoningValue)

    fig, ax = plt.subplots()

    index = np.arange(n_file)
    bar_width = 0.2

    opacity = 0.8
    error_config = {'ecolor': '0.3'}

    rects1 = plt.bar(index, backtrackValue, bar_width,
                     alpha=opacity,
                     color='#025E9A',
                     error_kw=error_config,
                     label='BackTrack')

    rects2 = plt.bar(index + bar_width, bestDecisionValue, bar_width,
                     alpha=opacity,
                     color='#9a025e',
                     error_kw=error_config,
                     label='BestDecision')

    rects3 = plt.bar(index + bar_width + bar_width, randomDecisionValue, bar_width,
                     alpha=opacity,
                     color='#5e9a02',
                     error_kw=error_config,
                     label='RandomDecision')

    rects4 = plt.bar(index + bar_width + bar_width + bar_width, deadReckoningValue, bar_width,
                     alpha=opacity,
                     color='#9a3e02',
                     error_kw=error_config,
                     label='Dead Reckoning')

    plt.ylabel('e%')
    plt.title('Errore in rapporto alla distanza della traccia. Quadranti: ' + str(quadrant) + ', WindowsTime: ' + str(windowsTime))
    plt.xticks(index + (bar_width / 2) * 2  , ('File1', 'File2', 'File3', 'File4', 'File5', 'File6', 'File7', 'File8', 'File9', 'File10', 'File11', 'File12'))
    plt.legend()
    plt.gca().set_ylim([0,100])
    plt.tight_layout()
    plt.grid(True)
    plt.savefig('output/firstChart' + str(quadrant) + '-' + str(windowsTime) + '.png')
    #plt.show()

#fisso i quadranti e le windowsTime, sull'asse x gli algoritmi, sull'asse y gli errori
def secondGraph(listData, quadrant, windowsTime):
    n_file = int(len(listData) / 192)

    listDataBacktrack = []
    listDataBestDecision = []
    listDataRandomDecision = []
    listDataDeadReckoning = []

    # Per ogni algoritmo mi costruisco una lista di valori, ogni valore corrisponde ad un file.
    for row in range(1, len(listData)):
        element = listData[row]
        if int(element[4]) == quadrant and int(element[5]) == windowsTime:
            if element[7] == 'Backtrack':
                listDataBacktrack.append(element)
            elif element[7] == 'BestDecision':
                listDataBestDecision.append(element)
            elif element[7] == 'RandomDecision':
                listDataRandomDecision.append(element)
            elif element[7] == 'DeadReckoning':
                listDataDeadReckoning.append(element)

    newListDataBacktrack = []
    index = 0
    while (index < len(listDataBacktrack)):
        minTemp = float(listDataBacktrack[index][3])
        minRow = listDataBacktrack[index]
        for i in range(index, index + 4):
            if float(listDataBacktrack[i][3]) < minTemp:
                minTemp = float(listDataBacktrack[i][3])
                minRow = listDataBacktrack[i]
        newListDataBacktrack.append(minRow)

        index = index + 4

    newListBestDecision = []
    index = 0
    while (index < len(listDataBestDecision)):
        minTemp = float(listDataBestDecision[index][3])
        minRow = listDataBestDecision[index]
        for i in range(index, index + 4):
            if float(listDataBestDecision[i][3]) < minTemp:
                minTemp = float(listDataBestDecision[i][3])
                minRow = listDataBestDecision[i]
        newListBestDecision.append(minRow)

        index = index + 4

    newListRandomDecision = []
    index = 0
    while (index < len(listDataRandomDecision)):
        minTemp = float(listDataRandomDecision[index][3])
        minRow = listDataRandomDecision[index]
        for i in range(index, index + 4):
            if float(listDataRandomDecision[i][3]) < minTemp:
                minTemp = float(listDataRandomDecision[i][3])
                minRow = listDataRandomDecision[i]
        newListRandomDecision.append(minRow)

        index = index + 4

    newListDeadReckoning = []
    index = 0
    while (index < len(listDataDeadReckoning)):
        minTemp = float(listDataDeadReckoning[index][3])
        minRow = listDataDeadReckoning[index]
        for i in range(index, index + 4):
            if float(listDataDeadReckoning[i][3]) < minTemp:
                minTemp = float(listDataDeadReckoning[i][3])
                minRow = listDataDeadReckoning[i]
        newListDeadReckoning.append(minRow)

        index = index + 4

    # ora ho tutte le row che mi interessano

    # ottengo la lista dei nomi dei file
    listNameFile = []
    for i in range(len(newListDataBacktrack)):
        listNameFile.append(newListDataBacktrack[i][1])

    # ottengo le tuple per ogni algoritmo
    listTuplesBacktrack = []
    for i in range(len(newListDataBacktrack)):
        listTuplesBacktrack.append(float(newListDataBacktrack[i][3]))
    backtrackValue = tuple(listTuplesBacktrack)

    listTuplesBestDecision = []
    for i in range(len(newListBestDecision)):
        listTuplesBestDecision.append(float(newListBestDecision[i][3]))
    bestDecisionValue = tuple(listTuplesBestDecision)

    listTuplesRandomDecision = []
    for i in range(len(newListRandomDecision)):
        listTuplesRandomDecision.append(float(newListRandomDecision[i][3]))
    randomDecisionValue = tuple(listTuplesRandomDecision)

    listTuplesDeadReckoning = []
    for i in range(len(newListDeadReckoning)):
        listTuplesDeadReckoning.append(float(newListDeadReckoning[i][3]))
    deadReckoningValue = tuple(listTuplesDeadReckoning)

    print('Backtrack')
    print(backtrackValue)
    print('BestDecision')
    print(bestDecisionValue)
    print('RandomDecision')
    print(randomDecisionValue)
    print('DeadReckoning')
    print(deadReckoningValue)

    backtrackAverage = sum(backtrackValue)/ len(backtrackValue)
    bestDecisionAverage = sum(bestDecisionValue) / len(bestDecisionValue)
    randomDecisionAverage = sum(randomDecisionValue) / len(randomDecisionValue)
    deadReckoningAverage = sum(deadReckoningValue) / len(deadReckoningValue)

    listAverage = []
    listAverage.append(backtrackAverage)
    listAverage.append(bestDecisionAverage)
    listAverage.append(randomDecisionAverage)
    listAverage.append(deadReckoningAverage)

    fig, ax = plt.subplots()

    index = np.arange(4)
    bar_width = 0.8

    opacity = 0.8
    error_config = {'ecolor': '0.3'}

    rects1 = plt.bar(index, tuple(listAverage), bar_width,
                     alpha=opacity,
                     color='#025E9A',
                     error_kw=error_config
                     )

    plt.ylabel('e%')
    plt.title('Errore medio relativo ad ogni algoritmo. Quadranti: ' + str(quadrant) + ', WindowsTime: ' + str(
        windowsTime))
    plt.xticks(index, ('Backtrack', 'BestDecision', 'RandomDecision' , 'DeadReckoning'))
    plt.tight_layout()
    plt.gca().set_ylim([0, 100])
    plt.gca().yaxis.grid(True)
    plt.savefig('output/secondChart' + str(quadrant) + '-' + str(windowsTime) + '.png')
    #plt.show()

# fisso gli algoritmi e la windowsTime, sull'asse Y gli errori in metri, sull'asse X la distanza del percorso
# avrò una linea per ogni quadrante, quindi 4 linee
def thirdGraph(listData, algorithm, windowsTime):
    listDataAlgorithm = []
    for row in range(1, len(listData)):
        element = listData[row]
        if element[7] == str(algorithm) and element[5] == str(windowsTime):
            listDataAlgorithm.append(element)

    newListDataAlgorithm = []
    index = 0
    while (index < len(listDataAlgorithm)):
        minTemp = float(listDataAlgorithm[index][3])
        minRow = listDataAlgorithm[index]
        for i in range(index, index + 4):
            if float(listDataAlgorithm[i][3]) < minTemp:
                minTemp = float(listDataAlgorithm[i][3])
                minRow = listDataAlgorithm[i]
        newListDataAlgorithm.append(minRow)

        index = index + 4

    # ora aggrego gli errori per quadranti
    listTwoQuadrants = []
    listFourQuadrants = []
    listEightQuadrants = []
    for i in range(len(newListDataAlgorithm)):
        element = newListDataAlgorithm[i]
        if int(element[4]) == 2:
            listTwoQuadrants.append(element)
        elif int(element[4]) == 4:
            listFourQuadrants.append(element)
        elif int(element[4]) == 8:
            listEightQuadrants.append(element)

    # for i in range(len(listEightQuadrants)):
    #     print(listEightQuadrants[i])

    tupleErrorTwoQuadrants = []
    tupleDistanceTwoQuadrants = []
    for i in range(len(listTwoQuadrants)):
        tupleDistanceTwoQuadrants.append(listTwoQuadrants[i][2])
        tupleErrorTwoQuadrants.append(listTwoQuadrants[i][8])

    tupleErrorFourQuadrants = []
    tupleDistanceFourQuadrants = []
    for i in range(len(listFourQuadrants)):
        tupleDistanceFourQuadrants.append(listFourQuadrants[i][2])
        tupleErrorFourQuadrants.append(listFourQuadrants[i][8])

    tupleErrorEightQuadrants = []
    tupleDistanceEightQuadrants = []
    for i in range(len(listEightQuadrants)):
        tupleDistanceEightQuadrants.append(listEightQuadrants[i][2])
        tupleErrorEightQuadrants.append(listEightQuadrants[i][8])

    print(tupleDistanceTwoQuadrants)
    print(tupleErrorTwoQuadrants)
    #--------------------
    fig, ax = plt.subplots()

    #prima tutte le x e poi tutte le y
    ax.plot(tuple(tupleDistanceTwoQuadrants), tuple(tupleErrorTwoQuadrants), label = '2 quadr.')
    ax.plot(tuple(tupleDistanceFourQuadrants), tuple(tupleErrorFourQuadrants), label = '4 quadr.')
    ax.plot(tuple(tupleDistanceEightQuadrants), tuple(tupleErrorEightQuadrants),'-.', label = '8 quadr.')

    plt.ylabel('error meter')
    plt.xlabel('track meter')
    plt.title(str(algorithm) + ', WindowsTime: ' + str(windowsTime))
    plt.tight_layout()

    if str(algorithm) != 'DeadReckoning':
        plt.legend()

    plt.gca().set_xlim([450, 4500])
    plt.gca().set_ylim([0, 3000])

    plt.gca().yaxis.grid(True)
    plt.savefig('output/thirdChart' + str(algorithm) + '-' + str(windowsTime) + '.png')
    plt.show()

def fourGraph(listData, windowsTime):
    listDataAlgorithm = []

    fig, ax = plt.subplots()
    tupleDistance = ['450', '500', '550', '600', '750', '800', '1400', '1500', '3000', '3100', '3200', '4300']

    tupleErrorBacktrack = ['90.7315425348', '109.1977160895', '63.3658097656', '52.1916703737', '78.6214097379', '9.1013507054', '151.5211752288', '92.3764589123', '23.7132594758', '26.528958505', '158.5173099758', '25.0245732642']

    tupleErrorBestDecision = ['281.7181503534', '142.3756005013', '134.7335578788', '229.2108322158', '258.8628991327', '143.6713889754', '296.8816370321', '616.666556843', '548.8097028586', '397.2573905226', '1446.6819557786', '662.550017939']

    tupleErrorRandomDecision = ['292.4105961086', '230.2915928929', '185.6343553959', '70.7283389631', '641.1441453639', '389.9793796673', '480.2108776574', '501.5484886495', '757.6201536304', '401.2665738501', '2093.0454540616', '560.7486954416']

    tupleErrorDeadReckoning = ['135.2419234843', '73.2550928473', '62.4171063996', '286.4862688067', '285.2648802419', '597.6241403245', '129.4325231947', '174.5837898067', '856.9915226249', '507.8791121878', '262.4487209878', '914.2478697389']

    # prima tutte le x e poi tutte le y
    ax.plot(tuple(tupleDistance), tuple(tupleErrorBacktrack), label='Backtrack')
    ax.plot(tuple(tupleDistance), tuple(tupleErrorBestDecision), label='BestDecision')
    ax.plot(tuple(tupleDistance), tuple(tupleErrorRandomDecision), '-.', label='RandomDecision')
    ax.plot(tuple(tupleDistance), tuple(tupleErrorDeadReckoning), '-.', label='DeadReckoning')

    plt.ylabel('error meter')
    plt.xlabel('track meter')
    plt.title(str(algorithm) + ', WindowsTime: ' + str(windowsTime))
    plt.tight_layout()

    if str(algorithm) != 'DeadReckoning':
        plt.legend()

    plt.gca().set_xlim([450, 4500])
    plt.gca().set_ylim([0, 3000])

    plt.gca().yaxis.grid(True)
    plt.savefig('output/fourChart' + str(windowsTime) + '.png')
    # plt.show()


#----------------------------------------#
nQuadrantsRange = [2, 4, 8]
windowsTimeRange = [20, 10, 5, 1]
algorithm = ['Backtrack', 'BestDecision', 'RandomDecision', 'DeadReckoning']

listData = importCsv()

for x in range(len(windowsTimeRange)):
    # for i in range(len(nQuadrantsRange)):
        #firstGraph(listData, nQuadrantsRange[i], windowsTimeRange[x])
        #secondGraph(listData, nQuadrantsRange[i], windowsTimeRange[x])
    for w in range(len(algorithm)):
        thirdGraph(listData, algorithm[w], windowsTimeRange[x])
#
# thirdGraph(listData, algorithm[0], 20)
# thirdGraph(listData, algorithm[1], 20)
# thirdGraph(listData, algorithm[2], 20)
# thirdGraph(listData, algorithm[3], 20)
# fourGraph(listData, 20)