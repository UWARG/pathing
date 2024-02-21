"""
Path template.
"""
import pathlib
import time

import dronekit

from modules import add_takeoff_and_landing_command
from modules import check_stop_condition
from modules import load_waypoint_name_to_coordinates_map
from modules import upload_commands
from modules import waypoints_to_commands
from modules import waypoint_tracking
from modules import waypoints_dict_to_list
from modules.common.kml.modules import waypoints_to_kml


WAYPOINT_FILE_PATH = pathlib.Path("2024", "waypoints", "wrestrc.csv")
ALTITUDE = 40
CONNECTION_ADDRESS = "tcp:localhost:14550"
KML_FILE_PARENT_DIRECTORY = pathlib.Path("waypoints")
KML_FILE_PREFIX = "waypoints_log"
DELAY = 0.1  # seconds
MAXIMUM_FLIGHT_TIME = 1800  # seconds


# Required for checks
# pylint: disable-next=too-many-return-statements
def run() -> int:
    """
    Reads in hardcoded waypoints from CSV file and sends drone commands.
    """
    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready = False)

    # Read in hardcoded waypoints from CSV file
    # Waypoints are stored in order of insertion, starting with the top row
    result, waypoint_name_to_coordinates = \
        load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
            WAYPOINT_FILE_PATH,
        )
    if not result:
        print("ERROR: load_waypoint_name_to_coordinates_map")
        return -1

    result, waypoints_list = waypoints_dict_to_list.waypoints_dict_to_list(
        waypoint_name_to_coordinates
    )
    if not result:
        print("ERROR: Unable to convert waypoints from dict to list")
        return -1

    # TODO: Remove tuple conversion when common repository's waypoint_to_kml() supports Waypoint class
    waypoints_list_tuple = [(waypoint.latitude, waypoint.longitude) for waypoint in waypoints_list]
    result, _ = waypoints_to_kml.waypoints_to_kml(
        waypoints_list_tuple,
        KML_FILE_PREFIX, KML_FILE_PARENT_DIRECTORY,
    )
    if not result:
        print("ERROR: Unable to generate KML file")
        return -1

    result, waypoint_commands = waypoints_to_commands.waypoints_to_commands(
        waypoints_list,
        ALTITUDE,
    )
    if not result:
        print("Error: waypoints_to_commands")
        return -1

    result, takeoff_landing_commands = \
        add_takeoff_and_landing_command.add_takeoff_and_landing_command(
            waypoint_commands,
            ALTITUDE,
        )
    if not result:
        print("Error: add_takeoff_and_landing_command")
        return -1

    result = upload_commands.upload_commands(drone, takeoff_landing_commands)
    if not result:
        print("Error: upload_commands")
        return -1

    start_time = time.time()
    while True:
        result, waypoint_info = waypoint_tracking.get_current_waypoint_info(drone)
        if not result:
            print("Error: waypoint_tracking (waypoint_info)")
        else:
            print(f"Current waypoint sequence: {waypoint_info}")

        result, location = waypoint_tracking.get_current_location(drone)
        if not result:
            print("Error: waypoint_tracking (get_current_location)")
        else:
            print(f"Current location (Lat, Lon): {location}")
        
        # Send drone back to launch if exceeds time limit
        current_time = time.time()
        is_returning_to_launch = check_stop_condition.check_stop_condition(start_time, current_time, drone, MAXIMUM_FLIGHT_TIME)
        if is_returning_to_launch:   
            break
        
        print(f"Elapsed time (s): {current_time - start_time}")

        time.sleep(DELAY)

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    result_run = run()
    if result_run < 0:
        print("ERROR")

    print("Done")
