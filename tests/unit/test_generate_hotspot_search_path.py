"""
Hotspot search path generation unit tests.
"""

import math

from modules import generate_hotspot_search_path
from modules.common.modules import position_global_relative_altitude


class TestGenerateSearchPath:
    """
    Test suite for generate_search_path.
    """

    def test_generate_search_path(self) -> None:
        """
        Test successful generation of search path.
        """
        result, center = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
            0.0, 0.0, 100.0
        )
        search_radius = 100.0
        search_area_dimensions = (20.0, 10.0)

        result, waypoints = generate_hotspot_search_path.generate_search_path(
            center, search_radius, search_area_dimensions
        )

        assert result
        assert waypoints

        camera_width, camera_height = search_area_dimensions
        current_radius = camera_width / 2
        waypoint_index = 0

        while current_radius <= search_radius:
            circumference = 2 * math.pi * current_radius
            num_points = max(3, int(circumference / camera_height))

            assert len(waypoints[waypoint_index : waypoint_index + num_points]) == num_points

            waypoint_index += num_points
            current_radius += camera_width

    def test_generate_search_path_zero_radius(self) -> None:
        """
        Test generate_search_path with a zero search radius.
        """
        result, center = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
            0.0, 0.0, 100.0
        )
        search_radius = 0.0
        search_area_dimensions = (3.0, 3.0)

        result, waypoints = generate_hotspot_search_path.generate_search_path(
            center, search_radius, search_area_dimensions
        )

        assert result
        assert waypoints == []

    def test_generate_search_path_negative_radius(self) -> None:
        """
        Test generate_search_path with a negative search radius.
        """
        result, center = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
            0.0, 0.0, 100.0
        )
        search_radius = -10.0
        search_area_dimensions = (3.0, 3.0)

        result, waypoints = generate_hotspot_search_path.generate_search_path(
            center, search_radius, search_area_dimensions
        )

        assert result is False
        assert waypoints is None

    def test_generate_search_path_invalid_dimensions(self) -> None:
        """
        Test generate_search_path with invalid search area dimensions.
        """
        result, center = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
            0.0, 0.0, 100.0
        )
        search_radius = 10.0
        search_area_dimensions = (-3, 3.0)

        result, waypoints = generate_hotspot_search_path.generate_search_path(
            center, search_radius, search_area_dimensions
        )

        assert result is False
        assert waypoints is None
