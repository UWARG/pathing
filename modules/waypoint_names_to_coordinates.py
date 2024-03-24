"""
This file contains a function for converting waypoint names to coordinates.
"""

from .common.kml.modules import location_ground


def waypoint_names_to_coordinates(
    waypoint_names: "list[str]", waypoint_mapping: "dict[str, location_ground.LocationGround]"
) -> "tuple[bool, list[location_ground.LocationGround]]":
    """
    Converts a list of waypoint names to their corresponding coordinates based on a waypoint mapping.

    Args:
        waypoint_names (list[str]): A list of waypoint names.
        waypoint_mapping (dict[str, LocationGround]): A dictionary mapping waypoint names to their
            corresponding LocationGround objects with coordinates.

    Returns:
        tuple[bool, list[LocationGround]]: A tuple containing a boolean indicating the success of the conversion
            and a list of LocationGround objects with coordinates corresponding to the given waypoint names.
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
