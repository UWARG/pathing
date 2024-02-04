"""
Test the drone stop condition
"""

import dronekit
import sys
import time

from modules import check_stop_condition
from modules.common.mavlink.modules import flight_controller

MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
MAVLINK_LANDING_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_LANDING_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH
MAVLINK_TAKEOFF_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_TAKEOFF_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT

MAXIMUM_FLIGHT_TIME = 5  # seconds (for testing purposes)

ALTITUDE = 10
ACCEPT_RADIUS = 10


def upload_intial_mission(
        waypoint: "tuple[float, float, float]",
        controller: "flight_controller.FlightController",
) -> bool:
    """
    Add initial mission to drone.
    """
    # Clear existing mission
    controller.drone.commands.download()
    controller.drone.commands.wait_ready()
    controller.drone.commands.clear()

    # Add takeoff command to the mission
    takeoff_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_TAKEOFF_FRAME,
        MAVLINK_TAKEOFF_COMMAND,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        ALTITUDE,
    )

    # Add waypoint to the mission
    waypoint_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_FRAME,
        MAVLINK_COMMAND,
        0,
        0,
        0,
        ACCEPT_RADIUS,
        0,
        0,
        waypoint[0],
        waypoint[1],
        waypoint[2],
    )

    # Add both commands to mission
    controller.drone.commands.add(takeoff_command)
    controller.drone.commands.add(waypoint_command)

    # Upload the mission to the drone
    controller.drone.commands.upload()



if __name__ == "__main__":
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("failed")
        sys.exit()

    # Get Pylance to stop complaining
    assert controller is not None

    # Set the home location of the drone to E5
    # Set extra command line to `--home=43.472978,-80.540103,336,0`
    waypoint = (43.4731, -80.5419, ALTITUDE)

    # Upload Mission
    upload_intial_mission(waypoint, controller)

    # loop mimicks path_2024 structure
    start_time = time.time()
    while True:
        time.sleep(1)
        
        # check whether drone exceeds max flight time
        current_time = time.time()
        has_exceeded_max_time = check_stop_condition.check_stop_condition(start_time, current_time, controller.drone, MAXIMUM_FLIGHT_TIME)
        if has_exceeded_max_time:   
            break

    print("Done")
