"""
This file contains a function for converting waypoint names to objects.
"""

from modules.waypoint_class import Waypoint

def waypoint_names_to_coordinates(waypoint_names: "list[str]",
                                  waypoint_mapping: "list[Waypoint]") \
    -> "tuple[bool, list[Waypoint]]":
    """
    Converts a list of waypoint names to their full Waypoint objects based on a waypoint mapping.

    Args:
        waypoint_names (list[str]): A list of waypoint names.
        waypoint_mapping (list[Waypoint]): A list of Waypoint objects containing the name and coordinates of each waypoint.

    Returns:
        tuple[bool, list[Waypoint] : A tuple containing a boolean indicating the success of the conversion
            and a list of the Waypoint objects that correspond to the given waypoint names.
    """
    # Handle the case when waypoint_names is empty
    if len(waypoint_names) == 0:
        return False, None

    locations = []
    for name in waypoint_names:
        for waypoint in waypoint_mapping:
            if name == waypoint.name:
                locations.append(waypoint)
        else:
            return False, None

    return True, locations

# # Original code

# def waypoint_names_to_coordinates(waypoint_names: "list[str]",
#                                   waypoint_mapping: "dict[str, tuple[float, float]]") \
#     -> "tuple[bool, list[tuple[float, float]]]":
#     """
#     Converts a list of waypoint names to their corresponding coordinates based on a waypoint mapping.

#     Args:
#         waypoint_names (list[str]): A list of waypoint names.
#         waypoint_mapping (dict[str, tuple[float, float]]): A dictionary mapping waypoint names to their coordinates.

#     Returns:
#         tuple[bool, list[tuple[float, float]]]: A tuple containing a boolean indicating the success of the conversion
#             and a list of coordinates corresponding to the given waypoint names.
#     """
#     # Handle the case when waypoint_names is empty
#     if len(waypoint_names) == 0:
#         return False, None

#     coordinates = []
#     for name in waypoint_names:
#         if name in waypoint_mapping:
#             coordinate = waypoint_mapping[name]
#             coordinates.append(coordinate)
#         else:
#             return False, None

#     return True, coordinates
