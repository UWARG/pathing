"""
Name-coordinate mapping from CSV file.
"""

import pathlib

from .common.modules import location_global
from .common.modules import position_global_relative_altitude


def load_waypoint_name_to_coordinates_map(
    waypoint_file_path: pathlib.Path,
) -> tuple[True, dict[str, location_global.LocationGlobal]] | tuple[False, None]:
    """
    Creates a name to coordinate dictionary from the CSV file.

    waypoint_file_path: Path to CSV file.

    Return: Success, name to coordinate dictionary.
    """
    if not waypoint_file_path.exists():
        return False, None

    name_to_coordinates_map = {}
    with open(waypoint_file_path, encoding="utf-8") as file:
        for line in file:
            # Skip header and empty lines
            parts = line.split(",")
            if line in "name,latitude,longitude\n" or len(parts) < 3:
                continue

            name, latitude, longitude = parts
            result, named_location = location_global.LocationGlobal.create(
                float(latitude), float(longitude)
            )
            if not result:
                return False, None

            name_to_coordinates_map[name] = named_location

    if len(name_to_coordinates_map) > 0:
        return True, name_to_coordinates_map

    return False, None


def load_waypoint_name_to_coordinates_and_altitude_map(
    waypoint_file_path: pathlib.Path,
) -> (
    tuple[True, dict[str, position_global_relative_altitude.PositionGlobalRelativeAltitude]]
    | tuple[False, None]
):
    """
    Creates a name to coordinate and altitude dictionary from the CSV file.

    waypoint_file_path: Path to CSV file.

    Return: Success, name to coordinate and altitude dictionary.
    """
    if not waypoint_file_path.exists():
        return False, None

    name_to_coordinates_and_altitude_map = {}
    with open(waypoint_file_path, encoding="utf-8") as file:
        for line in file:
            # Skip header and empty lines
            parts = line.split(",")
            if line in "name,latitude,longitude,altitude\n" or len(parts) < 4:
                continue

            name, latitude, longitude, altitude = parts
            result, point = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                float(latitude), float(longitude), float(altitude)
            )
            if not result:
                return False, None

            name_to_coordinates_and_altitude_map[name] = point

    if len(name_to_coordinates_and_altitude_map) > 0:
        return True, name_to_coordinates_and_altitude_map

    return False, None
