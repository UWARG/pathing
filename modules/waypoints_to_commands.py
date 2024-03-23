"""
Function to convert list of waypoints to dronekit commands.
"""

import dronekit

from . import generate_command
from .common.kml.modules import location_ground


ACCEPT_RADIUS = 10.0  # metres


def waypoints_to_commands(
    waypoints: "list[location_ground.LocationGround]", altitude: float
) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Convert list of waypoints to dronekit commands.

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
        (True, dronekit commands that can be sent to the drone) otherwise.
    """
    if len(waypoints) == 0:
        return False, None

    dronekit_command_list = []

    for point in waypoints:
        command = generate_command.waypoint(
            0.0, ACCEPT_RADIUS, point.latitude, point.longitude, altitude
        )

        dronekit_command_list.append(command)

    return True, dronekit_command_list
