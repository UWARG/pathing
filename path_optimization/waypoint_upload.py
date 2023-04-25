from pymavlink import mavutil

waypoints= [(latitude1, longitude1), (latitude2, longitude2)]#List of tuples containing waypoints with corresponding latitude and longitude values

#connect to autopilot using MAVlink protocol 

master= mavutil.mavlink_connection('udp:127.0.0.1:14550')

#clearing any existing waypoints

master.mav.mission_clear-all_send()

#iterating through waypoints and uplaoding them

for i, waypoint in enumerate(waypoints):
    # create a mavlink message for the waypoint 

    msg= mavutil.mavlink.MAVLink_mission_item_message(
        0,
        0,
        i, #sequence number 
        16, #frame type 
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        #following parameters with value of zero is not used (not applicable to this application)
        0,
        0,
        0,
        0,
        0,
        0,

        waypoint[0], #latitude
        waypoint[1], # longitude
        0) #altitude is not used 

    #send the MAVlink message  to the autopilot

    master.mav.send(msg)

    #send a message to indicate that mission upload is complete
    master.mav.mission_ack_send(0, mavutil.mavlink.MAV_MISSION_RESULT_ACCEPTED)
    

