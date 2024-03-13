"""
Test the drone stop condition.
"""
import sys
import time

from modules import add_takeoff_and_landing_command
from modules import check_time_condition
from modules import multiple_evaluator
from modules import upload_commands
from modules import waypoints_to_commands
from modules.common.kml.modules import location_ground
from modules.common.mavlink.modules import flight_controller


MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
MAXIMUM_FLIGHT_TIME = 5  # seconds (for testing purposes)

ALTITUDE = 50  # metres
DELAY = 1  # seconds


if __name__ == "__main__":
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("Unable to connect to Mission Planner.")
        sys.exit()

    # Get Pylance to stop complaining
    assert controller is not None

    # Upload mission with a single waypoint
    test_waypoint = location_ground.Location_ground("Test", 43.4731, -80.5419)
    result, test_waypoint_commands = waypoints_to_commands.waypoints_to_commands([test_waypoint], ALTITUDE)
    if not result:
        print("Unable to create waypoint commands.")
        sys.exit()
    
    result, commands_with_takeoff_landing = add_takeoff_and_landing_command.add_takeoff_and_landing_command(test_waypoint_commands, ALTITUDE)
    if not result:
        print("Unable to add takeoff and landing commands.")
        sys.exit()

    result = upload_commands.upload_commands(controller.drone, commands_with_takeoff_landing)
    if not result:
        print("Unable to upload commands.")
        sys.exit()

    # Loop mimics path_2024.py structure
    start_time = time.time()
    time_limit_evaluator = check_time_condition.CheckTimeCondition(start_time,MAXIMUM_FLIGHT_TIME)
    returning_to_launch_evaluator = multiple_evaluator.MultipleEvaluator([time_limit_evaluator])
    while True:
        # Check whether drone exceeds max flight time
        current_time = time.time()
        is_returning_to_launch = returning_to_launch_evaluator.evaluate_all()
        if is_returning_to_launch:   
            break

        time_limit_evaluator.output_time_elapsed()

        time.sleep(DELAY)

    print("Done!")
