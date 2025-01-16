"""
Hotspot search path generation unit tests.
"""

import pytest

from modules import generate_hotspot_search_path
from modules.common.modules import position_global_relative_altitude


def verify_close_enough(
    actual: position_global_relative_altitude.PositionGlobalRelativeAltitude,
    expected: position_global_relative_altitude.PositionGlobalRelativeAltitude,
    tolerance: float,
) -> bool:
    """
    Check equality of positions.
    """
    if not actual.latitude == pytest.approx(expected.latitude, rel=tolerance):
        return False

    if not actual.longitude == pytest.approx(expected.longitude, rel=tolerance):
        return False

    if not actual.relative_altitude == pytest.approx(expected.relative_altitude, rel=tolerance):
        return False

    return True


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
        assert result
        assert center is not None

        expected_points = [
            (0.0, 2.245788210298689e-05),
            (2.2609236926258363e-05, 1.3751486716526466e-21),
            (2.7688329632905757e-21, -2.245788210298689e-05),
            (-2.2609236926258363e-05, -4.125446014957939e-21),
            (0.0, 6.737364630893306e-05),
            (3.3913855389367626e-05, 5.834728924913043e-05),
            (5.87405206149349e-05, 3.368682315447818e-05),
            (6.782771077874665e-05, 4.1254460149579395e-21),
            (5.87405206149349e-05, -3.3686823154478156e-05),
            (3.3913855389367653e-05, -5.8347289249130414e-05),
            (8.30649888986659e-21, -6.737364630893306e-05),
            (-3.3913855389367606e-05, -5.834728924913044e-05),
            (-5.874052061493489e-05, -3.36868231544782e-05),
            (-6.782771077874665e-05, -1.2376338044873817e-20),
            (-5.874052061493492e-05, 3.368682315447813e-05),
            (-3.391385538936766e-05, 5.8347289249130414e-05),
        ]

        search_radius = 10.0
        search_area_dimensions = (5.0, 5.0)
        result, waypoints = generate_hotspot_search_path.generate_search_path(
            center, search_radius, search_area_dimensions
        )

        assert result
        assert waypoints is not None

        # Reduced tolerance as the planet is a not a sphere
        tolerance = 1e-2

        assert len(waypoints) == len(expected_points)
        for i, expected_point in enumerate(expected_points):
            actual = waypoints[i]
            assert actual is not None

            expected_latitude, expected_longitude = expected_point
            result, expected = (
                position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                    expected_latitude, expected_longitude, center.relative_altitude
                )
            )

            assert verify_close_enough(actual, expected, tolerance)

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
