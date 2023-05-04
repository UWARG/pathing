""" THIS FILE IS JUST FOR VISUALIZING THE PATHS SO ITS MESSY AF BUT WTV """

import pygame
from enum import Enum
from or_tools_algo import main, create_data_model
from distance_matrix import dict

waypoints_dict = dict
min_x, min_y = waypoints_dict['Alpha'][0], waypoints_dict['Alpha'][1]

for x, y in waypoints_dict.values():
    min_x, min_y = min(min_x, x), min(min_y, y)

waypoints_dict = {name: ((value[1] - min_y) / 2.5, (value[0] - min_x) / 2.5) for name, value in waypoints_dict.items()}

COLOURS = [(52, 167, 201), (207, 56, 124), (235, 158, 52), (153, 84, 232), (79, 232, 194)]


class Waypoints(Enum):
    Alpha = 0
    Bravo = 1
    Charlie = 2
    Delta = 3
    Echo = 4
    Foxtrot = 5
    Golf = 6
    Hotel = 7
    India = 8
    Juliette = 9
    Kilo = 10
    Lima = 11
    Mike = 12
    November = 13
    Oscar = 14
    Papa = 15
    Quebec = 16
    Point_18 = 17
    Romeo = 18
    Sierra = 19
    Tango = 20
    Uniform = 21
    Victor = 22
    Whiskey = 23
    Xray = 24
    Yankee = 25
    Zulu = 26


class AdjNode:
    def __init__(self, data):
        self.vertex = data
        self.next = None
        self.value = 0
        self.colour = None


# A class to represent a graph. A graph
# is the list of the adjacency lists.
# Size of the array will be the no. of the
# vertices "V"
class Graph:
    BLACK = (50, 50, 50)
    WHITE = (200, 200, 200)

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None] * self.V
        pygame.init()
        self.run = True
        self.screen = pygame.display.set_mode((1500, 1000))

    # Function to add an edge in an undirected graph
    def add_edge(self, src, dest, colour):
        # Adding the node to the source node
        node = AdjNode(dest)
        node.next = self.graph[src]
        node.colour = colour
        self.graph[src] = node

        # Adding the source node to the destination as
        # it is the undirected graph
        node = AdjNode(src)
        node.next = self.graph[dest]
        node.colour = colour
        self.graph[dest] = node

    # Function to print the graph
    def print_graph(self):

        # drawing waypoints and routes
        for key in waypoints_dict:
            if key == 'Alpha':
                pygame.draw.circle(self.screen, (207, 56, 124), (waypoints_dict[key][0], waypoints_dict[key][1]), 10)
            else:
                pygame.draw.circle(self.screen, self.WHITE, (waypoints_dict[key][0], waypoints_dict[key][1]), 10)
            for i in range(self.V):
                temp = self.graph[i]
                start_vert = waypoints_dict[Waypoints(i).name]
                while temp:
                    end_vert = waypoints_dict[Waypoints(temp.vertex).name]
                    pygame.draw.line(self.screen, temp.colour, start_vert, end_vert)
                    temp = temp.next

        # quit game
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()


def add_nodes_to_graph(graph):
    path_list = main()

    for index, path in enumerate(path_list):
        for point in path.visualization_path_list:
            graph.add_edge(Waypoints[point[0]].value, Waypoints[point[1]].value, COLOURS[index])

    return graph


graph = Graph(27)
add_nodes_to_graph(graph)

graph.print_graph()
