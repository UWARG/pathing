# longitude = Script.GetParam("lat")
# latitude = Script.GetParam("lng")

# print(MAV.getWPCount())

# MAV.setWp

# print(longitude, latitude)
# Script.ChangeParam("lat", latitude+10)
# Script.ChangeParam("lng", longitude+10)

# print('Coordinates changed')  




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

# https://mavlink.io/en/messages/common.html#MAV_CMD_NAV_WAYPOINT
# 1: Hold	Hold time. (ignored by fixed wing, time to stay at waypoint for rotary wing)	min:0	s
# 2: Accept Radius	Acceptance radius (if the sphere with this radius is hit, the waypoint counts as reached)	min:0	m
# 3: Pass Radius	0 to pass through the WP, if > 0 radius to pass by WP. Positive value for clockwise orbit, negative value for counter-clockwise orbit. Allows trajectory control.		m
# 4: Yaw	Desired yaw angle at waypoint (rotary wing). NaN to use the current system yaw heading mode (e.g. yaw towards next waypoint, yaw to home, etc.).		deg
# 5: Latitude	Latitude		
# 6: Longitude	Longitude		
# 7: Altitude


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
  






"""
home = Locationwp().Set(-34.9805,117.8518,0, id)
to = Locationwp()
Locationwp.id.SetValue(to, int(MAVLink.MAV_CMD.TAKEOFF))
Locationwp.p1.SetValue(to, 15)
Locationwp.alt.SetValue(to, 50)

new_waypoint = Locationwp()
Locationwp.id.SetValue(new_waypoint, int(MAVLink.MAV_CMD.WAYPOINT))
Locationwp.alt.SetValue(new_waypoint, 20 )
Locationwp.lng.SetValue(new_waypoint,30)
Locationwp.lat.SetValue(new_waypoint,50)

landing_waypoint= Locationwp()
Locationwp.id.SetValue(landing_waypoint, int(MAVLink.MAV_CMD.LAND))
Locationwp.alt.SetValue(landing_waypoint, 0)
Locationwp.lng.SetValue(landing_waypoint, 10)
Locationwp.lat.SetValue(landing_waypoint, 10)

wp1 = Locationwp().Set(-35,117.8,50, id)
wp2 = Locationwp().Set(-35,117.89,50, id)
wp3 = Locationwp().Set(-35,117.85,20, id)


print(vars(Locationwp))


print ("set wp total")
"""
time.sleep(4)
#lat1=43.4341
#long1=-80.5791
#lat2=43.4342
#long2=-80.5792
waypoints = [(lat1, long1), (lat2, long2)]
print(len(waypoints)+3)
MAV.setWPTotal(len(waypoints) + 3)


#current_longitude=5
#current_longitude=7

cs = MissionPlanner.CurrentState


current_latitude= cs.lat
current_longitude=cs.lng

print(current_latitude)
print(current_longitude)


index = 0
takeoff = create_command(MAVLink.MAV_CMD.TAKEOFF, current_latitude, current_longitude)
MAV.setWP(takeoff, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
index += 1
takeoff = create_command(MAVLink.MAV_CMD.TAKEOFF, current_latitude, current_longitude)
MAV.setWP(takeoff, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
index +=1

mav_waypoint = create_command(MAVLink.MAV_CMD.WAYPOINT, 0, 0)
MAV.setWP(mav_waypoint, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
index += 1


for waypoint in waypoints:
    lat = waypoint[0]
    lng = waypoint[1]
    print("lat: "+ str(lat) + ",    lng: " + str(lng))
    mav_waypoint = create_command(MAVLink.MAV_CMD.WAYPOINT, lat, lng)
    MAV.setWP(mav_waypoint, index, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
    print(index)
    index += 1
"""
MAV.setWPTotal(len(waypoints)) # might need to add +3?
print ("upload home - reset on arm")
MAV.setWP(home,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload to")
MAV.setWP(to,1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload wp1")
MAV.setWP(new_waypoint, 2, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print("upload new_waypoint")
MAV.setWP(wp1,3,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload wp2")
MAV.setWP(wp2,4,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload wp3")
MAV.setWP(wp3,5,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("final ack")
MAV.setWP(landing_waypoint,6,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print ("upload landing waypoint")
"""

mav_waypoint = create_command(MAVLink.MAV_CMD.RETURN_TO_LAUNCH)
MAV.setWP(mav_waypoint, index, MAVLink.MAV_FRAME.MISSION)

MAV.setWPACK()

print ("done")
