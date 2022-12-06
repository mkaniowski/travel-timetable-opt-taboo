import os
import json
import numpy as np
import geopy.distance

from city import City
from vehicle import Vehicle
from randTimetable import randTimetable


class Optimize:
    def __init__(self):
        self.cities = []
        self.names = []
        self.dists = None
        self.vehicles = []

    # add city object to the list of cities
    def addCity(self, city):
        self.cities.append(City(city['city'], city['lat'], city['lon']))
        self.names.append(city['city'])

    def addVehicle(self, vehicle):
        self.vehicles.append(vehicle)

    # calcualte distance bewteen 2 cities and put it in matrix
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

    # load timetables to city objects
    def loadTimetable(self):
        with open(f'{os.getcwd()}/src/data/timetable.json', 'r') as f:
            data = json.load(f)
        for i in range(len(self.cities)):
            self.cities[i].addTimetable(data[i]['timetable'])

    # calculate fitness of the solution
    def fitness(self, sol):
        # sol -> [(t, type, city, additionalTime), (t, type, city, additionalTime), ...], where t is the time spent for transport (full hours) to city and type (0, 1, 2) is the type of transport. Additional time is time needed to full hour + time spent in city
        out = 0
        for i in range(len(sol)-1):
            if i == 0:
                continue
            deltaTime = sol[i-1][0] - sol[i][0]
            out += deltaTime*self.vehicles[sol[i][1]].cost + sol[i][3]
        return out


def main():
    opt = Optimize()
    opt.addVehicle(Vehicle('bus', 100, 1))
    opt.addVehicle(Vehicle('train', 160, 1.2))
    opt.addVehicle(Vehicle('plane', 800, 2.5))

    # [bus, train, plane] order in timetable

    # adding cities to object
    with open(f'{os.getcwd()}/src/data/cities.json', 'r') as f:
        data = json.load(f)

    for i in data:
        opt.addCity(i)

    opt.calculateDist()

    randTimetable()

    opt.loadTimetable()

    ex = [(0, 0, 'warsaw', 0), (5, 0, 'berlin', 4), (4, 0, 'prague', 5),
          (2, 2, 'rome', 4), (2, 2, 'paris', 4), (4, 1, 'amsterdam', 3)]

    print(opt.fitness(ex))


main()
