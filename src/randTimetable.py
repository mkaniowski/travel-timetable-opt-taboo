import os
import json
from city import City
import numpy as np


def randTimetable():
    cities = []
    out = []
    with open(f'{os.getcwd()}/src/data/cities.json', 'r') as f:
        data = json.load(f)

    for i in data:
        cities.append(City(i['city'], i['lat'], i['lon']))

    for i in range(len(cities)):
        city = {
            'name': cities[i].name,
            'timetable': []
        }
        for h in range(24):
            # city['timetable'].append(TimetableMatrix(h, len(cities)))
            # mat = np.random.randint(
            #     low=0, high=2, size=(len(cities), len(cities)))
            mat = np.full((len(cities), len(cities), 3), fill_value=[0, 0, 0])
            for row in range(len(cities)):
                for col in range(len(cities)):
                    if row == col:
                        continue
                    mat[row][col] = np.random.randint(
                        low=0, high=2, size=3)
            city['timetable'].append(mat.tolist())

        out.append(city)

    jsonData = json.dumps(out, sort_keys=True, indent=4)

    with open(f'{os.getcwd()}/src/data/timetable.json', 'w') as f:
        f.write(jsonData)
