"""
Function to convert list of waypoints to dronekit commands
"""

import dronekit

from modules.waypoint import Waypoint


MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
ACCEPT_RADIUS = 10


def waypoints_to_commands(waypoints: "list[Waypoint]",
                          altitude: int) -> "list[dronekit.Command]":
    """
    Convert list of waypoints to dronekit commands.

    Parameters
    ----------
    waypoints: list[Waypoint]
        List of Waypoint objects.
    altitude: int
        altitude in meters to command the drone to.

    Returns
    -------
    list[dronekit.Command]
        dronekit commands that can be sent to the drone.
    """
    dronekit_command_list = []

    for waypoint in waypoints:
        lat = waypoint.latitude
        lng = waypoint.longitude
        command = dronekit.Command(
            0,
            0,
            0,
            MAVLINK_FRAME,
            MAVLINK_COMMAND,
            0,
            0,
            0,  # param1
            ACCEPT_RADIUS,
            0,
            0,
            lat,
            lng,
            altitude,
        )
        dronekit_command_list.append(command)

    return dronekit_command_list
