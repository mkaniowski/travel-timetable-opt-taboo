import os
import json
import numpy as np
import geopy.distance

from city import City
from randTimetable import randTimetable


class Optimize:
    def __init__(self):
        self.cities = []
        self.names = []
        self.dists = None

    def addCity(self, city):
        self.cities.append(City(city['city'], city['lat'], city['lon']))
        self.names.append(city['city'])

    def calculateDist(self):
        self.dists = np.zeros((len(self.cities), len(self.cities)))

        for row in range(len(self.dists)):
            for col in range(len(self.dists)):
                if (row == col):
                    self.dists[row, col] = np.inf
                    continue

                lon1 = self.cities[row].lon
                lon2 = self.cities[col].lon
                lat1 = self.cities[row].lat
                lat2 = self.cities[col].lat

                c1 = (lat1, lon1)
                c2 = (lat2, lon2)
                self.dists[row][col] = geopy.distance.geodesic(c1, c2).km

    def fitness(self):
        return None


def main():
    with open(f'{os.getcwd()}/src/data/cities.json', 'r') as f:
        data = json.load(f)

    opt = Optimize()

    for i in data:
        opt.addCity(i)

    opt.calculateDist()

    randTimetable()


main()
