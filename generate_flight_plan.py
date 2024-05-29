import re
from typing import List
from modules import load_waypoint_name_to_coordinates_map
import copy
import math
import pathlib
from modules import waypoint

import random

WAYPOINT_FILE_PATH = pathlib.Path("waypoints", "wrestrc_waypoints.csv")
RESULT, WAYPOINT_NAMES_TO_COORDINATES = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(WAYPOINT_FILE_PATH)

EARTH_RADIUS = 6371

TIME_LIMIT = 30
PASSENGER_CAPACITY = 6
DRONE_WEIGHT = 8
DRONE_RANGE = 1000
BEGINNING_WAYPOINT = "Alpha"

example_qr_text = "Route number 1: 2 pers; Lima; Quebec; 15 kg; obstacle 2 m to NE; $112 Route number 2: 6 pers; Delta; Charlie; 5 kg; nil; $50 Route number 3: 4 pers; Alpha; Zulu; 15 kg; other comment; $150"

example_qr_text_2 = "Route number 1: 4 pers; Charlie; Golf; 2 kg; nil; $159 Route number 2: 2 pers; Yankee; November; 6 kg; nil; $77 Route number 3: 6 pers; India; Echo; 4 kg; nil; $116 Route number 4: 5 pers; Oscar; Papa; 7 kg; nil; $124 Route number 5: 2 pers; Hotel; Delta; 7 kg; nil; $190 Route number 6: 2 pers; Golf; Delta; 4 kg; nil; $63 Route number 7: 2 pers; Foxtrot; Juliette; 6 kg; nil; $188 Route number 8: 4 pers; Alpha; Romeo; 8 kg; nil; $57 Route number 9: 2 pers; Tango; Sierra; 1 kg; nil; $52 Route number 10: 6 pers; Golf; Lima; 9 kg; nil; $123 Route number 11: 3 pers; Kilo; Point 18; 14 kg; nil; $106 Route number 12: 4 pers; Quebec; Zulu; 15 kg; nil; $143 Route number 13: 4 pers; Golf; India; 12 kg; nil; $71 Route number 14: 5 pers; Romeo; Juliette; 12 kg; nil; $62 Route number 15: 3 pers; Sierra; Oscar; 12 kg; nil; $151 Route number 16: 4 pers; Xray; November; 9 kg; nil; $56 Route number 17: 3 pers; Bravo; Alpha; 14 kg; nil; $69 Route number 18: 5 pers; Charlie; Whiskey; 2 kg; nil; $152 Route number 19: 3 pers; Whiskey; Papa; 5 kg; nil; $151 Route number 20: 1 pers; Romeo; Echo; 2 kg; nil; $73"

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
  
def process_qr_text(qr_text) -> List[Route]:
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

def get_flight_plan(max_range: float, routes: List[Route]) -> List[Route]:
  current_location = WAYPOINT_NAMES_TO_COORDINATES[BEGINNING_WAYPOINT]
  
  remaining_range = max_range
  
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
    max_weight = random.randint(1, 15)
    profit = random.randint(50, 200)


    start = random.choice(waypoint_names)
    end = random.choice(waypoint_names)

    while(start == end):
      end = random.choice(waypoint_names)

    str = f"Route number {i + 1}: {passengers} pers; {start}; {end}; {max_weight} kg; nil; ${profit} "
    
    qr_text += str

  return qr_text

processed_text = process_qr_text(example_qr_text)

flight_plan_result = get_flight_plan(DRONE_RANGE, processed_text)

profit = 0

for route in flight_plan_result:
  profit += route.profit
  
  
  print(route)

print(f"Total profit: ${profit}")