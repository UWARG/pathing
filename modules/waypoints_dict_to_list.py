"""
Module to convert waypoints dict to waypoints list.
"""

from . import waypoint
from .common.kml.modules import location_ground


def waypoints_dict_to_list(
    waypoint_name_to_coordinates: "dict[str, location_ground.LocationGround]",
) -> "tuple[bool, list[location_ground.LocationGround]]":
    """
    Converts dictionary of waypoints into a list.

    Parameters
    ----------
    waypoint_name_to_coordinates: dict[str, LocationGround]
        Waypoint mapping of name to (latitude, longitude).

    Returns
    -------
    bool: Whether waypoint data conversion was a success.
    list[Waypoint]: List of the waypoint coordinates.
    """
    # Check for empty input dictionary
    if len(waypoint_name_to_coordinates) == 0:
        return False, None

    # Create list of all the values in the input dictionary, ie. the LocationGround
    waypoints_list = list(waypoint_name_to_coordinates.values())

    return True, waypoints_list


def waypoints_dict_with_altitude_to_list(
    waypoint_name_to_coordinates_and_altitude: "dict[str, waypoint.Waypoint]",
) -> "tuple[bool, list[waypoint.Waypoint]]":
    """
    Converts dictionary of waypoints into a list.

    Parameters
    ----------
    waypoint_name_to_coordinates_and_altitude: dict[str, LocationGroundAndAltitude]
        Waypoint mapping of name to (latitude, longitude, altitude).

    Returns
    -------
    bool: Whether waypoint data conversion was a success.
    list[Waypoint]: List of the waypoint coordinates and altitude.
    """
    # Check for empty input dictionary
    if len(waypoint_name_to_coordinates_and_altitude) == 0:
        return False, None

    # Create list of all the values in the input dictionary, ie. the LocationGround
    waypoints_list = list(waypoint_name_to_coordinates_and_altitude.values())

    return True, waypoints_list
