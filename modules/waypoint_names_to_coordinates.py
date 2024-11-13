"""
This file contains a function for converting waypoint names to coordinates.
"""

from .common.modules import location_global


def waypoint_names_to_coordinates(
    waypoint_names: list[str],
    waypoint_mapping: dict[str, location_global.LocationGlobal],
) -> tuple[True, list[location_global.LocationGlobal]] | tuple[False, None]:
    """
    Converts a list of waypoint names to their corresponding coordinates based on a waypoint mapping.

    waypoint_names: A list of waypoint names.
    waypoint_mapping: A dictionary mapping waypoint names to their corresponding coordinates.

    Return: Success, list of named coordinates.
    """
    # Handle the case when waypoint_names is empty
    if len(waypoint_names) == 0:
        return False, None

    coordinates = []
    for name in waypoint_names:
        if name in waypoint_mapping:
            coordinate = waypoint_mapping[name]
            coordinates.append(coordinate)
        else:
            return False, None

    return True, coordinates
