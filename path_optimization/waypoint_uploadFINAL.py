
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



def create_waypoint(command_id, latitude=0, longitude=0, altitude=0, hold=0, accept_radius=0, pass_radius=0, yaw=0):

    '''
    Takes in appropriate values, and sets them to create a waypoint
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



def waypoint_upload(coordinates:"list[tuple[float]]"):
    '''
    Takes in a list of  tuples of floats (lat long values) and uploads 
    them to missionplanner with their appropriate id, and reference frame
    
    '''
    
    current_latitude= cs.lat
    current_longitude= cs.lng

    index = 0
    takeoff = create_command(MAVLink.MAV_CMD.TAKEOFF, current_latitude, current_longitude)
    MAV.setWP(takeoff, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
    index += 1
    takeoff = create_command(MAVLink.MAV_CMD.TAKEOFF, current_latitude, current_longitude)
    MAV.setWP(takeoff, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
    index +=1

    for coordinate in coordinates:
        lat= coordinate[0]
        lng= coordinate[1]
        mav_waypoint = create_command(MAVLink.MAV_CMD.WAYPOINT, lat, lng)
        MAV.setWP(mav_waypoint, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
        index += 1 
    
    mav_waypoint = create_command(MAVLink.MAV_CMD.RETURN_TO_LAUNCH)
    MAV.setWP(mav_waypoint, index, MAVLink.MAV_FRAME.MISSION)
        
    MAV.setWPACK()



    







