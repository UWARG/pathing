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
            (0.0, 2.245788210298689e-05),
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
            (0.0, 6.737364630893306e-05),
        ]

        search_radius = 10.0
        search_area_dimensions = (5.0, 5.0)
        result, waypoints = generate_hotspot_search_path.generate_search_path(
            center, search_radius, search_area_dimensions
        )

        assert result
        assert waypoints is not None

        waypoints = generate_hotspot_search_path.flatten_waypoints(waypoints)

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


def generate_waypoints(
    number_of_circles: int, points_per_circle: list[int]
) -> list[list[position_global_relative_altitude.PositionGlobalRelativeAltitude]]:
    """
    Generates dummy values for testing purposes. For simplicity, each waypoint longitude
    starts from 0 and increments by 1 for each concentric circle. The latitude is just the index of
    the circle and the altitude is constant.

    number_of_circles: number of concentric circles
    points_per_circle: A list of integers representing the number of waypoints for each circle

    Returns: A 2D list of waypoints by circle.
    """

    waypoints = []

    for i in range(number_of_circles):
        number_of_points = points_per_circle[i]
        circle_waypoints = []

        for j in range(number_of_points):
            logitude = j
            latitude = i

            _, waypoint = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                latitude, logitude, 100
            )

            circle_waypoints.append(waypoint)

        waypoints.append(circle_waypoints)

    return waypoints


class TestGetSearchPathSector:
    """
    Test suite for get_search_path_sector.
    """

    def test_get_search_path_sector(self) -> None:
        """
        Test successful generation of search path sector for multiple drones.
        """

        number_of_circles = 5
        points_per_circle = [4, 8, 11, 15, 17]
        waypoints = generate_waypoints(number_of_circles, points_per_circle)
        total_drones = 3

        expected_longitudes = []
        for drone_index in range(total_drones):
            current_longitudes = []
            for circle in waypoints:
                waypoints_per_drone = len(circle) // total_drones

                start = drone_index * waypoints_per_drone
                end = start + waypoints_per_drone

                if drone_index == total_drones - 1:
                    end = len(circle)

                current_longitudes.extend(circle[i].longitude for i in range(start, end))
            expected_longitudes.append(current_longitudes)

        for drone_index in range(total_drones):
            sector = generate_hotspot_search_path.get_search_path_sector(
                waypoints, total_drones, drone_index
            )

            if drone_index in (0, 1):
                assert len(sector) == 16
            elif drone_index == 2:
                assert len(sector) == 23

            assert [waypoint.longitude for waypoint in sector] == expected_longitudes[drone_index]

    def test_get_search_path_sector_one_drone(self) -> None:
        """
        Test successful generation of search path sector for one drone.
        """

        number_of_circles = 5
        points_per_circle = [4, 8, 11, 15, 17]
        waypoints = generate_waypoints(number_of_circles, points_per_circle)
        total_drones = 1

        sector = generate_hotspot_search_path.get_search_path_sector(waypoints, total_drones, 0)

        assert len(sector) == 55
        index = 0
        for i in range(number_of_circles):
            for j in range(points_per_circle[i]):
                assert j == sector[index].longitude
                index += 1

    def test_get_search_path_sector_empty_waypoints_list(self) -> None:
        """
        Test get_search_path_sector with empty waypoints list
        """

        total_drones = 3
        drone_index = 0

        waypoints = []
        sector = generate_hotspot_search_path.get_search_path_sector(
            waypoints, total_drones, drone_index
        )
        assert not sector

    def test_get_search_path_sector_invalid_index(self) -> None:
        """
        Test get_search_path_sector with invalid drone index
        """

        number_of_circles = 5
        points_per_circle = [4, 8, 11, 15, 17]
        waypoints = generate_waypoints(number_of_circles, points_per_circle)
        total_drones = 3
        drone_index = 3

        sector = generate_hotspot_search_path.get_search_path_sector(
            waypoints, total_drones, drone_index
        )
        assert not sector
