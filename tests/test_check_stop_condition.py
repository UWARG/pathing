"""
Test the drone stop condition.
"""

import sys
import time

import dronekit

from modules import add_takeoff_and_landing_command
from modules import check_stop_condition
from modules import upload_commands
from modules import waypoint
from modules import waypoints_to_commands
from modules.common.mavlink.modules import flight_controller


MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
MAVLINK_TAKEOFF_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_TAKEOFF_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT

MAXIMUM_FLIGHT_TIME = 5  # seconds (for testing purposes)

ALTITUDE = 50
ACCEPT_RADIUS = 10


if __name__ == "__main__":
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("Unable to connect to Mission Planner.")
        sys.exit()

    # Get Pylance to stop complaining
    assert controller is not None

    # Upload mission with a single waypoint
    test_waypoint = waypoint.Waypoint("Test", 43.4731, -80.5419)
    result, test_waypoint_commands = waypoints_to_commands.waypoints_to_commands([test_waypoint], ALTITUDE)
    if not result:
        print("Unable to create waypoint commands.")
        sys.exit()
    
    result, takeoff_landing_commands = add_takeoff_and_landing_command.add_takeoff_and_landing_command(test_waypoint_commands, ALTITUDE)
    if not result:
        print("Unable to add takeoff and landing commands.")
        sys.exit()

    result = upload_commands.upload_commands(controller.drone, takeoff_landing_commands)
    if not result:
        print("Unable to upload commands.")
        sys.exit()

    # loop mimics path_2024.py structure
    start_time = time.time()
    while True:
        # Check whether drone exceeds max flight time
        current_time = time.time()
        is_returning_to_launch = check_stop_condition.check_stop_condition(start_time, current_time, controller.drone, MAXIMUM_FLIGHT_TIME)
        if is_returning_to_launch:   
            break
        print(f"Elapsed time (s): {current_time - start_time}")

        time.sleep(1)

    print("Done!")
