import csv

includedColumn = [30, 16, 22, 23] #30 is time, 16 is azimuth, 22 is latitude, 23 is longitude

# importCSV restituisce una lista di obj composti da [time, azimuth]
def importCsv(pathFile):
    listData = []
    with open(pathFile, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            content = list(row[i] for i in includedColumn)
            listData.append(content)

    return listData


def getGpsStart(csv):
    latitude = csv[1][2]
    longitude = csv[1][3]
    obj = {'latitude': latitude,
           'longitude': longitude}
    return obj