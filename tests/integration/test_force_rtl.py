"""
Test to check if return to launch (RTL) works as intended.
"""

import time

from pymavlink import mavutil

from modules import force_rtl
from modules.common.modules.mavlink import dronekit
from modules.common.modules.mavlink import flight_controller


DELAY_TIME = 30.0  # seconds
MISSION_PLANNER_ADDRESS = "tcp:127.0.0.1:14550"
TIMEOUT = 1.0  # seconds

MAVLINK_TAKEOFF_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_TAKEOFF_COMMAND = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT

ALTITUDE = 10  # metres
ACCEPT_RADIUS = 10  # metres


# TODO: This function is to be removed when Dronekit-Python interfaces are
# moved from pathing repository.
def upload_mission(
    controller: flight_controller.FlightController, waypoints: "list[tuple[float, float, float]]"
) -> bool:
    """
    Add a takeoff command and waypoint following commands to the drone's
    command sequence, and upload them.

    controller: Flight controller.
    waypoints: Latitude (decimal degrees), longitude (decimal degrees), and altitude (metres).

    Return: If the mission is successfully uploaded or not.
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

    controller.drone.commands.add(takeoff_command)

    # Add waypoints to the mission
    for point in waypoints:
        command = dronekit.Command(
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
            point[0],
            point[1],
            point[2],
        )

        controller.drone.commands.add(command)

    # Upload the mission to the drone
    try:
        controller.drone.commands.upload()
        return True
    except dronekit.TimeoutError:
        return False


def main() -> int:
    """
    Main function.
    """
    result, controller = flight_controller.FlightController.create(MISSION_PLANNER_ADDRESS)
    if not result:
        print("Failed to create flight controller.")
        return -1

    # Get Pylance to stop complaining
    assert controller is not None

    # List of waypoints for the drone to travel
    waypoints = [
        (43.4731, -80.5419, ALTITUDE),
        (43.4723, -80.5380, ALTITUDE),
        (43.4735, -80.5371, ALTITUDE),
        (43.4743, -80.5400, ALTITUDE),
    ]

    # Upload mission
    result = upload_mission(controller, waypoints)
    if not result:
        print("Failed to upload mission.")
        return -1

    # Delay for one minute
    time.sleep(DELAY_TIME)

    # Force drone to return to launch (RTL)
    result = force_rtl.force_rtl(controller)

    if not result:
        print("Drone failed during return to launch sequence.")
        return -1

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
