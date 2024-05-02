"""
Function to convert list of waypoints a list of spline waypoint dronekit commands.
"""

import dronekit

from . import generate_command
from .common.kml.modules import location_ground


def waypoints_to_spline_commands(
    waypoints: "list[location_ground.LocationGround]", altitude: float
) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Convert list of waypoints to a list of spline waypoint dronekit commands.
    Spline waypoint dronekit commands fly to the target waypoint following a spline path
    (a path that curves around a waypoint).

    Parameters
    ----------
    waypoints: list[LocationGround]
        list of locationGround objects containing names and coordinates in decimal degrees.
    altitude: float
        altitude in meters to command the drone to.

    Returns
    -------
    tuple[bool, list[dronekit.Command] | None]:
        (False, None) if empty waypoints list,
        (True, list of spline waypoint commands) if waypoints list is not empty.
    """
    if len(waypoints) == 0:
        return False, None

    dronekit_spline_command_list = []

    for waypoint in waypoints:
        command = generate_command.waypoint_spline(
            0.0, waypoint.latitude, waypoint.longitude, altitude
        )
        dronekit_spline_command_list.append(command)

    return True, dronekit_spline_command_list
