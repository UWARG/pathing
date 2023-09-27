"""
Name-coordinate mapping from CSV file.
"""
import pathlib

from modules.waypoint import Waypoint

# Function to create a list of all Waypoint objects from a CSV file

def load_waypoint_name_to_coordinates_map(waypoint_file_path: pathlib.Path) \
    -> "tuple[bool, list[Waypoint]]":
    """
    Creates a list of Waypoint ojects with names and coordinates from the CSV file.
    """
    if not waypoint_file_path.exists():
        return False, None

    waypoints_map = []
    with open(waypoint_file_path, encoding="utf-8") as file:
        for line in file:
            # Skip header and empty lines
            parts = line.split(',')
            if line in "name,latitude,longitude\n" or len(parts) < 3:
                continue

            name, latitude, longitude = parts
            waypoint = Waypoint(name, float(latitude), float(longitude))
            waypoints_map.append(waypoint)

    if len(waypoints_map) > 0:
        return True, waypoints_map

    return False, None

# # Original code

# def load_waypoint_name_to_coordinates_map(waypoint_file_path: pathlib.Path) \
#     -> "tuple[bool, dict[str, tuple[float, float]]]":
#     """
#     Creates a name to coordinate dictionary from the CSV file.
#     """
#     if not waypoint_file_path.exists():
#         return False, None

#     name_to_coordinates_map = {}
#     with open(waypoint_file_path, encoding="utf-8") as file:
#         for line in file:
#             # Skip header and empty lines
#             if line in ("name,latitude,longitude\n", ""):
#                 continue

#             name, latitude, longitude = line.split(',')
#             name_to_coordinates_map[name] = (float(latitude), float(longitude))

#     if len(name_to_coordinates_map) > 0:
#         return True, name_to_coordinates_map

#     return False, None


