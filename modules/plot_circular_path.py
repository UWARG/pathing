"""
Module to plot n circular waypoints, given a center and radius.
"""

import math

from waypoint import Waypoint


def move_coordinates_by_offset(
    start_point: Waypoint, offset_x: float, offset_y: float, name: str
) -> Waypoint:
    """Given a starting waypoint and offsets x and y displacements, find the
    resulting waypoint.

    Args:
        starting_point (Waypoint): The starting waypoint
        offset_x (float): The (potentially negative) displacement in west-east
            direction, in meters
        offset_y (float): The (potentially negative) displacement in north-south
            direction, in meters
        name (str): The name for the resulting waypoint

    Returns:
        Waypoint: the resulting waypoint after being moved by offset from the
        original waypoint.
    """
    # both latitude and longitude are in degrees
    lat = start_point.location_ground.latitude
    lon = start_point.location_ground.longitude

    earth_radius = 6371000  # Earth's radius, in meters
    # the radius of the horizontal slice of the Earth, at the specific longitude
    slice_radius = earth_radius * math.cos(math.radians(lat))

    new_lat = lat + offset_y * (360 / (2 * math.pi * earth_radius))
    new_lon = lon + offset_x * (360 / (2 * math.pi * slice_radius))

    return Waypoint(name, new_lat, new_lon, start_point.altitude)


def generate_circular_path(center: Waypoint, radius: float, num_points: int) -> "list[Waypoint]":
    """Generate a list of `num_points` evenly-separated waypoints given a center
    and radius.

    Args:
        center (Waypoint): The center of the circular path
        radius (float): The length of the radius, in meters
        num_points (int): The number of waypoints to generate

    Returns:
        list[Waypoint]: `num_points` waypoints, evenly separated on the circular
        path.
    """
    waypoints = []

    # any two consecutive points are separated by 2 * pi / n radians.
    for i in range(num_points):
        # number of radians away from standard position
        rad = 2 * math.pi / num_points * i
        offset_x = radius * math.cos(rad)
        offset_y = radius * math.sin(rad)
        waypoints.append(
            move_coordinates_by_offset(center, offset_x, offset_y, f"Waypoint {i + 1}")
        )

    return waypoints
