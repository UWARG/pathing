"""
Module to convert waypoints dict to waypoints list.
"""

def waypoints_dict_to_list(waypoint_name_to_coordinates: "dict[str, tuple[float, float]]") -> "tuple[bool, list[tuple[float,float]]]":
    """
    Converts dictionary of waypoints into a list.

    Parameters
    ----------
    waypoint_name_to_coordinates: dict[str, tuple[float, float]]]
        Waypoint mapping of name to (latitude, longitude).

    Returns
    -------
    bool: Whether waypoint data conversion was a success.
    list[tuple[float, float]]: List of the waypoint coordinates.
    """
    # check for empty input dictionary
    if not waypoint_name_to_coordinates:
        return False, None
    
    # create list of all the values in the input dictionary, ie. the tuple[float, float]
    waypoints_list = list(waypoint_name_to_coordinates.values())

    return True, waypoints_list
