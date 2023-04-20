"""Simple Pickup Delivery Problem (PDP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from distance_matrix import distance_matrix, old_distance_matrix, paths


MAX_DISTANCE = 5000

def create_data_model():
    """Stores the data for the problem."""
    data = {}

    # ignore
    # paths = [
    #     [1, 6],
    #     [2, 10],
    #     [4, 3],
    #     [5, 9],
    #     [7, 8],
    #     [15, 11],
    #     [13, 12],
    #     [16, 14],
    # ]

    data['distance_matrix'] = distance_matrix()
    data['pickups_deliveries'] = [[i*2 + 1, i*2 + 2] for i in range(len(paths))]
    # data['demands'] = [1 if num % 2 == 1 else -1 for num in range(len(data['distance_matrix']))]
    # data['vehicle_capacities'] = [1]

    # this is how many "trips" we're taking. solution is kind of jank but whatever lol
    # i have no idea what this does
    data['depot'] = 0
    return data


def print_solution(num_vehicles, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        plan_output = 'Route {}:\n'.format(vehicle_id+1)
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


def path_list(num_vehicles, manager, routing, solution):
    # okay for this, just ingore the first location/name/wtv since its always just gonna be the start node
    drone_path_list = []
    drone_path_list_named = []
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        drone_path_list.append([])
        drone_path_list_named.append([])
        while not routing.IsEnd(index):
            cur_index = manager.IndexToNode(index)
            drone_path_list[-1].append(cur_index)
            if index == 0:
                drone_path_list_named[-1].append('Alpha')
            else:
                drone_path_list_named[-1].append(paths[(cur_index - 1) // 2][(cur_index - 1) % 2])
            index = solution.Value(routing.NextVar(index))
    print(drone_path_list)
    print(drone_path_list_named)
    return drone_path_list


def aaa(num_vehicles, data_model):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = data_model

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           num_vehicles, data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # for node in [i for i in range(0,20)]:
    #     routing.AddDisjunction(
    #         nodes=[node],
    #         penalty=0)

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
        0,  # no slack
        MAX_DISTANCE,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)

    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # def demand_callback(from_index):
    #     """Returns the demand of the node."""
    #     # Convert from routing variable Index to demands NodeIndex.
    #     from_node = manager.IndexToNode(from_index)
    #     return data['demands'][from_node]
    #
    # demand_callback_index = routing.RegisterUnaryTransitCallback(
    #     demand_callback)
    # routing.AddDimensionWithVehicleCapacity(
    #     demand_callback_index,
    #     0,  # null capacity slack
    #     [40],  # vehicle maximum capacities
    #     True,  # start cumul to zero
    #     'Capacity')


    # Define Transportation Requests.
    for request in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            # Same vehicle must do both
            routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
        routing.solver().Add(
            # Must be done by same vehicle
            distance_dimension.CumulVar(pickup_index) <= distance_dimension.CumulVar(delivery_index))
        routing.solver().Add(routing.NextVar(pickup_index) == delivery_index)

    # penalty = 10000000000
    # for node in data['pickups_deliveries']:
    #     start, end = node
    #     routing.AddDisjunction(
    #         [manager.NodeToIndex(end)], 0
    #     )
    #
    #     routing.AddDisjunction(
    #         [manager.NodeToIndex(start)], penalty
    #     )

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)
    search_parameters.time_limit.FromSeconds(10)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)


    # Print solution on console.
    if solution:
        print_solution(num_vehicles, manager, routing, solution)
        path_list(num_vehicles, manager, routing, solution)
    else:
        aaa(num_vehicles + 1, data_model)


if __name__ == '__main__':
    aaa(1, create_data_model())
