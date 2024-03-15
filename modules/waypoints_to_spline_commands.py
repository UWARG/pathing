"""
Function to convert list of waypoints a list of spline waypoint dronekit commands.
"""

import dronekit

from .common.kml.modules import location_ground


MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_SPLINE_WAYPOINT
ACCEPT_RADIUS = 10


def waypoints_to_spline_commands(waypoints: "list[location_ground.LocationGround]",
                                 altitude: int) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Convert list of waypoints to a list of spline waypoint dronekit commands.

    Parameters
    ----------
    waypoints: list[LocationGround]
        list of locationGround objects containing names and coordinates in decimal degrees.
    altitude: int
        altitude in meters to command the drone to.

    Returns
    -------
    tuple[bool, list[dronekit.Command] | None]: 
        (False, None) if empty waypoints list,
        (True, spline waypoint dronekit commands that can be sent to the drone) otherwise spline waypoint dronekit commands that can be sent to the drone.
    """
    if len(waypoints) == 0:
        return False, None

    dronekit_spline_command_list = []

    for point in waypoints:
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
            point.latitude,
            point.longitude,
            altitude,
        )
        dronekit_spline_command_list.append(command)

    return True, dronekit_spline_command_list