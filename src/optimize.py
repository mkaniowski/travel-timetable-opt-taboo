import math
import os
import json
import numpy as np
import geopy.distance

from city import City
from vehicle import Vehicle


class Optimize:
    def __init__(self):
        self.cities = []
        self.names = []
        self.dists = None
        self.vehicles = []

    # add city object to the list of cities
    def addCity(self, city):
        self.cities.append(
            City(city['city'], city['lat'], city['lon'], city['timeSpent'], city['desire']))
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
        # sol -> [(type, city, t), (type, city, t), ...], where t is additional time spent in city and type (0, 1, 2) is the type of transport
        out = 0
        for i in range(len(sol)-1):
            if i == 0:
                continue
            travelTime = self.dists[sol[i-1][1]][sol[i]
                                                 [1]]/self.vehicles[sol[i][0]].vel
            res = math.ceil(travelTime) - travelTime
            out += travelTime*self.vehicles[sol[i][0]].cost*(
                1/self.cities[sol[i][1]].desire) + self.cities[sol[i][1]].timeSpent + res
        return out

    def getInitSol(self, start, end, time):
        currTime = time
        visited = [start]
        curr = start
        sol = [[0, start, self.cities[start].timeSpent]]
        addTime = 0
        while True:
            for c in range(len(self.cities[curr].timetable[0][currTime])):
                if (c == curr) or (c in visited) or (c == end):
                    continue

                while 1 not in self.cities[curr].timetable[0][currTime][c]:
                    addTime += 1
                    currTime += 1

                for t in range(len(self.cities[curr].timetable[0][currTime][c])):
                    if self.cities[curr].timetable[0][currTime][c][t] == 1:
                        mov = [t, c, addTime + self.cities[curr].timeSpent]
                        sol.append(mov)
                        visited.append(c)
                        curr = c
                        addTime = 0
                        break
                break
            if len(sol) > len(self.cities[curr].timetable[0][currTime]) - 2:
                visited.append(end)

                while 1 not in self.cities[curr].timetable[0][currTime][end]:
                    addTime += 1
                    currTime += 1

                for t in range(len(self.cities[curr].timetable[0][currTime][end])):
                    if self.cities[curr].timetable[0][currTime][end][t] == 1:
                        mov = [t, end, addTime + self.cities[curr].timeSpent]
                        sol.append(mov)
                        visited.append(end)
                        curr = c
                        addTime = 0
                        break

                break
        return sol

    def getNeighborhood(self, sol):
        sol_=sol.copy()
        n1 = np.random.randint(low=1, high=len(sol_))
        n2 = np.random.randint(low=1, high=len(sol_))
        while n1 == n2:
            n2 = np.random.randint(low=1, high=len(sol_))

        sol_[n1], sol_[n2] = sol_[n2], sol_[n1]

        return sol_

    def correctNeighborhood(self, sol, time):
        sol__ = sol.copy()
        currTime = time
        for i in range(len(sol__)):
            sol__[i][2] = self.cities[sol__[i][1]].timeSpent

        for i in range(len(sol__)-1):
            if i == 0:
                continue
            addTime = 0
            while 1 not in self.cities[sol__[i][1]].timetable[0][currTime][sol__[i+1][1]]:
                addTime += 1
                currTime += 1
                if currTime > 23:
                    currTime = 0
            sol__[i][2] += addTime
            busCost = np.inf
            trainCost = np.inf
            planeCost = np.inf
            for l in range(3):
                if self.cities[sol__[i][1]].timetable[0][currTime][sol__[i+1][1]][l] == 1:
                    if l == 0:
                        travelTime = self.dists[sol__[i][1]
                                                ][sol__[i+1][1]]/self.vehicles[l].vel
                        busCost = travelTime * \
                            self.vehicles[sol__[i][0]].cost * \
                            (1/self.cities[sol__[i][1]].desire)
                    if l == 1:
                        travelTime = self.dists[sol__[i][1]
                                                ][sol__[i+1][1]]/self.vehicles[l].vel
                        trainCost = travelTime * \
                            self.vehicles[sol__[i][0]].cost * \
                            (1/self.cities[sol__[i][1]].desire)
                    if l == 2:
                        travelTime = self.dists[sol__[i][1]
                                                ][sol__[i+1][1]]/self.vehicles[l].vel
                        planeCost = travelTime * \
                            self.vehicles[sol__[i][0]].cost * \
                            (1/self.cities[sol__[i][1]].desire)

            bestVeh = np.argmin([busCost, trainCost, planeCost])
            sol__[i][0] = bestVeh

        return sol__

    def opt(self, startPoint: int, endPoint:int, time: int, maxCost: float, maxTabuLen: int, aspiration: int, Nmax: int):
        sol = self.getInitSol(startPoint, endPoint, time)
        bestSol = sol
        bestSolCost = self.getCost(bestSol)
        tabuList = [sol]
        it = 0
        it1 = 0
        it2 = 0
        noImprovement = 0
        costs = []
        while ((it <= Nmax) and (bestSolCost <= maxCost)):
            it += 1
            newSol = self.correctNeighborhood(self.getNeighborhood(sol), time)
            if tabuList.count(newSol) == 0: # if tabuList.count(newSol) == 0
                noImprovement += 1
                newSolCost = self.getCost(newSol)
                it1 +=1
                if newSolCost < bestSolCost:
                    noImprovement = 0
                    bestSol = newSol
                    bestSolCost = newSolCost
                    costs.append(bestSolCost)
                    it2 +=1
                tabuList.append(newSol)
                if len(tabuList) >= maxTabuLen:
                    tabuList.pop(0)

                # aspiration criteria
                if noImprovement >= aspiration:
                    aspiredSolCost = self.getCost(tabuList[0])
                    idx = 0
                    for i in range(len(tabuList)-2):
                        currCost = self.getCost(tabuList[i])
                        if (currCost < aspiredSolCost) and (tabuList[i] != bestSol) and (tabuList[i] != sol):
                            aspiredSolCost = currCost
                            idx = i
                        sol = tabuList[idx]
                        tabuList.pop(idx)
                else:
                    sol = newSol
        return self.getCost(bestSol), it, bestSol, costs, it1, it2


def main():
    opt = Optimize()
    opt.addVehicle(Vehicle('bus', 100, 1))
    opt.addVehicle(Vehicle('train', 160, 1.2))
    opt.addVehicle(Vehicle('plane', 800, 5))

    # [bus, train, plane] order in timetable

    # adding cities to object
    with open(f'{os.getcwd()}/src/data/cities.json', 'r') as f:
        data = json.load(f)

    for i in data:
        opt.addCity(i)

    with open(f'{os.getcwd()}/src/data/timetable.json', 'r') as f:
        data = json.load(f)

    for i in range(len(data)):
        opt.cities[i].addTimetable(data[i]["timetable"])

    opt.calculateDist()

    opt.loadTimetable()

    # ex = [(0, 0, 0), (0, 2, 1), (0, 5, 3),
    #       (2, 3, 2), (2, 10, 0), (1, 1, 0)]

    # print(opt.getCost(ex))
    # print(opt.cities[0].timetable[0][5])
    # print(opt.getInitSol(3, 10, 5))
    # s = opt.getInitSol(3, 10, 5)
    # print(opt.getNeighborhood(s))
    # print(opt.correctNeighborhood(opt.getNeighborhood(s), 5))
    # print(opt.opt(100, 5, 3, 1000, 3))


# main()
