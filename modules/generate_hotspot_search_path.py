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
) -> "tuple[bool, list[position_global_relative_altitude.PositionGlobalRelativeAltitude] | None, list[int] | None]":
    """
    Generates list of spline waypoints representing concentric rings for drone search path.

    center: waypoint for center of circle.
    search_radius: drone search radius.
    search_area_dimensions: search area width, height

    Returns: Success, list of waypoints, number of waypoints per circle.
    """
    camera_horizontal_size, camera_vertical_size = search_area_dimensions

    if camera_horizontal_size <= 0 or camera_vertical_size <= 0:
        print(f"ERROR: Camera dimensions must be greater than 0: {search_area_dimensions}")
        return False, None, None

    if search_radius < 0:
        print(f"ERROR: Search radius must be greater than or equal to 0: {search_radius}")
        return False, None, None

    current_radius = camera_horizontal_size / 2

    all_waypoints = []
    waypoints_per_circle = []

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
            return False, None, None
        all_waypoints.extend(waypoints)
        waypoints_per_circle.append(len(waypoints))

        current_radius += camera_horizontal_size

    return True, all_waypoints, waypoints_per_circle


def get_search_path_sector(
    waypoints: list[position_global_relative_altitude.PositionGlobalRelativeAltitude],
    waypoints_per_circle: list[int],
    total_drones: int,
    drone_index: int,
) -> list[position_global_relative_altitude.PositionGlobalRelativeAltitude]:
    """
    Generates a sector of concentric circle for corresponding drone index.

    waypoints: list of all waypoints in concentric circles
    waypoints_per_circle: list of number of waypoints for each concentric circle
    total_drones: the total number of drones flying
    drone_index: [0, num_drones)

    Returns: list of waypoints in sector for specific drone
    """

    sector_waypoints = []
    number_of_circles = len(waypoints_per_circle)

    for i in range(number_of_circles):
        waypoints_per_drone = waypoints_per_circle[i] // total_drones

        if drone_index == total_drones - 1:
            waypoints_per_drone += (
                waypoints_per_circle[i] % total_drones
            )  # Last drone handles extras

        start = drone_index * waypoints_per_drone
        end = start + waypoints_per_drone
        sector_waypoints.extend(waypoints[start:end])

    return sector_waypoints
