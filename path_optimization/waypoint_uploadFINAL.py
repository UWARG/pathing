
import sys
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


def create_command(command_id, index, p1=0, p2=0, p3=0, p4=0, lat=0, lng=0, alt=50):
    '''
    Used to create any command in mission planner
    
    '''
    command=Locationwp()
    command.id=index
    command.command=command_id
    command.p1=p1
    command.p2=p2
    command.p3=p3
    command.p4=p4
    command.lat=lat
    command.lng=lng
    command.alt=alt
    return command


def create_waypoint(command_id, latitude=0, longitude=0, altitude=50, hold=0, accept_radius=0, pass_radius=0, yaw=0):

    '''
    Takes in appropriate values, and sets them to create a waypoint

    https://mavlink.io/en/messages/common.html#MAV_CMD_NAV_WAYPOINT
    1: Hold	Hold time. (ignored by fixed wing, time to stay at waypoint for rotary wing)	min:0	s
    2: Accept Radius	Acceptance radius (if the sphere with this radius is hit, the waypoint counts as reached)	min:0	m
    3: Pass Radius	0 to pass through the WP, if > 0 radius to pass by WP. Positive value for clockwise orbit, negative value for counter-clockwise orbit. Allows trajectory control.		m
    4: Yaw	Desired yaw angle at waypoint (rotary wing). NaN to use the current system yaw heading mode (e.g. yaw towards next waypoint, yaw to home, etc.).		deg
    5: Latitude	Latitude		
    6: Longitude	Longitude		
    7: Altitude
    '''
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
    '''
    Takes in a list of  tuples of floats (lat long values) and uploads 
    them to missionplanner with their appropriate id, and reference frame
    
    '''
    
    current_latitude= cs.lat
    current_longitude= cs.lng

    # The line below throws an error
    #MAVLink.MAV_VTOL_STATE_MC

    index = 0
    takeoff = create_waypoint(MAVLink.MAV_CMD.TAKEOFF, current_latitude, current_longitude)
    MAV.setWP(takeoff, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
    index += 1
    # takeoff = create_waypoint(MAVLink.MAV_CMD.TAKEOFF, current_latitude, current_longitude)
    # MAV.setWP(takeoff, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
    # index +=1

    #MAVLink.MAV_VTOL_STATE_TRANSITION_TO_FW

    #MAVLink.MAV_VTOL_STATE_FW

    for coordinate in coordinates:
        
        lat= coordinate[0]
        lng= coordinate[1]
        mav_waypoint = create_waypoint(MAVLink.MAV_CMD.WAYPOINT, lat, lng)
        MAV.setWP(mav_waypoint, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
        index += 1 
    
    #MAVLink.MAV_VTOL_STATE_TRANSITION_TO_MC

    #MAVLink.MAV_VTOL_STATE_MC
    
    mav_waypoint = create_waypoint(MAVLink.MAV_CMD.RETURN_TO_LAUNCH)
    MAV.setWP(mav_waypoint, index, MAVLink.MAV_FRAME.MISSION)
        
    MAV.setWPACK()

filename = "C:\\Users\\WARG\\Documents\\WARG\\IMACS\\path_optimization\\paths.txt"

while True:
    input_file = open(filename, "r")
    line = input_file.read()

    if not line:
        print("Empty Line")
    else:
        print(line)
        break

    time.sleep(2)

print("Received Waypoints")
waypoints = list(eval(line))
print(type(waypoints))

# Erase the contents of the paths.txt file
open(filename, 'w').close()

waypoint_upload(waypoints)

print("Done")
    







