# Libs
import utm  # pip install utm
import shapely.geometry  # pip install shapely
import matplotlib.pyplot as plt  # pip install matplotlib
from math import sqrt, pow


BUFFER = 0.0001  # Planet Earth degrees (~11 metres)


# A sample bounded area
def restriction(start, end, bound):
    '''
    :type start, end: tuples(x,y) coordintes in UTM
    '''
    print("restriction()")
    # Represents the bounded area
    bounded = polygon(bound)

    boundedScaled = bounded.buffer(BUFFER, join_style=2)

    scaledPoints = list(boundedScaled.exterior.coords)

    vertices = [start, end]

    for points in scaledPoints:
        vertices.append(points)

    # Modified Dijkstra's algorithm

    distances = {}
    parents = {}
    queue = set()

    for vertex in vertices:
        distances[vertex] = float("inf")
        parents[vertex] = None
        queue.add(vertex)

    distances[start] = 0

    while len(queue) > 0:
        print("Loop")

        current_vertex = None
        current_distance = float("inf")
        for vertex in queue:
            d = distances[vertex]
            print(d)
            if d < current_distance:
                current_distance = d
                current_vertex = vertex

        if current_vertex is None:
            print("ERROR: -1")
            print(len(queue))
            break

        queue.remove(current_vertex)

        for vertex in vertices:
            if vertex == current_vertex:
                continue

            if intersect(vertex, current_vertex, bounded):
                print("Intersect, skip")
                continue

            if not vertex in queue:
                continue

            d = current_distance + distance(vertex, current_vertex)
            if d < distances[vertex]:
                distances[vertex] = d
                parents[vertex] = current_vertex

    sequence = [end]
    current = end

    while (current != start):
        if parents[current] is None:
            print("ERROR: -2")
            break

        sequence.insert(0, parents[current])
        current = parents[current]

    print(distances)
    print(parents)

    #really_finallist = [utm.to_latlon(i[0],i[1],19,'U') for i in finalList]

    return sequence


def intersect(start, end, boundedArea):
    '''
    Returns true if a line segment with endpoint start,end intersects a bounded region

    Parameters:
    start,end : tuple of (x,y) values
    boundedArea
    '''

    line = shapely.geometry.LineString([(start[0], start[1]), (end[0], end[1])])

    return line.intersects(boundedArea)


def distance(Point1, Point2):
    '''
    returns a float of distance between two points
    Point1, Point2 : tuples with (x,y) values
    '''
    return sqrt(pow(Point1[0] - Point2[0], 2) + pow(Point1[1] - Point2[1], 2))


def polygon(lst):
    '''
    returns a shapely polygon given a list of coordinates

    Current assumptions:
    list of points must be ordered to generate convex shape
    the polygon is composed of 4 points
    '''

    polyReturned = [[lst[coord][0], lst[coord][1]] for coord in range(len(lst))]

    return shapely.geometry.Polygon(polyReturned)

# Random code for testing
# lst = restriction(BRAVO, QUEBEC, bound)

# x, y = polygon(bound).exterior.xy
# plt.plot(x, y)
# for i in lst:
#     plt.plot(i[0], i[1], 'bo', linestyle="--")

# for i in range(len(names)):
#     plt.annotate(names[i], (bound[i][0], bound[i][1]))

# plt.annotate("START", (BRAVO[0], BRAVO[1]))
# plt.annotate("END", (QUEBEC[0], QUEBEC[1]))

# plt.show()
# print (lst)