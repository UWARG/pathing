"""
Generates search path for hotspots.
"""

import math

from . import plot_circular_path
from .common.modules import position_global_relative_altitude


MINIMUM_POINTS = 3


def generate_search_path(
    center: position_global_relative_altitude.PositionGlobalRelativeAltitude,
    search_radius: float,
    search_area_dimensions: "tuple[float, float]",
) -> "tuple[bool, list[position_global_relative_altitude.PositionGlobalRelativeAltitude] | None]":
    """
    Generates list of spline waypoints representing concentric rings for drone search path.

    center: waypoint for center of circle.
    search_radius: drone search radius.
    search_area_dimensions: search area width, height

    Returns: Success, list of waypoints.
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
        num_points = max(MINIMUM_POINTS, int(circumference / camera_vertical_size))

        result, waypoints = plot_circular_path.generate_circular_path(
            center, current_radius, num_points
        )
        if not result or waypoints is None:
            return False, None
        all_waypoints.extend(waypoints)

        current_radius += camera_horizontal_size

    return True, all_waypoints
