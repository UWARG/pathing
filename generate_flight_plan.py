import re
from typing import List
from modules import load_waypoint_name_to_coordinates_map
import copy
import math
import pathlib
from modules import waypoint

import random #to generate test cases, remove in production

WAYPOINT_FILE_PATH = pathlib.Path("waypoints", "wrestrc_waypoints.csv")
RESULT, WAYPOINT_NAMES_TO_COORDINATES = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(WAYPOINT_FILE_PATH)

EARTH_RADIUS = 6371

PASSENGER_CAPACITY = 6
DRONE_WEIGHT = 8 #kg
DRONE_RANGE = 1000 #Battery recharges are included in range
BEGINNING_WAYPOINT = "Alpha" #starting waypoint

class Route:
  def __init__(self, route_number: int, passengers: int, start_waypoint: str, end_waypoint: str, max_weight: float, notes: str, profit: int):
    waypoint_coordinates = [WAYPOINT_NAMES_TO_COORDINATES[start_waypoint], WAYPOINT_NAMES_TO_COORDINATES[end_waypoint]]
    
    self.route_number = route_number
    self.passengers = passengers
    self.start_waypoint = start_waypoint
    self.end_waypoint = end_waypoint
    self.max_weight = max_weight
    self.notes = notes
    self.profit = profit
    self.distance = distance_between_coordinates(waypoint_coordinates[0], waypoint_coordinates[1])
    
  def __str__(self):
    return f"Route {self.route_number}: {self.passengers} passengers, {self.max_weight} kg limit, from {self.start_waypoint} to {self.end_waypoint}, {self.profit} profit, distance {self.distance}m"
  
def distance_between_coordinates(coordinate_1: waypoint.location_ground.LocationGround, coordinate_2: waypoint.location_ground.LocationGround) -> float:
  #get distance between coordinates in m
  
  #convert decimal degrees to radians
  lon1, lat1, lon2, lat2 = map(math.radians, [coordinate_1.longitude, coordinate_1.latitude, coordinate_2.longitude, coordinate_2.latitude])
  
  long_difference = lon2 - lon1
  lat_difference = lat2 - lat1
    
  dist = 2*EARTH_RADIUS*math.asin(math.sqrt(math.sin(lat_difference/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(long_difference/2)**2))*1000
  
  return dist
  
def qr_text_to_routes(qr_text) -> List[Route]:
  #get list of all valid routes (removes routes that exceed passenger capacity or drone weight limit)
  
  route_pattern = r"Route number (\d+): (\d+) pers; ([^;]+); ([^;]+); (\d+) kg; ([^;]+); \$(\d+)"
  matches=re.findall(route_pattern, qr_text)
  
  routes = []
  
  for match in matches:
    route_number = int(match[0])
    passengers = int(match[1])
    start_waypoint = match[2]
    end_waypoint = match[3]
    max_vehicle_weight = int(match[4])
    remarks = match[5]
    earnings = int(match[6])
    if(passengers <= PASSENGER_CAPACITY and max_vehicle_weight >= DRONE_WEIGHT):
      route = Route(route_number, passengers, start_waypoint, end_waypoint, max_vehicle_weight, remarks, earnings)
      routes.append(route)
  return routes

def get_next_route(current_location: waypoint.location_ground.LocationGround, available_routes: List[Route], remaining_range: float) -> Route:
  #get next waypoint based on current waypoint and list of routes
  best_route = available_routes[0]
  highest_profit_per_km, range_consumed = 0, 0
  
  for route in available_routes:
    total_distance = 0
    if(route.start_waypoint == current_location.name):
      total_distance = route.distance
    else:
      total_distance = distance_between_coordinates(current_location, WAYPOINT_NAMES_TO_COORDINATES[route.start_waypoint]) + route.distance
    if(total_distance > remaining_range):
      continue
    profit_per_km = route.profit/total_distance
    
    if(profit_per_km > highest_profit_per_km):
      highest_profit_per_km = profit_per_km
      best_route = route
      range_consumed = total_distance
    
  if(highest_profit_per_km == 0):
    return False, None, None

  return True, best_route, range_consumed

def get_flight_plan(drone_range: float, routes: List[Route]) -> List[Route]:
  current_location = WAYPOINT_NAMES_TO_COORDINATES[BEGINNING_WAYPOINT]
  
  remaining_range = drone_range
  
  #objectives: maximize earnings --> prioritize earnings/total distance
  routes_copy = copy.deepcopy(routes)
  flight_plan = []
  
  for i in range(len(routes)):
    result, next_route, range_consumed = get_next_route(current_location, routes_copy, remaining_range)
    
    if(not result):
      break
    
    remaining_range -= range_consumed
    flight_plan.append(next_route)
    routes_copy.remove(next_route)
    current_location = WAYPOINT_NAMES_TO_COORDINATES[next_route.end_waypoint]

  return flight_plan

def generate_test_cases(number_of_cases: int):
  qr_text = ""

  for i in range (number_of_cases):
    waypoint_names = list(WAYPOINT_NAMES_TO_COORDINATES.keys())
    passengers = random.randint(1, 6)
    max_weight = random.randint(5, 20)
    profit = random.randint(50, 200)


    start_waypoint = random.choice(waypoint_names)
    end_waypoint = random.choice(waypoint_names)

    while(start_waypoint == end_waypoint):
      end_waypoint = random.choice(waypoint_names)

    route_text = f"Route number {i + 1}: {passengers} pers; {start_waypoint}; {end_waypoint}; {max_weight} kg; nil; ${profit} "
    
    qr_text += route_text

  return qr_text

NUM_TEST_CASES = 10

test_qr_text = generate_test_cases(NUM_TEST_CASES)
routes_list = qr_text_to_routes(test_qr_text)
flight_plan_result = get_flight_plan(DRONE_RANGE, routes_list)
revenue = 0

print("Flight Plan:")
for route_item in flight_plan_result:
  revenue += route_item.profit
  print(route_item)

print("fraction of routes completed:", len(flight_plan_result)/NUM_TEST_CASES) #percentage of routes completed
print(f"Total profit: ${revenue}") #total profit

# TODO: find a way to get the optimal flight plan. The current implementation is a greedy algorithm that may not always be optimal.