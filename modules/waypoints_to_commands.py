"""
Function to convert list of waypoints to dronekit commands.
"""

import dronekit

from . import generate_command, location_ground_and_altitude
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
        list of LocationGround objects containing names and coordinates in decimal degrees.
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

def waypoints_with_altitude_to_commands(
    waypoints: "list[location_ground_and_altitude.LocationGroundAndAltitude]",
) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Convert list of waypoints to dronekit commands.

    Parameters
    ----------
    waypoints: list[LocationGroundAndAltitude]
        list of LocationGroundAndAltitude objects containing names, coordinates in decimal degrees, and altitude in metres.

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
            0.0, ACCEPT_RADIUS, point.location_ground.latitude, point.location_ground.longitude, point.altitude
        )

        dronekit_command_list.append(command)

    return True, dronekit_command_list