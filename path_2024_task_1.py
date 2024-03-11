"""
Task 1 path.
"""
import pathlib

import dronekit

from modules import load_waypoint_name_to_coordinates_map
from modules import waypoints_dict_to_list


WAYPOINT_NAMES_FILE_PATH = pathlib.Path("2024", "waypoints", "waypoint_task_1.csv")
LAP_WAYPOINT_FILE_PATH = pathlib.Path("2024", "waypoints", "lap_waypoint_task_1.csv")
CONNECTION_ADDRESS = "tcp:localhost:14550"


# Required for checks
# pylint: disable-next=too-many-return-statements
def run() -> int:
    """
    Uploads mission to run a maximum number of laps and monitors the mission for early landing.
    """
    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready=False)

    # Create waypoint name to coordinate dictionary for named waypoints
    result, waypoint_names_dictionary = \
        load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
            WAYPOINT_NAMES_FILE_PATH,
        )
    if not result:
        print("ERROR: Load waypoint to coordinates map")
        return -1

    # Convert named waypoint dictionary to list
    result, waypoint_names_list = \
        waypoints_dict_to_list.waypoints_dict_to_list(
            waypoint_names_dictionary,
        )
    if not result:
        print("ERROR: Convert waypoint dictionary to list")
        return -1

    # Create waypoint name to coordinate dictionary for lap waypoints
    result, lap_waypoint_dictionary = \
        load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
            LAP_WAYPOINT_FILE_PATH,
        )
    if not result:
        print("ERROR: Load waypoint to coordinates map")
        return -1

    # Convert lap waypoint dictionary to list
    result, lap_waypoint_list = \
        waypoints_dict_to_list.waypoints_dict_to_list(
            lap_waypoint_dictionary,
        )
    if not result:
        print("ERROR: Convert waypoint dictionary to list")
        return -1

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    result_run = run()
    if result_run < 0:
        print("ERROR")

    print("Done")
