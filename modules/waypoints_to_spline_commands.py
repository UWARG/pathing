"""
Function to convert list of waypoints to a list of spline waypoint dronekit commands.
"""

import dronekit
from modules.common.comms.modules.TelemMessages.Waypoint import Waypoint


MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_SPLINE_WAYPOINT
ACCEPTANCE_RADIUS = 10


def waypoints_to_spline_commands(waypoints: "Waypoint") -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Convert list of waypoints to a list of spline waypoint dronekit commands.

    Parameters
    ----------
    waypoints: Waypoint
        waypoint coordinates in decimal degrees (latitude, longitude).

    Returns
    -------
    tuple[bool, list[dronekit.Command] | None]: 
        (False, None) if empty waypoints list,
        (True, dronekit commands that can be sent to the drone) otherwise dronekit commands that can be sent to the drone.
    """
    if len(waypoints) == 0:
        return False, None

    dronekit_command_list = []

    for waypoint in waypoints:
        lat = waypoint.latitude
        lng = waypoint.longtitude
        command = dronekit.Command(
            0,
            0,
            0,
            MAVLINK_FRAME,
            MAVLINK_COMMAND,
            0,
            0,
            0,  # param1
            ACCEPTANCE_RADIUS,
            0,
            0,
            lat,
            lng,
            waypoint.altitude,
        )
        dronekit_command_list.append(command)

    return True, dronekit_command_list
