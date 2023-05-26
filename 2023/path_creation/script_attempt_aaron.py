import math
import clr
import time
import System
from System import Byte

clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink


def create_command(command_id, latitude=0, longitude=0, altitude=0, hold=0, accept_radius=0, pass_radius=0, yaw=0):
    waypoint = Locationwp()
    
    Locationwp.id.SetValue(waypoint, int(command_id))
    Locationwp.p1.SetValue(waypoint, hold)
    Locationwp.p2.SetValue(waypoint, accept_radius)
    Locationwp.p3.SetValue(waypoint, pass_radius)
    Locationwp.p3.SetValue(waypoint, yaw)
    Locationwp.lat.SetValue(waypoint, latitude)
    Locationwp.lng.SetValue(waypoint, longitude)
    Locationwp.alt.SetValue(waypoint, altitude)
    return waypoint

def waypoint_upload(coordinates):
    index=0
    current_latitude= cs.lat
    current_longitude= cs.lng
    
    for coordinate in coordinates:
        lat= coordinate[0]
        lng= coordinate[1]
        mav_waypoint = create_command(MAVLink.MAV_CMD.WAYPOINT, lat, lng)
        MAV.setWP(mav_waypoint, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
        index += 1 

    index = 0
    takeoff = create_command(MAVLink.MAV_CMD.TAKEOFF, current_latitude, current_longitude)
    MAV.setWP(takeoff, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
    index += 1
    takeoff = create_command(MAVLink.MAV_CMD.TAKEOFF, current_latitude, current_longitude)
    MAV.setWP(takeoff, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
    index +=1

    mav_waypoint = create_command(MAVLink.MAV_CMD.RETURN_TO_LAUNCH)
    MAV.setWP(mav_waypoint, index, MAVLink.MAV_FRAME.MISSION)


MAV.setWPACK()

# sys.path.append(r"C:\Users\WARG\Documents\WARG\UWARG-Path-Optimization")
import sys
# This appends a path to mission planner (u only have to call it once per path per session)
sys.path.append(r"C:\Users\WARG\Desktop\funsies")
sys.path.append(r"C:\Users\WARG\Desktop\funsies\shapely")
from math import sqrt, pow
import utm
import shapely.geometry


# I copied the file here in an attempt to fix things (it did not fix anything)
def restriction(start, end, bound):
    '''
    :type start, end: tuples(x,y) coordintes in UTM
    '''
    # Represents the bounded area
    bounded = polygon(bound)

    boundedScaled = bounded.buffer(15, join_style=2)

    scaledPoints = list(boundedScaled.exterior.coords)

    graph = [start, end]

    for x in scaledPoints:
        graph.append(x)

    dist = {}
    prev = {}
    queue = []

    for x in graph:
        dist[x] = float('inf')
        prev[x] = 0
        queue.append(x)

    dist[start] = 0

    while queue:
        unvisited = []
        tempNode = min(queue)

        for node in graph:
            if (node == tempNode): continue
            if (intersect(tempNode, node, bounded) == False):
                unvisited.append(node)

        queue.remove(tempNode)
        for node in unvisited:
            tempDist = dist[tempNode] + distance(tempNode, node)
            if (tempDist < dist[node]):
                dist[node] = tempDist
                prev[node] = tempNode

    finalList = [end]
    tempCurrent = end

    while (tempCurrent != start):
        finalList.insert(0, prev[tempCurrent])
        tempCurrent = prev[tempCurrent]

    really_final_list = [utm.to_latlon(i[0],i[1],19,'U') for i in finalList]

    return really_final_list


def intersect(start, end, boundedArea):

    line = shapely.geometry.LineString([(start[0], start[1]), (end[0], end[1])])

    return line.intersects(boundedArea)


def distance(Point1, Point2):
    return sqrt(pow(Point1[0] - Point2[0], 2) + pow(Point1[1] - Point2[1], 2))


def polygon(lst):
    polyReturned = [[lst[coord][0], lst[coord][1]] for coord in range(len(lst))]

    return shapely.geometry.Polygon(polyReturned)

# Random testing points + calling function to test (nothing was tested because importing doesnt work)
ALPHA = utm.from_latlon(48.5166707,-71.6375025) 
VICTOR = utm.from_latlon(48.510353,-71.6228085)
NOVEMBER = utm.from_latlon(48.5090567,-71.6461702)
OSCAR = utm.from_latlon(48.5107057,-71.6516848)
BRAVO = utm.from_latlon(48.5060947,-71.6317518)
QUEBEC =  utm.from_latlon(48.5262308,-71.6345802)
ZULU = utm.from_latlon(48.4932846,-71.6664874)

bound = [ALPHA,VICTOR,NOVEMBER,OSCAR]

waypoints = restriction(BRAVO,QUEBEC,bound)

waypoint_upload(waypoints)