"""
Task 1 path. Uploads mission to run a maximum number of laps and monitors the mission for early landing.
Using the updated waypoint_to_spline_command
"""

import pathlib

import dronekit

from modules import load_waypoint_name_to_coordinates_map
from modules import waypoints_dict_to_list
from modules import waypoints_to_spline_commands


TAKEOFF_WAYPOINT_FILE_PATH = pathlib.Path("2024", "waypoints", "takeoff_waypoint_task_1")
LAP_WAYPOINTS_FILE_PATH = pathlib.Path("2024", "waypoints", "lap_waypoints_task_1.csv")
CONNECTION_ADDRESS = "tcp:localhost:14550"


def main() -> int:
    """
    Main function.
    """
    # Wait ready is false as the drone may be on the ground
    # TODO: In progress
    # pylint: disable-next=unused-variable
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready=False)

    # Create waypoint name to coordinate dictionary for takeoff waypoint
    result, takeoff_waypoint_dictionary = (
        load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
            TAKEOFF_WAYPOINT_FILE_PATH,
        )
    )
    if not result:
        print("ERROR: Load waypoint to coordinates map")
        return -1

    # Convert named waypoint dictionary to list
    # TODO: In progress
    # pylint: disable-next=unused-variable
    result, waypoint_takeoff_list = waypoints_dict_to_list.waypoints_dict_to_list(
        takeoff_waypoint_dictionary,
    )
    if not result:
        print("ERROR: Convert waypoint dictionary to list")
        return -1

    # Create waypoint name to coordinate dictionary for lap waypoints
    result, lap_waypoint_dictionary = (
        load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
            LAP_WAYPOINTS_FILE_PATH,
        )
    )
    if not result:
        print("ERROR: Load waypoint to coordinates map")
        return -1

    # Convert lap waypoint dictionary to list
    # TODO: In progress
    # pylint: disable-next=unused-variable
    result, lap_waypoint_list = waypoints_dict_to_list.waypoints_dict_to_list(
        lap_waypoint_dictionary,
    )
    if not result:
        print("ERROR: Convert waypoint dictionary to list")
        return -1

    result, waypoint_commands = waypoints_to_spline_commands.waypoints_to_spline_commands(
        lap_waypoint_list,
        ALTITUDE,
    )
    if not result:
        print("Error: waypoints_to_spline_commands")
        return -1

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
