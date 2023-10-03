"""
Task 1 path.
"""
import pathlib

import dronekit

from modules import add_takeoff_and_landing_command
from modules import load_waypoint_name_to_coordinates_map
from modules import qr_input
from modules import qr_to_waypoint_names
from modules import upload_commands
from modules import waypoint_names_to_coordinates
from modules import waypoints_to_commands


WAYPOINT_FILE_PATH = pathlib.Path(".", "waypoints", "wrestrc_waypoints.csv")
CAMERA = 0
ALTITUDE = 40
CONNECTION_ADDRESS = "tcp:localhost:14550"

def get_current_destination(drone):
    # Get the command sequence
    cmds = drone.commands
    cmds.download()
    cmds.wait_ready()

    # Get the current command index
    current_command_index = cmds.next

    if current_command_index < cmds.count:
        # Get the current command
        current_command = cmds[current_command_index]

        if current_command.command == dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT:
            # Extract latitude and longitude from the waypoint command
            latitude = current_command.x
            longitude = current_command.y
            print ("longitude, latitude: ", longitude, latitude)
            return latitude, longitude
        else:
            print("ERROR: Current command is not a waypoint command.")
    else:
        print("ERROR: No waypoints or current command index out of range.")

    return None, None
    

def run() -> int:
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready = True)

    current_latitude, current_longitude = get_current_destination(drone)
    
    if current_latitude is not None and current_longitude is not None:
        print("Current Destination Latitude:", current_latitude)
        print("Current Destination Longitude:", current_longitude)
    else:
        print("Unable to retrieve the current destination.")

    result, waypoint_name_to_coordinates = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(WAYPOINT_FILE_PATH)
    if not result:
        print("ERROR: load_waypoint_name_to_coordinates_map")
        return -1

    result, qr_text = qr_input.qr_input(CAMERA)
    if not result:
        print("ERROR: qr_input")
        return -1

    result, waypoint_names = qr_to_waypoint_names.qr_to_waypoint_names(qr_text)
    if not result:
        print("ERROR: qr_to_waypoint_names")
        return -1

    result, waypoints = waypoint_names_to_coordinates.waypoint_names_to_coordinates(waypoint_names, waypoint_name_to_coordinates)
    if not result:
        print("ERROR: waypoint_names_to_coordinates")
        return -1
    
    waypoint_commands = waypoints_to_commands.waypoints_to_commands(waypoints, ALTITUDE)
    if len(waypoint_commands) == 0:
        print("Error: waypoints_to_commands")
        return -1
    
    takeoff_landing_commands = add_takeoff_and_landing_command.add_takeoff_and_landing_command(waypoint_commands, ALTITUDE)
    if len(takeoff_landing_commands) == 0:
        print("Error: add_takeoff_and_landing_command")
        return -1
    
    result = upload_commands.upload_commands(drone, takeoff_landing_commands)
    if not result:
        print("Error: upload_commands")
        return -1
    
    return 0


if __name__ == "__main__":
    result_run = run()
    if result_run < 0:
        print("ERROR")
    print("Done")
