import math
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
    def addCity(self, city, timeSpent, desire):
        self.cities.append(
            City(city['city'], city['lat'], city['lon'], timeSpent, desire))
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

    # calculate cost of the solution
    def getCost(self, sol):
        # sol -> [(type, city), (type, city), ...], where t is the time spent in city type (0, 1, 2) is the type of transport
        out = 0
        for i in range(len(sol)-1):
            if i == 0:
                continue
            travelTime = self.dists[sol[i-1][1]][sol[i]
                                                 [1]]/self.vehicles[sol[i][0]].vel
            res = math.ceil(travelTime) - travelTime
            out += travelTime*self.vehicles[sol[i][0]].cost*(1/self.cities[sol[i][1]].desire) + self.cities[sol[i][1]].timeSpent + res
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
        opt.addCity(i, np.random.randint(low=2, high=13),
                    np.random.randint(low=1, high=11))

    opt.calculateDist()

    randTimetable()

    opt.loadTimetable()

    ex = [(0, 0), (0, 2), (0, 5),
          (2, 3), (2, 10), (1, 1)]

    print(opt.getCost(ex))


main()
