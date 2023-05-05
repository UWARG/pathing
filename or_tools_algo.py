"""Simple Pickup Delivery Problem (PDP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from distance_matrix import distance_matrix, paths, dict
import csv

import QR_CSV

MAX_DISTANCE = 8000
TOTAL_PATHS = 0


# class to keep track of things for each flight path
class DronePaths:
    def __init__(self, path, path_order, n_path, v_path, total_points, routes_completed, routes_flown):
        self.path_list = path
        self.path_order = path_order
        self.path_list_name = n_path
        self.visualization_path_list = v_path
        self.total_points = total_points
        self.routes_completed = routes_completed
        self.routes_flown = routes_flown


def create_data_model() -> dict:
    """Stores the data for the problem."""
    data = {'distance_matrix': distance_matrix(dict),
            'pickups_deliveries': [[i * 2 + 1, i * 2 + 2] for i in range(len(paths))],
            'depot': 0}
    return data


def print_solution(data, manager, routing, solution):
    # will fix this when i have time
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        plan_output = 'Route {}:\n'.format(vehicle_id + 1)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        total_distance += route_distance
    print('Total Distance of all routes: {}m'.format(total_distance))


def path_list(num_vehicles, manager, routing, solution) -> list[DronePaths]:
    # okay for this, just ignore the first location/name/wtv since its always just gonna be the start node
    global TOTAL_PATHS
    flight_paths = []
    route_points_dict = {}

    with open('QRpaths.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        index = 1
        for row in reader:
            route_points_dict[str(index) + " " + str(index + 1)] = [row[2],row[3]]
            index += 2
            TOTAL_PATHS += 1

    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        drone_path_list = []
        drone_path_order = []
        drone_path_list_named = []
        visualization_list = []
        route_points = 0
        routes_completed = 0
        routes_flown = 0
        while not routing.IsEnd(index):
            cur_index = manager.IndexToNode(index)
            drone_path_list.append(cur_index)
            if cur_index == 0:
                drone_path_list_named.append('Alpha')
            elif paths[(cur_index - 1) // 2][(cur_index - 1) % 2] != drone_path_list_named[-1]:
                drone_path_list_named.append(paths[(cur_index - 1) // 2][(cur_index - 1) % 2])
                routes_flown += 1

            previous_index = index
            index = solution.Value(routing.NextVar(index))
            if str(previous_index) + " " + str(index) in route_points_dict:
                route_points += float(route_points_dict[str(previous_index) + " " + str(index)][0])
                drone_path_order.append(route_points_dict[str(previous_index) + " " + str(index)][1])
                routes_completed += 1



        drone_path_list.append(0)
        drone_path_list_named.append('Alpha')
        for index in range(len(drone_path_list_named) - 1):
            visualization_list.append((drone_path_list_named[index], drone_path_list_named[index + 1]))

        flight_paths.append(
            DronePaths(drone_path_list, drone_path_order, drone_path_list_named, visualization_list, route_points, routes_completed, routes_flown))

    return flight_paths


"""
ALRIGHT HERE IS MY LINE OF THOUGHT

i couldn't figure out how to get the node dropping thing to work with this stupid line of code
routing.solver().Add(routing.NextVar(pickup_index) == delivery_index)...

so instead whats happening rn is that we start with a single vehicle, and we increase the vehicle number by 1
everytime until there is a viable route

we should know how far the drone can travel in one go (which will be the MAX_DISTANCE) and then also approximately
how long it takes the drone to travel the MAX_DISTANCE. so then we know how many times the drone can fly in the hour,
lets call that x, so then we just take the first x routes.
"""


def calculate_route(num_vehicles, data_model) -> list[DronePaths]:
    """Entry point of the program."""
    # Instantiate the data problem.
    data = data_model

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           num_vehicles, data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack  (idk what this does)
        MAX_DISTANCE,  # vehicle maximum travel distance
        True,  # start cumul to zero (i also dk what this does)
        dimension_name)

    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Define Transportation Requests.
    for request in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])

        # Using pickup and delivery feature for our case, where pickup is the starting node and delivery is end

        routing.AddPickupAndDelivery(pickup_index, delivery_index)

        routing.solver().Add(
            # Same vehicle must do both pickup and delivery
            routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
        # Pickup before delivery
        routing.solver().Add(
            # Pickup and delivery must be done by same vehicle
            distance_dimension.CumulVar(pickup_index) <= distance_dimension.CumulVar(delivery_index))
        # Pickup and delivery must be consequetive
        routing.solver().Add(routing.NextVar(pickup_index) == delivery_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # return solution is there is one
    if solution:
        return path_list(num_vehicles, manager, routing, solution)
    else:
        return calculate_route(num_vehicles + 1, data_model)


def main() -> list[DronePaths]:
    drone_paths = []
    routes_completed = 0
    flight_paths = calculate_route(1, create_data_model())

    # sort the flight paths based on the total points we receive from flying each path
    flight_paths.sort(key=lambda p: p.routes_flown / p.routes_completed if p.routes_completed > 0 else 0)
    # we have an hour to fly and have a flight time of 12 minutes, so we take the top 5 paths
    # that give us the most points
    for path in flight_paths:
        if routes_completed > TOTAL_PATHS // 2:
            return drone_paths
        routes_completed += path.routes_completed
        drone_paths.append(path.path_list_name)

    return drone_paths



if __name__ == '__main__':

    QR_CSV.QR_CSV()

    drone_paths = str(main())
    print(drone_paths)