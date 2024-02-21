"""
Name-coordinate mapping from CSV file.
"""
import pathlib

from .common.kml.modules import location_ground


def load_waypoint_name_to_coordinates_map(waypoint_file_path: pathlib.Path) \
    -> "tuple[bool, dict[str, location_ground.LocationGround]]":
    """
    Creates a name to coordinate dictionary from the CSV file.
    """
    if not waypoint_file_path.exists():
        return False, None

    name_to_coordinates_map = {}
    with open(waypoint_file_path, encoding="utf-8") as file:
        for line in file:
            # Skip header and empty lines
            parts = line.split(',')
            if line in "name,latitude,longitude\n" or len(parts) < 3:
                continue

            name, latitude, longitude = parts
            name_to_coordinates_map[name] = location_ground.LocationGround(name, float(latitude), float(longitude))

    if len(name_to_coordinates_map) > 0:
        return True, name_to_coordinates_map

    return False, None
