"""
Function to create new route around diversion
"""

import dronekit

from . import waypoints_to_commands
from .common.kml.modules import location_ground
from . import diversion_waypoints_from_vertices


def add_takeoff_and_landing_command(
    location: "tuple[float, float]",
    diversion_waypoints: "list[location_ground.LocationGround]",
    rejoin_waypoint: "location_ground.LocationGround",
    altitude: float,
) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Converts a list of waypoint around diversion area and rejoin waypoint to a list of dronekit commands.

    Parameters
    ----------
    location: tuple[float, float]:
        latitude and longitude coordinate of current location

    diversion_waypoints: list[LocationGround]
        list of locationGround objects containing names and coordinates in decimal degrees.

    rejoin_waypoints: [LocationGround]
        locationGround object containing name and coordinate in decimal degrees

    altitude: float
        altitude in meters to command the drone to.

    Returns
    -------
    tuple[bool, list[dronekit.Command] | None]:
        (False, None) if empty diversion_waypoint list, return false if no new route needs to be created (balanji's function is empty)
        (True, dronekit commands with takeoff and land commands that can be sent to the drone) otherwise.
    """

    if len(diversion_waypoints) == 0:
        return False, None

    # call balanji's function (output is a list), check if list is empty
    # already appends current location and rejoin waypoint...
    diversion_waypoints_path: "list[location_ground.LocationGround]" = (
        diversion_waypoints_from_vertices(location, rejoin_waypoint, diversion_waypoints)
    )

    result, dronekit_command_list = waypoints_to_commands(diversion_waypoints, altitude)

    return True, dronekit_command_list
