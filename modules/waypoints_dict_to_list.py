"""
Module to convert waypoints dict to waypoints list.
"""

from . import waypoint

def waypoints_dict_to_list(waypoint_name_to_coordinates: "dict[str, waypoint.Waypoint]") \
    -> "tuple[bool, list[waypoint.Waypoint]]":
    """
    Converts dictionary of waypoints into a list.

    Parameters
    ----------
    waypoint_name_to_coordinates: dict[str, Waypoint]
        Waypoint mapping of name to (latitude, longitude).

    Returns
    -------
    bool: Whether waypoint data conversion was a success.
    list[Waypoint]: List of the waypoint coordinates.
    """
    # Check for empty input dictionary
    if len(waypoint_name_to_coordinates) == 0:
        return False, None
    
    # Create list of all the values in the input dictionary, ie. the Waypoint
    waypoints_list = list(waypoint_name_to_coordinates.values())

    return True, waypoints_list
