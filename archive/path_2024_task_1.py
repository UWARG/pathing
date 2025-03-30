"""
Task 1 path. Uploads mission to run a maximum number of laps and monitors the mission for early landing.
"""

import pathlib
import time

from modules import condition_evaluator
from modules import load_waypoint_name_to_coordinates_map
from modules import mission_time_condition
from modules import waypoints_dict_to_list
from modules import waypoints_to_commands
from modules import waypoints_to_spline_commands
from modules import generate_command
from modules import add_takeoff_and_rtl_command
from modules import upload_commands
from modules.common.modules.mavlink import dronekit


TAKEOFF_WAYPOINT_FILE_PATH = pathlib.Path("2024", "waypoints", "takeoff_waypoint_task_1.csv")
LAP_WAYPOINTS_FILE_PATH = pathlib.Path("2024", "waypoints", "lap_waypoints_task_1.csv")
CONNECTION_ADDRESS = "tcp:localhost:14550"
PRINT_FREQUENCY = 30  # seconds
MAXIMUM_FLIGHT_TIME = 1800  # in seconds
TAKEOFF_ALTITUDE = 0  # metres
ALPHA_WAYPOINT_ALTITUDE = 100  # metres
MISSION_WAIT_ALTITUDE_THRESHOLD = 5  # metres
LAP_WAYPOINT_ALTITUDE = 20  # metres
DRONE_TIMEOUT = 30.0  # seconds
MISSION_WAIT_TIMEOUT = 5.0  # seconds
LAP_START_SEQUENCE_NUMBER = 3
MAXIMUM_NUMBER_OF_LAPS = 4


def main() -> int:
    """
    Main function.
    """
    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready=False)

    # Create waypoint name to coordinate dictionary for takeoff waypoint
    (
        result,
        takeoff_waypoint_dictionary,
    ) = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
        TAKEOFF_WAYPOINT_FILE_PATH,
    )
    if not result:
        print("ERROR: Load takeoff waypoint to coordinates map")
        return -1

    # Convert named waypoint dictionary to list
    result, waypoint_takeoff_list = waypoints_dict_to_list.waypoints_dict_to_list(
        takeoff_waypoint_dictionary,
    )
    if not result:
        print("ERROR: Convert takeoff waypoint dictionary to list")
        return -1

    # Create waypoint name to coordinate dictionary for lap waypoints
    (
        result,
        lap_waypoint_dictionary,
    ) = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
        LAP_WAYPOINTS_FILE_PATH,
    )
    if not result:
        print("ERROR: Load lap waypoints to coordinates map")
        return -1

    # Convert lap waypoint dictionary to list
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

    (
        result,
        lap_spline_waypoint_commands,
    ) = waypoints_to_spline_commands.waypoints_to_spline_commands(
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
    waypoint_commands.insert(len(waypoint_commands), do_jump_command)

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
        print("ERROR: upload_commands")
        return -1

    print("Upload successful, waiting for takeoff ...")

    # Wait for the drone to takeoff
    location_info = drone.location
    while location_info.global_relative_frame.alt < MISSION_WAIT_ALTITUDE_THRESHOLD:
        location_info = drone.location
        time.sleep(MISSION_WAIT_TIMEOUT)

    start_time = time.time()
    result, time_condition = mission_time_condition.MissionTimeCondition.create(
        start_time, MAXIMUM_FLIGHT_TIME
    )

    if not result:
        print("ERROR: Mission time condition")
        return -1

    return_to_launch_evaluator = condition_evaluator.ConditionEvaluator([time_condition])
    should_return_to_launch = False
    starting_lap = True
    lap_start_time, lap_end_time = 0, 0
    lap_counter = 0

    while True:
        # Time how long it takes for the drone to fly a lap and decide if there is enough time to fly another lap
        if drone.commands.next == LAP_START_SEQUENCE_NUMBER:
            if starting_lap:
                if lap_start_time == 0:
                    # Record the start time when running a new lap
                    lap_start_time = time.time()
                    lap_counter += 1

                    # Log lap and time data
                    print("\n--------------------------------------------------------")
                    print(f"Starting lap {lap_counter}")
                    print("--------------------------------------------------------")
                    time_condition.output_time_elapsed(PRINT_FREQUENCY)

                    # Disable flag since starting lap time is recorded
                    starting_lap = False
                else:
                    # Calculate lap time
                    lap_end_time = time.time()
                    lap_time = lap_end_time - lap_start_time

                    # Log lap and time data
                    time_condition.output_time_elapsed(PRINT_FREQUENCY)
                    print("--------------------------------------------------------")
                    print(f"Lap {lap_counter} start time (s): {lap_start_time}")
                    print(f"Lap {lap_counter} end time (s): {lap_end_time}")
                    print(f"Lap {lap_counter} time (s): {lap_time}")
                    print(f"Maximum flight time (s): {MAXIMUM_FLIGHT_TIME}")
                    print(
                        f"Estimated finish time of next lap (s): {(time.time() - start_time) + lap_time}"
                    )
                    print("--------------------------------------------------------")

                    # Update lap time and decided to continue or force early RTL
                    time_condition.update_lap_time(lap_time)
                    should_return_to_launch = return_to_launch_evaluator.evaluate_all_conditions()

                    # Reset lap start time and end time
                    lap_start_time, lap_end_time = 0, 0
            else:
                # Log time data
                time_condition.output_time_elapsed(PRINT_FREQUENCY)
        else:
            # Log time data
            time_condition.output_time_elapsed(PRINT_FREQUENCY)
            # Enable flag so when lap start waypoint is reached again, lap time can be calculated
            starting_lap = True

        if should_return_to_launch:
            break

    # Force early RTL
    drone.mode = dronekit.VehicleMode("RTL")
    rtl_command = generate_command.return_to_launch()
    result = upload_commands.upload_commands(
        drone,
        [rtl_command],
        DRONE_TIMEOUT,
    )
    if not result:
        print("ERROR: Failed to upload RTL command. Manually set RTL.")

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
