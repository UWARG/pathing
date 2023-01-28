import pygame
import csv
from enum import Enum

min_x = 302040.33535061247
min_y = 5374350.079445223

waypoints_dict = {'Alpha': (818.681765564761, 704.4890672084875),
                  'Bravo': (914.7188790768414, 406.971431433456),
                  'Charlie': (859.6996074083872, 20.0),
                  'Delta': (762.8083579160593, 660.8905478811357),
                  'Echo': (49.95284312800504, 282.3065556753427),
                  'Foxtrot': (1428.6186876053544, 465.7259886134416),
                  'Golf': (540.896909219111, 532.629700880032),
                  'Hotel': (721.0388504122384, 605.5175412415992),
                  'India': (715.8753538846358, 570.8978201274294),
                  'Juliette': (1090.6707175938936, 769.1363809166942),
                  'Kilo': (444.71190177511016, 210.90717066219077),
                  'Lima': (1029.7583143423108, 288.78854405507445),
                  'Mike': (185.6049142487609, 833.702646224061),
                  'November': (651.3557325071743, 498.46217597764917),
                  'Oscar': (551.1331981609837, 547.8085447035264),
                  'Papa': (948.3559718949982, 346.61649848986417),
                  'Quebec': (881.7835133016633, 968.2598096290603),
                  'Point_18': (20.0, 590.184706106782),
                  'Romeo': (707.7516389627563, 200.7970903820824),
                  'Sierra': (927.3416660914809, 955.620900222566),
                  'Tango': (94.00416959755239, 256.9561401945539),
                  'Uniform': (953.666272884584, 60.993974533630535),
                  'Victor': (1083.9024167056923, 519.6145871703047),
                  'Whiskey': (1105.097261217772, 490.02062915218994),
                  'Xray': (1429.479621720864, 134.25759339053184),
                  'Yankee': (928.0562095595669, 550.0825357977301),
                  'Zulu': (260.9680535528314, 73.26624496164732)}

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


# A class to represent a graph. A graph
# is the list of the adjacency lists.
# Size of the array will be the no. of the
# vertices "V"
class Graph:
    BLACK = (50, 50, 50)
    WHITE = (200, 200, 200)
    BLUE = (52, 167, 201)
    PINK = (207, 56, 124)

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None] * self.V
        pygame.init()
        self.run = True
        self.screen = pygame.display.set_mode((1500, 1000))

    # Function to add an edge in an undirected graph
    def add_edge(self, src, dest):
        # Adding the node to the source node
        node = AdjNode(dest)
        node.next = self.graph[src]
        self.graph[src] = node

        # Adding the source node to the destination as
        # it is the undirected graph
        node = AdjNode(src)
        node.next = self.graph[dest]
        self.graph[dest] = node

    # Function to print the graph
    def print_graph(self):

        # drawing waypoints and routes
        for key in waypoints_dict:
            pygame.draw.circle(self.screen, self.WHITE, (waypoints_dict[key][0], waypoints_dict[key][1]), 10)
            for i in range(self.V):
                temp = self.graph[i]
                start_vert = waypoints_dict[Waypoints(i).name]
                while temp:
                    end_vert = waypoints_dict[Waypoints(temp.vertex).name]
                    pygame.draw.line(self.screen, self.PINK, start_vert, end_vert)
                    temp = temp.next

        # quit game
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()


def add_nodes_to_graph(graph):
    # Open file
    with open('myfile.csv') as file_obj:
        # Create reader object by passing the file object to reader method
        reader_obj = csv.reader(file_obj)

        # Iterate over each row in the csv file using reader object
        for row in reader_obj:
            x = row[0] if row[0] != "Point 18" else "Point_18"
            y = row[1] if row[1] != "Point 18" else "Point_18"

            graph.add_edge(Waypoints[x].value, Waypoints[y].value)

    return graph


graph = Graph(27)
add_nodes_to_graph(graph)

graph.print_graph()
