"""
Task 1 path. Uploads mission to run a maximum number of laps and monitors the mission for early landing.
"""

import pathlib
import time

import dronekit

from modules import condition_evaluator
from modules import load_waypoint_name_to_coordinates_map
from modules import mission_time_condition
from modules import waypoints_dict_to_list
from modules import waypoints_to_commands
from modules import waypoints_to_spline_commands
from modules import generate_command
from modules import add_takeoff_and_rtl_command
from modules import upload_commands


TAKEOFF_WAYPOINT_FILE_PATH = pathlib.Path("2024", "waypoints", "takeoff_waypoint_task_1.csv")
LAP_WAYPOINTS_FILE_PATH = pathlib.Path("2024", "waypoints", "lap_waypoints_task_1.csv")
CONNECTION_ADDRESS = "tcp:localhost:14550"
DELAY = 0.1  # seconds
MAXIMUM_FLIGHT_TIME = 1800  # in seconds
TAKEOFF_ALTITUDE = 10  # metres
ALPHA_WAYPOINT_ALTITUDE = 100  # metres
LAP_WAYPOINT_ALTITUDE = 50  # metres
DRONE_TIMEOUT = 30.0  # seconds
LAP_START_SEQUENCE_NUMBER = 3
MAXIMUM_NUMBER_OF_LAPS = 2


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
        print("ERROR: Load takeoff waypoint to coordinates map")
        return -1

    # Convert named waypoint dictionary to list
    # TODO: In progress
    # pylint: disable-next=unused-variable
    result, waypoint_takeoff_list = waypoints_dict_to_list.waypoints_dict_to_list(
        takeoff_waypoint_dictionary,
    )
    if not result:
        print("ERROR: Convert takeoff waypoint dictionary to list")
        return -1

    # Create waypoint name to coordinate dictionary for lap waypoints
    result, lap_waypoint_dictionary = (
        load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
            LAP_WAYPOINTS_FILE_PATH,
        )
    )
    if not result:
        print("ERROR: Load lap waypoints to coordinates map")
        return -1

    # Convert lap waypoint dictionary to list
    # TODO: In progress
    # pylint: disable-next=unused-variable
    result, lap_waypoint_list = waypoints_dict_to_list.waypoints_dict_to_list(
        lap_waypoint_dictionary,
    )
    if not result:
        print("ERROR: Convert lap waypoints dictionary to list")
        return -1

    result, takeoff_waypoint_command = waypoints_to_commands.waypoints_to_commands(
        waypoint_takeoff_list,
        ALPHA_WAYPOINT_ALTITUDE,
    )
    if not result:
        print("ERROR: takeoff waypoint to command")
        return -1

    result, lap_spline_waypoint_commands = waypoints_to_spline_commands.waypoints_to_spline_commands(
        lap_waypoint_list,
        LAP_WAYPOINT_ALTITUDE,
    )

    # Subtract `MAXIMUM_NUMBER_OF_LAPS` by 1 to account for the first lap the drone makes
    do_jump_command = generate_command.do_jump(
        LAP_START_SEQUENCE_NUMBER,
        MAXIMUM_NUMBER_OF_LAPS - 1,
    )

    # Assemble the drone's path
    waypoint_commands = []
    waypoint_commands.extend(takeoff_waypoint_command)
    waypoint_commands.extend(lap_spline_waypoint_commands)
    waypoint_commands.insert(-1, do_jump_command)

    result, takeoff_and_rtl_commands = add_takeoff_and_rtl_command.add_takeoff_and_rtl_command(
        waypoint_commands,
        TAKEOFF_ALTITUDE,
    ) 

    result = upload_commands.upload_commands(
        drone,
        takeoff_and_rtl_commands,
        DRONE_TIMEOUT,
    )
    if not result:
        print("Error: upload_commands")
        return -1

    start_time = time.time()
    result, time_condition = mission_time_condition.MissionTimeCondition.create(
        start_time, MAXIMUM_FLIGHT_TIME
    )

    if not result:
        print("Error: Mission time condition")
        return -1

    return_to_launch_evaluator = condition_evaluator.ConditionEvaluator([time_condition])

    while True:
        # Send drone back to launch if exceeds time limit

        should_return_to_launch = return_to_launch_evaluator.evaluate_all_conditions()
        if should_return_to_launch:
            break

        time_condition.output_time_elapsed()

        time.sleep(DELAY)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
