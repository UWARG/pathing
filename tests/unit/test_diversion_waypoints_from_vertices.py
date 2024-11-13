"""
Test cases for creating waypoints to avoid area bounded by verticies and rejoining path
"""

import pytest
import shapely.geometry

from modules import diversion_waypoints_from_vertices
from modules.common.modules import location_global


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def restricted_vertices() -> list[location_global.LocationGlobal]:  # type: ignore
    """
    Fixture for normal restricted area.
    """
    result, waypoint_1 = location_global.LocationGlobal.create(25.0, -25.0)
    assert result
    assert waypoint_1 is not None

    result, waypoint_2 = location_global.LocationGlobal.create(25.0, 25.0)
    assert result
    assert waypoint_2 is not None

    result, waypoint_3 = location_global.LocationGlobal.create(75.0, 25.0)
    assert result
    assert waypoint_3 is not None

    result, waypoint_4 = location_global.LocationGlobal.create(75.0, -25.0)
    assert result
    assert waypoint_4 is not None

    lap_sequence = [waypoint_1, waypoint_2, waypoint_3, waypoint_4]

    yield lap_sequence


def verify_path_does_not_intersect_restriction(
    path: list[location_global.LocationGlobal], restricted_area: shapely.geometry.Polygon
) -> bool:
    """
    Check.

    path: Travelled points including start.
    restricted area: Shape that cannot be intersected with.

    Return: True if there is no intersection.
    """
    for i in range(0, len(path) - 1):
        current_point = path[i]
        next_point = path[i + 1]

        line = shapely.geometry.LineString(
            [
                (current_point.latitude, current_point.longitude),
                (next_point.latitude, next_point.longitude),
            ]
        )

        result = line.intersects(restricted_area)
        if result:
            return False

    return True


def test_no_vertices_given() -> None:
    """
    Test behaviour when given no restricted area.
    """
    # Setup
    result, start = location_global.LocationGlobal.create(0.0, 0.0)
    assert result
    assert start is not None

    result, end = location_global.LocationGlobal.create(0.0, 50.0)
    assert result
    assert end is not None

    vertices = []

    expected = [start, end]

    # Run
    result, actual = diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(
        start, end, vertices
    )

    # Check
    assert result
    assert actual == expected


def test_diversion_waypoints_from_vertices(
    restricted_vertices: list[location_global.LocationGlobal],
) -> None:
    """
    Test correctness of diversion_waypoints_from_vertices in the normal case.
    """
    # Setup
    result, start = location_global.LocationGlobal.create(0.0, 0.0)
    assert result
    assert start is not None

    result, end = location_global.LocationGlobal.create(100.0, 0.0)
    assert result
    assert end is not None

    bounded_area = shapely.geometry.Polygon(
        [(vertex.latitude, vertex.longitude) for vertex in restricted_vertices]
    )

    # Run
    result, diversion = diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(
        start, end, restricted_vertices
    )
    path = [start] + diversion

    # Check
    assert result
    assert verify_path_does_not_intersect_restriction(path, bounded_area)


def test_concave_restricted_area(
    restricted_vertices: list[location_global.LocationGlobal],
) -> None:
    """
    Test correctness of diversion_waypoints_from_vertices when restricted area has concavity.
    """
    # Setup
    result, start = location_global.LocationGlobal.create(0.0, 0.0)
    assert result
    assert start is not None

    result, end = location_global.LocationGlobal.create(100.0, 0.0)
    assert result
    assert end is not None

    result, extra_vertex = location_global.LocationGlobal.create(50.0, 0.0)
    assert result
    assert end is not None

    # Deep copy
    vertices = list(restricted_vertices)
    vertices.insert(-1, extra_vertex)

    bounded_area = shapely.geometry.Polygon(
        [(vertex.latitude, vertex.longitude) for vertex in vertices]
    )

    # Run
    result, diversion = diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(
        start, end, vertices
    )
    path = [start] + diversion

    # Check
    assert result
    assert verify_path_does_not_intersect_restriction(path, bounded_area)


def test_efficiency(restricted_vertices: list[location_global.LocationGlobal]) -> None:
    """
    Test if diversion_waypoints_from_vertices produces shortest path to rejoin point.
    """
    # Setup
    result, start = location_global.LocationGlobal.create(0.0, 0.0)
    assert result
    assert start is not None

    result, end = location_global.LocationGlobal.create(100.0, 0.0)
    assert result
    assert end is not None

    # Run
    result, path = diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(
        start, end, restricted_vertices
    )

    # Check
    assert result

    for waypoint in path:
        assert waypoint.longitude >= 0.0
