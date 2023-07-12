"""
This file contains a function for converting waypoint names to coordinates.
"""

def waypoint_names_to_coordinates(waypoint_names: "list[str]",
                waypoint_mapping: "dict[str, tuple[float, float]]") \
        -> "tuple[bool, list[tuple[float, float]]]":
    """
    Converts a list of waypoint names to their corresponding coordinates based on a waypoint mapping.

    Args:
        waypoint_names (list[str]): A list of waypoint names.
        waypoint_mapping (dict[str, tuple[float, float]]): A dictionary mapping waypoint names to their coordinates.

    Returns:
        tuple[bool, list[tuple[float, float]]]: A tuple containing a boolean indicating the success of the conversion
            and a list of coordinates corresponding to the given waypoint names.
    """
    coordinates = []

    if not len(waypoint_names) == 0:  # Handle the case when waypoint_names is empty
        return False, coordinates

    for name in waypoint_names:
        if name in waypoint_mapping:
            coordinate = waypoint_mapping[name]
            coordinates.append(coordinate)
        else:
            return False, None

    return True, coordinates
