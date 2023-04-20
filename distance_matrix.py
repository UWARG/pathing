import math
import data_structure_gen


def compute_euclidean_distance_matrix(locations):
    """return distance matrix in form of dictionary
    """
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances


paths = [
    ['Alpha', 'Foxtrot'],
    ['Alpha', 'Juliette'],
    ['Bravo', 'Juliette'],
    ['Delta', 'Charlie'],
    ['Echo', 'India'],
    ['Golf', 'Hotel'],
    ['Oscar', 'Kilo'],
    ['Mike', 'Lima'],
    ['Papa', 'November'],
]


# just adding every single start and end of the routes to the distance matrix
def distance_matrix():
    # for every point in list of paths
    dict = data_structure_gen.dictionary(False, False)
    points = []
    points.append(dict['Alpha'])
    for i in paths:
        points.append(dict[i[0]])
        points.append(dict[i[1]])

    computed_matrix_dict = compute_euclidean_distance_matrix(points)

    computed_matrix_list = []
    for key, value in computed_matrix_dict.items():
        temp_list = []
        for i, j in value.items():
            temp_list.append(j)
        computed_matrix_list.append(temp_list)

    return computed_matrix_list


# probably not useful but im gonna leave it here for funsies
def old_distance_matrix():

    points = data_structure_gen.list(False, False)
    computed_matrix_dict = compute_euclidean_distance_matrix(points)

    computed_matrix_list = []
    for key,value in computed_matrix_dict.items():
        temp_list = []
        for i,j in value.items():
            temp_list.append(j)
        computed_matrix_list.append(temp_list)
    
    return computed_matrix_list
