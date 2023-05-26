
import math

import data_structure_gen


NAMES = [
    "Alpha",
    "Bravo",
    "Charlie",
    "Delta",
    "Echo",
    "Foxtrot",
    "Golf",
    "Hotel",
    "India",
    "Juliette",
    "Kilo",
    "Lima",
    "Mike",
    "November",
    "Oscar",
    "Papa",
    "Quebec",
    "Point 18",
    "Romeo",
    "Sierra",
    "Tango",
    "Uniform",
    "Victor",
    "Whiskey",
    "Xray",
    "Yankee",
    "Zulu",
]


if __name__ == "__main__":
    coordinates = data_structure_gen.dictionary_imacs("Waypoints_IMACS.csv", True)

    distances = []
    for name0 in NAMES:
        for name1 in NAMES:
            distance = math.hypot(float(coordinates[name1][0]) - float(coordinates[name0][0]), float(coordinates[name1][1]) - float(coordinates[name0][1]))
            distances.append(((name0, name1), distance / 360 * 40_000_000))

    distances.sort()
    for distance in distances:
        print(distance[0][0] + "," + distance[0][1] + "," + str(int(distance[1])))
