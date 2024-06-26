"""
Test the drone stop condition.
"""

import time

from modules import add_takeoff_and_landing_command
from modules import condition_evaluator
from modules import mission_time_condition
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

    (
        result,
        commands_with_takeoff_landing,
    ) = add_takeoff_and_landing_command.add_takeoff_and_landing_command(
        test_waypoint_commands, ALTITUDE
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
    success, check_time_condition = mission_time_condition.MissionTimeCondition.create(
        start_time, MAXIMUM_FLIGHT_TIME
    )
    if not success:
        print("Unable to create the MissionTimeCondition object.")
        return -1

    return_to_launch_evaluator = condition_evaluator.ConditionEvaluator([check_time_condition])

    while True:
        # Check whether drone exceeds max flight time
        should_return_to_launch = return_to_launch_evaluator.evaluate_all_conditions()
        if should_return_to_launch:
            break

        check_time_condition.output_time_elapsed(30)

        time.sleep(DELAY)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
