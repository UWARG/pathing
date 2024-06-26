import re
from typing import List
from modules import load_waypoint_name_to_coordinates_map
import copy
import math
import pathlib
from modules import waypoint
import random  # to generate test cases, remove in production
import route as routeObj

WAYPOINT_FILE_PATH = pathlib.Path("waypoints", "wrestrc_waypoints.csv")
RESULT, WAYPOINT_NAMES_TO_COORDINATES = (
    load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(WAYPOINT_FILE_PATH)
)

EARTH_RADIUS = 6371

PASSENGER_CAPACITY = 6
DRONE_WEIGHT = 8  # kg
DRONE_RANGE = 1000  # Battery recharges are included in range
BEGINNING_WAYPOINT = "Alpha"  # starting waypoint

def generate_test_cases(number_of_cases: int):
    qr_text = ""

    for i in range(number_of_cases):
        waypoint_names = list(WAYPOINT_NAMES_TO_COORDINATES.keys())
        passengers = random.randint(1, 6)
        max_weight = random.randint(5, 20)
        profit = random.randint(50, 200)

        start_waypoint = random.choice(waypoint_names)
        end_waypoint = random.choice(waypoint_names)

        while start_waypoint == end_waypoint:
            end_waypoint = random.choice(waypoint_names)

        route_text = f"Route number {i + 1}: {passengers} pers; {start_waypoint}; {end_waypoint}; {max_weight} kg; nil; ${profit} "

        qr_text += route_text

    return qr_text


def qr_text_to_routes(qr_text) -> List[routeObj.Route]:
    # get list of all valid routes (removes routes that exceed passenger capacity or drone weight limit)

    route_pattern = r"Route number (\d+): (\d+) pers; ([^;]+); ([^;]+); (\d+) kg; ([^;]+); \$(\d+)"
    matches = re.findall(route_pattern, qr_text)

    routes = []

    for match in matches:
        route_number = int(match[0])
        passengers = int(match[1])
        start_waypoint = match[2]
        end_waypoint = match[3]
        max_vehicle_weight = int(match[4])
        remarks = match[5]
        earnings = int(match[6])
        if passengers <= PASSENGER_CAPACITY and max_vehicle_weight >= DRONE_WEIGHT:
            route = routeObj.Route(
                route_number,
                passengers,
                start_waypoint,
                end_waypoint,
                max_vehicle_weight,
                remarks,
                earnings,
            )
            routes.append(route)
    return routes


def get_next_route(
    current_location: waypoint.location_ground.LocationGround,
    available_routes: List[routeObj.Route],
    remaining_range: float,
) -> routeObj.Route:
    # get next waypoint based on current waypoint and list of routes
    best_route = [available_routes[0]]
    highest_profit_per_km, range_consumed = 0, 0

    for route in available_routes:
        total_distance = 0
        if route.start_waypoint.name == current_location.name:
            total_distance = route.distance
        else:
            total_distance = (
                routeObj.Route.distance_between_locations(
                    current_location, route.start_waypoint
                )
                + route.distance
            )
        if total_distance > remaining_range:
            continue
        profit_per_km = route.profit / total_distance

        if profit_per_km > highest_profit_per_km:
            highest_profit_per_km = profit_per_km
            best_route = [route]
            range_consumed = total_distance

    if highest_profit_per_km == 0:
        return False, None, None

    return True, best_route, range_consumed

#search the best route with foresight NOTE: i dont know how to do the output type annotation
def get_next_route_depth(
    current_location: waypoint.location_ground.LocationGround,
    available_routes: List[routeObj.Route],
    remaining_range: float,
):
    
    best_single_route = None
    best_double_route = None
    
    total_distance_single = 0
    total_distance_double = 0
    
    highest_single_specific_profit = 0
    highest_double_specific_profit = 0
    
    for first_route in available_routes:
        # get the range consumed by the first route
        range_consumed_single = 0
        range_consumed_single += routeObj.Route.distance_between_locations(
            current_location, first_route.start_waypoint
        )
        range_consumed_single += first_route.distance
        if range_consumed_single > remaining_range:
            continue
        
        profit_per_km = first_route.profit / range_consumed_single

        if profit_per_km > highest_single_specific_profit:
            highest_single_specific_profit = profit_per_km
            best_single_route = [first_route]
            total_distance_single = range_consumed_single
        
        range_consumed_double = range_consumed_single
        
        for second_route in available_routes:
            if second_route == first_route:
                continue
            
            range_consumed_double += routeObj.Route.distance_between_locations(
                first_route.end_waypoint, second_route.start_waypoint
            )
            range_consumed_double += second_route.distance
            
            if range_consumed_double > remaining_range:
                continue
            
            profit_per_km = (first_route.profit + second_route.profit) / range_consumed_double
            
            if profit_per_km > highest_double_specific_profit:
                highest_double_specific_profit = profit_per_km
                best_double_route = [first_route, second_route]
                total_distance_double = range_consumed_double
    
    if best_single_route is None:
        return False, None, None
    
    if highest_double_specific_profit > highest_single_specific_profit:
        return True, best_double_route, total_distance_double
    
    return True, best_single_route, total_distance_single

