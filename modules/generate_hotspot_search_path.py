"""
Generates search path for hotspots.
"""

import math

from . import plot_circular_path
from .common.modules import position_global_relative_altitude


MULTIPLIER = 1.2
MINIMUM_POINTS = 3


def generate_search_path(
    center: position_global_relative_altitude.PositionGlobalRelativeAltitude,
    search_radius: float,
    search_area_dimensions: "tuple[float, float]",
) -> "tuple[bool, list[list[position_global_relative_altitude.PositionGlobalRelativeAltitude]] | None]":
    """
    Generates list of spline waypoints representing concentric rings for drone search path.

    center: waypoint for center of circle.
    search_radius: drone search radius.
    search_area_dimensions: search area width, height

    Returns: Success, list of list of waypoints.
    """
    camera_horizontal_size, camera_vertical_size = search_area_dimensions

    if camera_horizontal_size <= 0 or camera_vertical_size <= 0:
        print(f"ERROR: Camera dimensions must be greater than 0: {search_area_dimensions}")
        return False, None

    if search_radius < 0:
        print(f"ERROR: Search radius must be greater than or equal to 0: {search_radius}")
        return False, None

    current_radius = camera_horizontal_size / 2

    all_waypoints = []

    while current_radius <= search_radius:
        circumference = 2 * math.pi * current_radius

        num_points_vertical = circumference / camera_vertical_size
        num_points_horizontal = circumference / camera_horizontal_size
        num_points = math.ceil(MULTIPLIER * max(num_points_vertical, num_points_horizontal))
        num_points = max(MINIMUM_POINTS, num_points)

        result, waypoints = plot_circular_path.generate_circular_path(
            center, current_radius, num_points
        )
        if not result or waypoints is None:
            return False, None
        all_waypoints.append(waypoints)

        current_radius += camera_horizontal_size

    return True, all_waypoints


def flatten_waypoints(
    waypoints: list[list[position_global_relative_altitude.PositionGlobalRelativeAltitude]],
) -> list[position_global_relative_altitude.PositionGlobalRelativeAltitude]:
    """
    Transforms the list of list of all waypoints by circle into a linear list.

    waypoints: list of list of all waypoints by circle

    Returns: Linear list of all the waypoints.
    """

    flattened_waypoints = [waypoint for circle in waypoints for waypoint in circle]

    return flattened_waypoints


def get_search_path_sector(
    waypoints: list[list[position_global_relative_altitude.PositionGlobalRelativeAltitude]],
    total_drones: int,
    drone_index: int,
) -> list[position_global_relative_altitude.PositionGlobalRelativeAltitude]:
    """
    Generates a sector of concentric circle for corresponding drone index.

    waypoints: list of all waypoints in concentric circles
    total_drones: the total number of drones flying
    drone_index: [0, num_drones)

    Returns: list of waypoints in sector for specific drone
    """

    if drone_index >= total_drones or drone_index < 0:
        print(f"ERROR: drone index must be in [0, total_drones): {drone_index}")
        return []

    sector_waypoints = []
    number_of_circles = len(waypoints)

    for i in range(number_of_circles):
        waypoints_per_drone = len(waypoints[i]) // total_drones

        start = drone_index * waypoints_per_drone

        if drone_index == total_drones - 1:
            waypoints_per_drone += len(waypoints[i]) % total_drones  # Last drone handles extras
            
        end = start + waypoints_per_drone
        sector_waypoints.extend(waypoints[i][start:end])

    return sector_waypoints