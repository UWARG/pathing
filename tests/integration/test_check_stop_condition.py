"""
Test the drone stop condition.
"""

import time

from modules import add_takeoff_and_landing_command
from modules import check_stop_condition
from modules import upload_commands
from modules import waypoints_to_commands
from modules.common.kml.modules import location_ground
from modules.common.mavlink.modules import flight_controller


MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
MAXIMUM_FLIGHT_TIME = 5  # seconds (for testing purposes)

ALTITUDE = 50  # metres
DRONE_TIMEOUT = 30.0  # seconds

DELAY = 1  # seconds


# No enable


def main() -> int:
    """
    Main function.
    """
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("Unable to connect to Mission Planner.")
        return -1

    # Get Pylance to stop complaining
    assert controller is not None

    # Upload mission with a single waypoint
    test_waypoint = location_ground.Location_ground("Test", 43.4731, -80.5419)
    result, test_waypoint_commands = waypoints_to_commands.waypoints_to_commands(
        [test_waypoint], ALTITUDE
    )
    if not result:
        print("Unable to create waypoint commands.")
        return -1

    result, commands_with_takeoff_landing = (
        add_takeoff_and_landing_command.add_takeoff_and_landing_command(
            test_waypoint_commands, ALTITUDE
        )
    )
    if not result:
        print("Unable to add takeoff and landing commands.")
        return -1

    result = upload_commands.upload_commands(
        controller.drone, commands_with_takeoff_landing, DRONE_TIMEOUT
    )
    if not result:
        print("Unable to upload commands.")
        return -1

    # Loop mimics path_2024.py structure
    start_time = time.time()
    while True:
        # Check whether drone exceeds max flight time
        current_time = time.time()
        is_returning_to_launch = check_stop_condition.check_stop_condition(
            start_time, current_time, controller.drone, MAXIMUM_FLIGHT_TIME
        )
        if is_returning_to_launch:
            break

        print(f"Elapsed time (s): {current_time - start_time}")

        time.sleep(DELAY)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