# def get_next_route_recursive(
#     current_location: waypoint.location_ground.LocationGround,
#     available_routes: List[routeObj.Route],
#     remaining_range: float,
#     depth: int,
# ):
    
#     best_route_sequences = []
    
#     total_distance = 0
    
#     highest_profits_per_km = []
    
#     def recursiveThingy(targetDepth, depth):
        
    
#     return True, best_single_route, total_distance_single

def get_flight_plan(drone_range: float, routes: List[routeObj.Route]) -> List[routeObj.Route]:
    current_location = WAYPOINT_NAMES_TO_COORDINATES[BEGINNING_WAYPOINT]

    remaining_range = drone_range

    # objectives: maximize earnings --> prioritize earnings/total distance
    routes_copy = copy.deepcopy(routes)
    flight_plan = []

    for i in range(len(routes)):
        result, next_routes, range_consumed = get_next_route(
            current_location, routes_copy, remaining_range
        )

        if not result:
            break

        remaining_range -= range_consumed
        
        for route in next_routes:
            flight_plan.append(route)
            routes_copy.remove(route)
            
        current_location = next_routes[-1].end_waypoint

    return flight_plan

def get_flight_plan_depth(drone_range: float, routes: List[routeObj.Route]) -> List[routeObj.Route]:
    current_location = WAYPOINT_NAMES_TO_COORDINATES[BEGINNING_WAYPOINT]

    remaining_range = drone_range

    # objectives: maximize earnings --> prioritize earnings/total distance
    routes_copy = copy.deepcopy(routes)
    flight_plan = []

    for i in range(len(routes)):
        result, next_routes, range_consumed = get_next_route_depth(
            current_location, routes_copy, remaining_range
        )

        if not result:
            break

        remaining_range -= range_consumed
        
        for route in next_routes:
            flight_plan.append(route)
            routes_copy.remove(route)
            
        current_location = next_routes[len(next_routes) - 1].end_waypoint

    return flight_plan

NUM_TEST_CASES = 50

test_qr_text = generate_test_cases(NUM_TEST_CASES)
routes_list = qr_text_to_routes(test_qr_text)
flight_plan_result = get_flight_plan(DRONE_RANGE, routes_list)
flight_plan_result_depth = get_flight_plan_depth(DRONE_RANGE, routes_list)
revenue = 0
revenue_depth = 0
theoretical_revenue = 0

print("Flight Plan:")
for route_item in flight_plan_result:
    revenue += route_item.profit
    print(route_item.start_waypoint.name, " -> ", route_item.end_waypoint.name, " : ", route_item.profit, "$")

for route_item in routes_list:
    theoretical_revenue += route_item.profit
    
print("Theoretical Revenue: $", theoretical_revenue)

print(
    "Fraction of routes completed:", len(flight_plan_result) / NUM_TEST_CASES
)  # percentage of routes completed
 # total profit

print ("\n\nFlight Plan Depth:")
for route_item in flight_plan_result_depth:
    revenue_depth += route_item.profit
    print(route_item.start_waypoint.name, " -> ", route_item.end_waypoint.name, " : ", route_item.profit, "$")
print(
    "Fraction of routes completed:", len(flight_plan_result) / NUM_TEST_CASES
) 
print("Fraction of routes completed:", len(flight_plan_result_depth) / NUM_TEST_CASES)

print(f"Total profit: $ {revenue}") 
print(f"Total profit depth: $ {revenue_depth}")  # total profit#
# TODO: find a way to get the optimal flight plan. The current implementation is a greedy algorithm that may not always be optimal.
