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
        cities.append(City(i['city'], i['lat'], i['lon'], 0, 0))

    for i in range(len(cities)):
        city = {
            'name': cities[i].name,
            'timetable': []
        }

        mat = np.full((24, len(cities), 3), fill_value=[0, 0, 0])

        for t in range(24):
            for c in range(len(cities)):
                mat[t][c] = np.random.randint(
                    low=0, high=2, size=3)
            mat[t][i] = [0, 0, 0]

        city['timetable'].append(mat.tolist())

        out.append(city)

    jsonData = json.dumps(out, sort_keys=True, indent=4)

    with open(f'{os.getcwd()}/src/data/timetable.json', 'w') as f:
        f.write(jsonData)


# {
#     "name": "warsaw",
#     "timetable":
#     [
#      24 arrays (time) of cities
#         [
#          12 arrays (cities) of avalible transport
#             [0, 1, 1],
#             []
#         ],
#         [],
#         [],
#         []
#     ]
# }
