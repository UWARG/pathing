"""
Module to convert waypoints dict to waypoints list.
"""

from .common.modules import location_global
from .common.modules import position_global_relative_altitude


def waypoints_dict_to_list(
    waypoint_name_to_coordinates: dict[str, location_global.LocationGlobal],
) -> tuple[True, list[location_global.LocationGlobal]] | tuple[False, None]:
    """
    Converts dictionary of waypoints into a list.

    waypoint_name_to_coordinates: Waypoint mapping of name to coordinate.

    Return: Success, list of coordinates.
    """
    # Check for empty input dictionary
    if len(waypoint_name_to_coordinates) == 0:
        return False, None

    # Create list of all the values in the input dictionary
    waypoints_list = list(waypoint_name_to_coordinates.values())

    return True, waypoints_list


def waypoints_dict_with_altitude_to_list(
    waypoint_name_to_coordinates_and_altitude: dict[
        str, position_global_relative_altitude.PositionGlobalRelativeAltitude
    ],
) -> (
    tuple[True, list[position_global_relative_altitude.PositionGlobalRelativeAltitude]]
    | tuple[False, None]
):
    """
    Converts dictionary of waypoints into a list.

    waypoint_name_to_coordinates: Waypoint mapping of name to coordinate.

    Return: Success, list of coordinates.
    """
    # Check for empty input dictionary
    if len(waypoint_name_to_coordinates_and_altitude) == 0:
        return False, None

    # Create list of all the values in the input dictionary, ie. the LocationGround
    waypoints_list = list(waypoint_name_to_coordinates_and_altitude.values())

    return True, waypoints_list
