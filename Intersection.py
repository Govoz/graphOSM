import lxml
from bs4 import BeautifulSoup

global soup

soup = BeautifulSoup(open('map.osm'), 'xml')

class Intersection:
    def __init__(self, id):
        self.id = id
        self.lat = 0
        self.lon = 0

        allNode = soup.find_all('node')
        for i in range(len(allNode)):
            idNode = allNode[i].attrs['id']
            if idNode == str(id):
                self.lon = allNode[i].attrs['lon']
                self.lat = allNode[i].attrs['lat']

    def __str__(self):
        string = str(self.id) + " - " + str(self.lat) + " - " + str(self.lon)
        return string
